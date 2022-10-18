#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        printf("Height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= height - i - 2; j++)
        {
            printf(" ");
        }
        for (int k = height; k > height - i - 1; k--)
        {
            printf("#");
        }
        printf("  ");
        for (int k = height; k > height - i - 1; k--)
        {
            printf("#");
        }
        printf("\n");
    }
}
