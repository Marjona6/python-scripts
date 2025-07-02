import random
import os

def create_word_search(words, size, attempts_per_word=1000):
    grid = [['' for _ in range(size)] for _ in range(size)]
    
    directions = [
        (0,1),   # right
        (1,0),   # down
        (1,1),   # diagonal down-right
        (-1,1)   # diagonal up-right
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

    def count_overlap(word, row, col, dr, dc):
        overlap = 0
        for i in range(len(word)):
            r = row + dr*i
            c = col + dc*i
            if grid[r][c] == word[i]:
                overlap += 1
        return overlap

    def place_word_smart(word):
        best = []
        best_overlap = -1
        # Shuffle directions for more randomness
        dirs = directions[:]
        random.shuffle(dirs)
        # Generate all grid positions and shuffle
        positions = [(row, col) for row in range(size) for col in range(size)]
        random.shuffle(positions)
        for dr, dc in dirs:
            for row, col in positions:
                if can_place(word, row, col, dr, dc):
                    overlap = count_overlap(word, row, col, dr, dc)
                    if overlap > best_overlap:
                        best = [(row, col, dr, dc)]
                        best_overlap = overlap
                    elif overlap == best_overlap:
                        best.append((row, col, dr, dc))
        if best:
            row, col, dr, dc = random.choice(best)
            for i in range(len(word)):
                r = row + dr*i
                c = col + dc*i
                grid[r][c] = word[i]
            return True
        return False

    placed_words = []
    failed_words = []
    words_by_length = sorted(words, key=len, reverse=True)
    for w in words_by_length:
        for _ in range(attempts_per_word):
            if place_word_smart(w.upper()):
                placed_words.append(w)
                break
        else:
            failed_words.append(w)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '':
                grid[r][c] = random.choice(alphabet)
    return grid, placed_words, failed_words

def spaced_line(row, space_count):
    space = ' ' * space_count
    return space.join(row)

def generate_puzzle_text(grid, space_count):
    lines = [spaced_line(row, space_count) for row in grid]
    return "\n".join(lines)

if __name__ == "__main__":
    word_list_input = input("Enter your comma-separated words: ")
    size_input = input("Enter puzzle size (10, 12, or 15) [default 10]: ")
    space_input = input("Enter number of spaces between letters (0 or more) [default 3]: ")
    puzzle_name = input("Enter a name for this Word Search puzzle: ")

    words = [w.strip() for w in word_list_input.split(',') if w.strip()]
    max_word_length = max(len(word) for word in words)
    try:
        size = int(size_input) if size_input.strip() else 10
        if size not in (10, 12, 15):
            print(f"Invalid size! Using size 10.")
            size = 10
        elif size < max_word_length:
            print(f"Grid size {size} is too small for longest word ({max_word_length} letters).")
            size = max(10, max_word_length)
            print(f"Using size {size} instead.")
    except ValueError:
        size = max(10, max_word_length)
        print(f"Invalid size! Using size {size}.")
    try:
        space_between_letters = int(space_input) if space_input.strip() else 3
        if space_between_letters < 0:
            print("Negative spacing not allowed. Using 3.")
            space_between_letters = 3
    except ValueError:
        print("Invalid spacing! Using 3.")
        space_between_letters = 3

    # Try multiple full generations, keep the best
    best_grid = None
    best_placed = []
    best_failed = words
    best_score = -1
    for _ in range(10):
        grid, placed_words, failed_words = create_word_search(words, size, attempts_per_word=1000)
        if len(placed_words) > best_score:
            best_score = len(placed_words)
            best_grid = grid
            best_placed = placed_words
            best_failed = failed_words
        if not failed_words:
            break
    puzzle_text = generate_puzzle_text(best_grid, space_between_letters)
    os.makedirs("puzzles/clean", exist_ok=True)
    filename_safe = puzzle_name.strip().replace(' ', '_').lower() or "puzzle_output"
    filename = f"puzzles/clean/puzzle_{filename_safe}.txt"
    word_list_text = "\n\nWords to find:\n" + ", ".join(best_placed)
    if best_failed:
        warning_text = f"\n\nWARNING: {len(best_failed)} word(s) could not be placed due to space constraints:\n" + ", ".join(best_failed)
        complete_puzzle_text = puzzle_text + word_list_text + warning_text
    else:
        complete_puzzle_text = puzzle_text + word_list_text
    with open(filename, "w") as f:
        f.write(complete_puzzle_text)
    print(f"Puzzle saved to '{filename}'.")
    if best_failed:
        print(f"\nWARNING: The following {len(best_failed)} word(s) could not be placed due to space constraints:")
        for word in best_failed:
            print(f"  - {word}")
        print(f"Successfully placed {len(best_placed)} out of {len(words)} words.")
    else:
        print(f"All {len(words)} words were successfully placed in the puzzle.")
