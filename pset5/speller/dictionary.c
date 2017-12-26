/**
 * Implements a dictionary's functionality.
 * Uses tries for speed.
 */

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

// define data structure (trie)
typedef struct node
{
    bool is_word;
    struct node* children[27];
}
node;

// root node
node* root;

// word count
int words = 0;


/**
 * Finds the index of a character within the trie.
 */
unsigned int find(const char c)
{
    int index;
    // if apostrophe
    if (c == '\'')
    {
        index = 26;
    }
    // general case
    else
    {
        index = tolower(c) % 'a';
    }
    return index;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // set cursor
    node *cursor = root;
    // go through input word
    for (int i = 0; word[i] != '\0'; i++)
    {
        // find index of letter
        int index = find(word[i]);
        // if next character does not exist in the trie
        if (cursor->children[index] == NULL)
        {
            return false;
        }
        // move cursor along
        cursor = cursor->children[index];
    }
    // at end of word
    return cursor->is_word;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // allocate memory to root
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        unload();
        return false;
    }
    // initialize values
    for (int i = 0; i < 27; i++)
    {
        root->children[i] = NULL;
        root->is_word = false;
    }

    // open file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // set cursor
    node* cursor = root;

    // go through entire file
    for (char c = fgetc(file); c != EOF; c = fgetc(file))
    {
        // if end of word
        if (c == '\n')
        {
            // mark as word, increment word count and reset cursor to root
            cursor->is_word = true;
            words += 1;
            cursor = root;
        }
        // general case
        else
        {
            int index = find(c);
            // if node not already there, create new node
            if (cursor->children[index] == NULL)
            {
                // allocate new node in memory
                cursor->children[index] = malloc(sizeof(node));
                // initialize values
                cursor = cursor->children[index];
                for (int i = 0; i < 27; i++)
                {
                    cursor->children[i] = NULL;
                    cursor->is_word = false;
                }
            }
            else
            {
                // move cursor on
                cursor = cursor->children[index];
            }
        }
    }
    // close file
    fclose(file);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return words;
}

/**
 * Recursively frees a trie from memory
 */
void clear(node* node)
{
    for (int i = 0; i < 27; i++)
    {
        // if memory in use, free it
        if (node->children[i] != NULL)
        {
            clear(node->children[i]);
        }
    }
    free(node);
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // call clear
    clear(root);
    return true;
}
