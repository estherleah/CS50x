#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_UPPER 'A'
#define MIN_LOWER 'a'

void printCipher(string, string);
char getKey(string, int);

int main(int argc, string argv[])
{
    // check correct number of arguments
    if (argc != 2) {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    // check 2nd argument is all letters
    for (int i = 0, n = strlen(argv[1]); i < n; i++) {
        if (!isalpha(argv[1][i])) {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
    // assign the 2nd arguement as key
    string k = argv[1];
    // get plaintext from user
    printf("plaintext: ");
    string s = get_string();
    // pass string and key to a function that ciphers it
    printf("ciphertext: ");
    printCipher(k, s);
    return 0;
}

void printCipher(string k, string s)
{
    for (int i = 0, j = 0, n = strlen(s); i < n; i++)
    {
        // if i'th char is a letter
        if (isalpha(s[i]))
        {
            // if is upper case
            if (isupper(s[i]))
            {
                printf("%c", ((s[i] - MIN_UPPER + getKey(k, j)) % 26) + MIN_UPPER);
            }
            // if is lower case
            if (islower(s[i]))
            {
                printf("%c", ((s[i] - MIN_LOWER + getKey(k, j)) % 26) + MIN_LOWER);
            }
            // increment j
            j++;
            if (j == strlen(k))
            {
                j = 0;
            }
        }
        // else just print the character
        else {
            printf("%c", s[i]);
        }
    }
    printf("\n");
}

char getKey(string k, int j)
{
    // return the next character of the key
    return tolower(k[j]) - MIN_LOWER;
}
