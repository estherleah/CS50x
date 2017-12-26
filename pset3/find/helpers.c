/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    int start = 0;
    int end = n - 1;
    int middle = (start + end) / 2;
    while (end - start + 1 > 0)
    {
        if (values[middle] == value)
        {
            return true;
        }
        // search left side of list
        else if (values[middle] > value)
        {
            end = middle - 1;
            middle = (start + end) / 2;
        }
        // search right side of list
        else
        {
            start = middle + 1;
            middle = (start + end) / 2;
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int value;
    int position = 0;
    // find largest value in counting array
    int max = 0;
    for (int i = 0; i < n; i++)
    {
        if (values[i] > max)
        {
            max = values[i];
        }
    }
    // create counting array
    max += 1;
    int counting[max];
    // initialise all values in the array
    for (int i = 0; i < max; i++)
    {
        counting[i] = 0;
    }
    // go through each element in values
    for (int i = 0; i < n; i++)
    {
        // increment the counting array at the value position
        value = values[i];
        counting[value] += 1;
    }
    // go through counting array
    for (int i = 0; i < max; i++)
    {
        while (counting[i] > 0)
        {
            values[position] = i;
            // decrement the count and increment the position
            counting[i] -= 1;
            position += 1;
        }
    }
}
