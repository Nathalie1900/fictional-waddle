def main():
    # Prompt user for text
    text = input("Text: ")

    # Count letters, words and sentences in text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate Coleman-Liau index
    index = coleman_liau(letters, words, sentences)

    # Print grade level
    if index < 1:
        print("Before Grade 1")
    elif 0 < index < 16:
        print(f"Grade {index}")
    else:
        print("Grade 16+")


def count_letters(text):
    # Count all alphabetical characters
    letters = 0
    length = len(text)

    for i in range(length):
        is_letter = text[i].isalpha()
        if is_letter == True:
            letters += 1
    return letters


def count_words(text):
    # Count all spaces and add 1
    words = 0
    length = len(text)

    for i in range(length):
        if text[i] == ' ':
            words += 1
    words += 1
    return words


def count_sentences(text):
    # // Count all '.', '?' and '!'
    sentences = 0
    length = len(text)

    for i in range(length):
        if text[i] == '.' or text[i] == '?' or text[i] == '!':
            sentences += 1
    return sentences


def coleman_liau(letters, words, sentences):
    # Calculate index
    L = letters / words * 100
    S = sentences / words * 100
    index = round((0.0588 * L) - (0.296 * S) - 15.8)
    return index


main()
