import curses
import os
from pathlib import Path
import time

class BookReader:
    def __init__(self):
        self.books = []
        self.current_book = None
        self.current_text = ""
        self.current_pos = 0
        self.auto_scroll = False
        self.scroll_speed = 1
        self.page_size = 20  # lines per page
        
    def load_book(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.current_text = f.read()
                self.current_pos = 0
                self.books.append(filepath)
                self.current_book = filepath
                return True
        except Exception as e:
            return False

    def get_current_page(self, height):
        lines = self.current_text.split('\n')
        start = self.current_pos
        end = min(start + height - 4, len(lines))
        return lines[start:end]

    def next_page(self, height):
        lines = self.current_text.split('\n')
        self.current_pos = min(self.current_pos + height - 4, len(lines) - (height - 4))

    def prev_page(self, height):
        self.current_pos = max(0, self.current_pos - (height - 4))

class BookBotUI:
    def __init__(self):
        self.reader = BookReader()
        self.mode = "page"  # "page" or "scroll"
        self.books_dir = Path("books")

    def draw_menu(self, stdscr, selected_idx):
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        
        # Draw header
        header = "BookBot Reader"
        stdscr.addstr(0, (width - len(header)) // 2, header, curses.A_BOLD)
        
        # Draw available books
        books = list(self.books_dir.glob("*.txt"))
        for idx, book in enumerate(books):
            y = idx + 2
            if y < height - 1:
                prefix = ">" if idx == selected_idx else " "
                text = f"{prefix} {book.name}"
                stdscr.addstr(y, 2, text[:width-4])
        
        # Draw footer
        footer = "↑/↓: Select | Enter: Open | q: Quit"
        if height > 5:
            stdscr.addstr(height-1, 0, footer[:width-1])
        
        stdscr.refresh()
        return books

    def draw_reader(self, stdscr):
        height, width = stdscr.getmaxyx()
        while True:
            stdscr.clear()
            
            # Draw header
            if self.reader.current_book:
                header = f"Reading: {Path(self.reader.current_book).name}"
                mode_info = f"Mode: {'Auto-scroll' if self.mode == 'scroll' else 'Page'}"
                stdscr.addstr(0, 0, header[:width-1], curses.A_BOLD)
                stdscr.addstr(0, max(width - len(mode_info) - 1, 0), mode_info)
            
            # Draw content
            if self.reader.current_text:
                current_page = self.reader.get_current_page(height)
                for idx, line in enumerate(current_page):
                    if idx + 2 < height - 1:
                        stdscr.addstr(idx + 2, 0, line[:width-1])
            
            # Draw footer
            footer = "←/→: Page | s: Toggle Scroll | +/-: Speed | m: Menu | q: Quit"
            stdscr.addstr(height-1, 0, footer[:width-1])
            
            stdscr.refresh()
            
            if self.mode == "scroll" and self.reader.current_text:
                time.sleep(1 / self.reader.scroll_speed)
                self.reader.next_page(height)
                continue
            
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('m'):
                return 'menu'
            elif key == ord('s'):
                self.mode = "scroll" if self.mode == "page" else "page"
            elif key == ord('+') or key == ord('='):
                self.reader.scroll_speed = min(10, self.reader.scroll_speed + 1)
            elif key == ord('-'):
                self.reader.scroll_speed = max(1, self.reader.scroll_speed - 1)
            elif key == curses.KEY_RIGHT and self.mode == "page":
                self.reader.next_page(height)
            elif key == curses.KEY_LEFT and self.mode == "page":
                self.reader.prev_page(height)

    def main(self, stdscr):
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.timeout(-1)  # No timeout for getch
        
        selected_idx = 0
        current_view = 'menu'
        
        while True:
            if current_view == 'menu':
                books = self.draw_menu(stdscr, selected_idx)
                
                key = stdscr.getch()
                if key == ord('q'):
                    break
                elif key == curses.KEY_UP:
                    selected_idx = (selected_idx - 1) % len(books)
                elif key == curses.KEY_DOWN:
                    selected_idx = (selected_idx + 1) % len(books)
                elif key == 10:  # Enter key
                    if books:
                        if self.reader.load_book(books[selected_idx]):
                            current_view = 'reader'
            
            elif current_view == 'reader':
                result = self.draw_reader(stdscr)
                if result == 'menu':
                    current_view = 'menu'

def main():
    app = BookBotUI()
    curses.wrapper(app.main)

if __name__ == "__main__":
    main()
