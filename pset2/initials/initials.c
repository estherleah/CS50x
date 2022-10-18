#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void printInitial(char);
bool isFirst;

int main(void)
{
    // get string and check isn't null
    string s = get_string();
    if (s != NULL)
    {
        // check if first character is a letter
        if (isalpha(s[0]))
        {
            // if it is, assign true
            isFirst = true;
        }
        else
        {
            // otherwise, assign false
            isFirst = false;
        }
        // iterate over string
        for (int i = 0, n = strlen(s); i < n; i++)
        {
            if (isFirst)
            {
                printInitial(s[i]);
            }
            if (s[i] == ' ' && !isspace(s[i + 1]))
            {
                isFirst = true;
            }
        }
        printf("\n");
    }
}

// print the initials
void printInitial(char c)
{
    printf("%c", toupper(c));
    isFirst = false;
}
