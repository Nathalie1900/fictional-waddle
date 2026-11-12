import csv
from sys import argv


def main():

    # Check for command-line usage
    if len(argv) != 3:
        print("Usage: python dna.py database sequence")

    # Read database file into a variable
    rows = []
    with open(argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    with open(argv[2]) as file_2:
        sequence = file_2.read()

    # Find longest match of each STR in DNA sequence
    subsequences = reader.fieldnames
    subsequences_1 = subsequences[1:]
    cant_subsequences = len(subsequences)
    cant_repetitions = []
    for subsequence in subsequences_1:
        longest_run = longest_match(sequence, subsequence)
        cant_repetitions.append(longest_run)

    # Check database for matching profiles

    # Note to self:
    # On line 37, subsequences_1[counter] gives the name of a subsequence
    # Then, row[subsequences_1[counter]] equals row[name of subsequence] using that name as a key to access its value
    # Finally, int() is used to convert that value to integer so it can be compared to cant_repetitions[counter],
    # As in the csv file it was stored as a string

    for row in rows:
        counter = 0
        match = True
        for subsequence in subsequences_1:
            counter += 1
            if int(row[subsequences_1[counter - 1]]) == cant_repetitions[counter - 1]:
                continue
            else:
                match = False
                break
        if match == True:
            print(f"{row['name']}")
            break
    if match == False:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
