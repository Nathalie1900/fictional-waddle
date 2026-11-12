#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int score(string word);

// Array of points for each letter by position (has to be outside of all functions for it to be
// always accesible)
int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void)
{
    // Prompt 2 players for words

    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calculate scores

    int score1 = score(word1);
    int score2 = score(word2);

    // Print winner

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int score(string word)
{
    // Declare variables
    int score = 0;
    int lenght = strlen(word);

    // Go through every character in word and check if uppercase, lowercase or neither
    for (int i = 0; i < lenght; i++)
    {
        // if the character isn't alphabetical, just skip
        if (isalpha(word[i]) == 0)
        {
            continue;
            // the continue statement will skip the loop iteration in this case
        }
        // check if lowercase
        else if (islower(word[i]))
        {
            score += points[word[i] - 'a'];
            // i.e.: if char = 'z' the ASCII code for 'z' minus the one for 'a' is how many letters
            // apart from 'a' and equals position in points[]
        }
        // check if uppercase
        else
        {
            score += points[word[i] - 'A'];
        }
    }

    return score;
}
