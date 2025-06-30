import random

def create_word_search(words, size):
    grid = [['' for _ in range(size)] for _ in range(size)]
    
    directions = [
        (0,1),  # right
        (1,0),  # down
        (1,1),  # diagonal down-right
        (-1,1), # diagonal up-right
    ]
    
    def can_place(word, row, col, dr, dc):
        for i in range(len(word)):
            r = row + dr*i
            c = col + dc*i
            if r < 0 or r >= size or c < 0 or c >= size:
                return False
            if grid[r][c] != '' and grid[r][c] != word[i]:
                return False
        return True
    
    def place_word(word):
        attempts = 100
        while attempts > 0:
            dr, dc = random.choice(directions)
            row = random.randint(0, size-1)
            col = random.randint(0, size-1)
            if can_place(word, row, col, dr, dc):
                for i in range(len(word)):
                    r = row + dr*i
                    c = col + dc*i
                    grid[r][c] = word[i]
                return True
            attempts -= 1
        return False

    for w in words:
        place_word(w.upper())

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '':
                grid[r][c] = random.choice(alphabet)
    
    return grid

def spaced_line(row, space_count):
    space = ' ' * space_count
    return space.join(row)

def generate_puzzle_text(grid, space_count):
    lines = [spaced_line(row, space_count) for row in grid]
    return "\n".join(lines)

if __name__ == "__main__":
    word_list_input = input("Enter your comma-separated words: ")
    size_input = input("Enter puzzle size (10, 12, or 15): ")
    space_input = input("Enter number of spaces between letters (0 or more): ")
    puzzle_name = input("Enter a name for this Word Search puzzle: ")

    words = [w.strip() for w in word_list_input.split(',') if w.strip()]
    try:
        size = int(size_input)
        if size not in (10, 12, 15):
            raise ValueError
    except ValueError:
        print("Invalid size! Using default size 15.")
        size = 15
    
    try:
        space_between_letters = int(space_input)
        if space_between_letters < 0:
            print("Negative spacing not allowed. Using 0.")
            space_between_letters = 0
    except ValueError:
        print("Invalid spacing! Using 0.")
        space_between_letters = 0

    grid = create_word_search(words, size)
    puzzle_text = generate_puzzle_text(grid, space_between_letters)

    filename_safe = puzzle_name.strip().replace(' ', '_').lower() or "puzzle_output"
    filename = f"puzzle_{filename_safe}.txt"

    with open(filename, "w") as f:
        f.write(puzzle_text)

    print(f"Puzzle saved to '{filename}'.")
