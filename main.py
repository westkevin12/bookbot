def sort_on(dict):
    return dict["count"]

def count_chars(text):
    chars = {}
    for char in text.lower():
        if char.isalpha():
            if char in chars:
                chars[char] += 1
            else:
                chars[char] = 1
    return chars

def count_words(book):
    with open(book) as f:
        file_contents = f.read()
        words = file_contents.split()
        return len(words)

def get_book(book):
    with open(book) as f:
        file_contents = f.read()
        return file_contents

def main():
    path = "books/frankenstein.txt"
    text = get_book(path)
    word_count = count_words(path)
    print("--- Begin report of books/frankenstein.txt ---")
    print(f"{word_count} words found in the document\n")
    
    char_counts = count_chars(text)
    char_list = [{"char": char, "count": count} for char, count in char_counts.items()]
    char_list.sort(reverse=True, key=sort_on)
    
    for char_data in char_list:
        print(f"The '{char_data['char']}' character was found {char_data['count']} times")
    
    print("--- End report ---")

if __name__ == "__main__":
    main()
