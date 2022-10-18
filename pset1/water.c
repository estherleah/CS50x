#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("How many minutes did you spend in the shower? ");
    int minutes = get_int();
    int bottles = minutes * 12;
    printf("%i\n", bottles);
}
