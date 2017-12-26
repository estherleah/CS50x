/**
 * Recovers JPEG files from a corrupt memory card
 */

#include <stdio.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // create buffer
    uint8_t buffer[512];
    FILE *image = NULL;
    int count = 0;

    // check every 512 block
    while (fread(buffer, 512, 1, inptr))
    {
        // check if first 4 bytes correspond to JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close file if it is open
            if (image != NULL)
            {
                fclose(image);
            }
            // open JPEG
            char filename[8];
            sprintf(filename, "%03i.jpg", count);
            image = fopen(filename, "w");
            count += 1;
        }
        if (image != NULL)
        {
            fwrite(buffer, 512, 1, image);
        }
    }

    if (image != NULL)
    {
        fclose(image);
    }

    // close input file
    fclose(inptr);

    return 0;
}
