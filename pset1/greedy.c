#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int total = 0;
    float change;
    do
    {
        printf("How much change is owed? ");
        change = get_float();
    }
    while (change < 0);
    int cents = round(change * 100);
    while (cents >= quarter)
    {
        cents = cents - quarter;
        total++;
    }
    while (cents >= dime)
    {
        cents = cents - dime;
        total++;
    }
    while (cents >= nickel)
    {
        cents = cents - nickel;
        total++;
    }
    while (cents >= penny)
    {
        cents = cents - penny;
        total++;
    }
    printf("%i\n", total);
}
