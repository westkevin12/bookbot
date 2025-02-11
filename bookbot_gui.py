import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path

class BookBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BookBot Reader")
        self.root.geometry("1024x768")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.setup_book_selection()
        self.setup_reading_area()
        self.setup_controls()

    def setup_book_selection(self):
        # Book selection frame
        selection_frame = ttk.LabelFrame(self.main_container, text="Book Selection", padding="5")
        selection_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Add book button
        self.add_btn = ttk.Button(selection_frame, text="Add Books", command=self.add_books)
        self.add_btn.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Book list
        self.book_list = tk.Listbox(selection_frame, selectmode=tk.MULTIPLE, height=6)
        self.book_list.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Scrollbar for book list
        scrollbar = ttk.Scrollbar(selection_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.book_list.configure(yscrollcommand=scrollbar.set)

    def setup_reading_area(self):
        reading_frame = ttk.LabelFrame(self.main_container, text="Reading Area", padding="5")
        reading_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        reading_frame.columnconfigure(0, weight=1)
        reading_frame.rowconfigure(0, weight=1)
        
        # Text widget for displaying book content
        self.text_area = tk.Text(reading_frame, wrap=tk.WORD, padx=10, pady=10)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text area
        text_scroll = ttk.Scrollbar(reading_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        text_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_area.configure(yscrollcommand=text_scroll.set)

    def setup_controls(self):
        # Controls frame
        controls_frame = ttk.LabelFrame(self.main_container, text="Reading Controls", padding="5")
        controls_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Reading mode selection
        ttk.Label(controls_frame, text="Reading Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="page")
        mode_frame = ttk.Frame(controls_frame)
        mode_frame.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Radiobutton(mode_frame, text="Page Turn", variable=self.mode_var, 
                       value="page").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="Auto-scroll", variable=self.mode_var,
                       value="scroll").grid(row=0, column=1, padx=5)
        
        # Speed control
        ttk.Label(controls_frame, text="Scroll Speed:").grid(row=1, column=0, padx=5, pady=5)
        self.speed_scale = ttk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Navigation buttons
        nav_frame = ttk.Frame(controls_frame)
        nav_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.prev_btn = ttk.Button(nav_frame, text="Previous Page", command=self.prev_page)
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = ttk.Button(nav_frame, text="Play/Pause", command=self.toggle_scroll)
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.next_btn = ttk.Button(nav_frame, text="Next Page", command=self.next_page)
        self.next_btn.grid(row=0, column=2, padx=5)

    def add_books(self):
        files = filedialog.askopenfilenames(
            title="Select Books",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        for file in files:
            filename = Path(file).name
            self.book_list.insert(tk.END, filename)

    def prev_page(self):
        # TODO: Implement previous page functionality
        pass

    def next_page(self):
        # TODO: Implement next page functionality
        pass

    def toggle_scroll(self):
        # TODO: Implement auto-scroll toggle
        pass

def main():
    root = tk.Tk()
    app = BookBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
