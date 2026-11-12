// Future Improvements:
// 1. Change the number of buckets in the hash table for less collisions.
// Hash function that creates a 26*26 hash table (676 buckets)
// If the first letter is b and the second one is b, it's 1 * 26 + 1, meaning table_index 27
// int hash_value = ((toupper(word[0]) - 'A') * 26) + (toupper(word[1]) - 'A');
// 2. Free the memory in all error paths in the load function to prevent memory leaks.

// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N]; // this array contains N node pointers

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain its hash value
    int table_index = hash(word);
    // Search the hash table at the location specified by the word’s hash value
    char case_insensitive[strlen(word) + 1];

    for (node *ptr = table[table_index]; ptr != NULL; ptr = ptr->next)
    {
        for (int i = 0; i < strlen(word) + 1; i++)
        {
            case_insensitive[i] = tolower(word[i]);
        }
        if (strcmp(case_insensitive, ptr->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");

    if (source == NULL)
    {
        printf("Could not open dictionary\n");
        return false;
    }

    // Read each word in the file
    char buffer;
    char word[LENGTH + 1];
    int index = 0;

    while (fread(&buffer, sizeof(char), 1, source)) // if wrong use fscanf function
    {
        if (buffer != '\n')
        {
            word[index] = buffer;
            index++;
        }
        else // if buffer == \n
        {
            // prepare index for new word
            word[index] = '\0';
            index = 0;

            // Add each word to the hash table

            // Create space for a new hash table node
            node *new_node = malloc(sizeof(node));
            if (new_node == NULL)
            {
                return false;
            }

            // Copy the word into the new node
            strcpy(new_node->word, word);
            new_node->next = NULL;
            // printf("%s\n", new_node->word); I used this to debug

            // Hash the word to obtain its hash value
            int table_index = hash(word);

            // Insert the new node into the hash table (using the index specified by its hash
            // value), preppending it to the list
            new_node->next = table[table_index];
            table[table_index] = new_node;
        }
    }

    // Close the dictionary file
    fclose(source);

    // If loading successful
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int counter = 0;
    for (int i = 0; i < N; i++)
    {
        // Iterate over nodes in table[i]
        for (node *ptr = table[i]; ptr != NULL; ptr = ptr->next)
        {
            counter++;
        }
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *next = ptr->next;
            free(ptr);
            ptr = next;
        }
    }
    return true;
}
