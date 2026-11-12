#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Future changes:
// 1. Use character aritmetic instead of the alphabet strings to eliminate the need for the position
// calculation loop. (i.e.: the position of any letter in a hipothetical alphabet string is its ASCII
// number - 'a' or 'A' ASCII numbers)
// 2. Handle code repetition in rotate function.
// (it has some duplicated logic for handling lowercase and uppercase characters).

const string alphabetlower = {"abcdefghijklmnopqrstuvwxyz"};
const string alphabetupper = {"ABCDEFGHIJKLMNOPQRSTUVWXYZ"};

char rotate(char character, int key);

int main(int argc, string argv[])
{
    // Missing or too many command line arguments

    if (argc != 2)
    {
        fprintf(stderr, "Error. Must include one command line argument.\n");
        return 1;
    }

    // Check that command line argument just has digits

    else
    {
        int digits = 0;
        int len = strlen(argv[1]);

        for (int i = 0; i < len; i++)
        {
            if (isdigit(argv[1][i]))
            {
                digits++;
            }
        }

        // Command line argument doesn't have just digits

        if (digits < len)
        {
            fprintf(stderr, "Usage: ./caesar key\n");
            return 1;
        }

        // Command like argument has just digits

        else
        {
            int k = atoi(argv[1]);
            string plaintext = get_string("plaintext:  ");
            int length = strlen(plaintext);

            printf("ciphertext: ");

            for (int i = 0; i < length; i++)
            {
                char newc = rotate(plaintext[i], k);
                printf("%c", newc);
            }
            printf("\n");
            return 0;
        }
    }
}

char rotate(char character, int key)
{
    if (isalpha(character) == 0)
    {
        return character;
    }
    else
    {
        // Identify current position of character

        int position = 0;

        for (int i = 0; i < 26; i++)
        {
            if (islower(character))
            {
                if (alphabetlower[i] != character)
                {
                    position++;
                }
                else
                {
                    break;
                }
            }

            else
            {
                if (alphabetupper[i] != character)
                {
                    position++;
                }
                else
                {
                    break;
                }
            }
        }

        // Calculate new position for character

        int new_position = (position + key) % 26;

        // Get new character

        if (islower(character))
        {
            char new_c = alphabetlower[new_position];
            return new_c;
        }
        else
        {
            char new_c = alphabetupper[new_position];
            return new_c;
        }
    }
}
