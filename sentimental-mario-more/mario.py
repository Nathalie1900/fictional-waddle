from cs50 import get_int


def main():
    # Prompt user for height
    while True:
        height = get_int("Height: ")
        if 0 < height < 9:
            break

    spaces = height
    for i in range(height):
        # Print each row
        print_row(spaces - 1, i + 1)
        spaces -= 1


def print_row(spaces, bricks):
    # Print one row at a time
    print(" " * spaces, "#" * bricks, "  ", "#" * bricks, sep='', end='')
    # Add a new line
    print()


main()
