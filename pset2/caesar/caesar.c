#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_UPPER 'A'
#define MIN_LOWER 'a'

void printCipher(int, string);
int main(int argc, string argv[])
{
    // check correct number of arguments
    if (argc != 2) {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    // assign the 2nd arguement as key
    int k = atoi(argv[1]);
    // get plaintext from user
    printf("plaintext: ");
    string s = get_string();
    // pass string and key to a function that ciphers it
    printf("ciphertext: ");
    printCipher(k, s);
    return 0;
}

void printCipher(int k, string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // if i'th char is a letter
        if (isalpha(s[i]))
        {
            // if is upper case
            if (isupper(s[i]))
            {
                printf("%c", ((s[i] - MIN_UPPER + k) % 26) + MIN_UPPER);
            }
            // if is lower case
            if (islower(s[i]))
            {
                printf("%c", ((s[i] - MIN_LOWER + k) % 26) + MIN_LOWER);
            }
        }
        // else just print the character
        else
        {
            printf("%c", s[i]);
        }
    }
    // print newline
    printf("\n");
}
