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
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Initialize reading state
        self.current_text = ""
        self.current_position = 0
        self.page_size = 2000  # Characters per page
        self.auto_scroll_id = None
        self.page_turn_id = None
        self.is_scrolling = False
        
        self.setup_book_selection()
        self.setup_reading_area()
        self.setup_controls()

        self.root.bind('<Configure>', self.on_window_resize)
        
        # Bind global keyboard shortcuts
        self.root.bind('<space>', lambda e: self.toggle_scroll())
        self.root.bind('<Left>', lambda e: self.prev_page())    # Left arrow for previous page
        self.root.bind('<Right>', lambda e: self.next_page())   # Right arrow for next page
        self.root.bind('<Up>', lambda e: self.adjust_speed(1))  # Up arrow to increase speed
        self.root.bind('<Down>', lambda e: self.adjust_speed(-1))  # Down arrow to decrease speed

    def setup_book_selection(self):
        # Book selection frame
        selection_frame = ttk.LabelFrame(self.main_container, text="Book Selection", padding="5")
        selection_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Add book button
        self.add_btn = ttk.Button(selection_frame, text="Add Books", command=self.add_books)
        self.add_btn.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Book list
        self.book_list = tk.Listbox(selection_frame, selectmode=tk.SINGLE, height=6)
        self.book_list.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.book_list.bind('<<ListboxSelect>>', self.on_book_select)
        
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
        
        # Bind manual scroll events
        self.text_area.bind('<MouseWheel>', self.on_manual_scroll)  # Windows
        self.text_area.bind('<Button-4>', self.on_manual_scroll)    # Linux scroll up
        self.text_area.bind('<Button-5>', self.on_manual_scroll)    # Linux scroll down
        self.text_area.bind('<B1-Motion>', self.on_manual_scroll)   # Scrollbar drag
        
        # Bind keyboard scroll events
        self.text_area.bind('<Prior>', self.on_manual_scroll)       # Page Up
        self.text_area.bind('<Next>', self.on_manual_scroll)        # Page Down
        self.text_area.bind('<Up>', self.on_manual_scroll)          # Up arrow
        self.text_area.bind('<Down>', self.on_manual_scroll)        # Down arrow
        
        # Bind space bar for play/pause
        self.text_area.bind('<space>', lambda e: (self.toggle_scroll(), 'break'))
        
        # Scrollbar for text area
        text_scroll = ttk.Scrollbar(reading_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        text_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_scroll.bind('<B1-Motion>', self.on_manual_scroll)
        self.text_area.configure(yscrollcommand=text_scroll.set)

    def setup_controls(self):
        # Controls frame
        controls_frame = ttk.LabelFrame(self.main_container, text="Reading Controls", padding="5")
        controls_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Auto modes frame
        auto_frame = ttk.Frame(controls_frame)
        auto_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        # Auto-scroll toggle
        self.auto_scroll_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(auto_frame, text="Auto-scroll", 
                       variable=self.auto_scroll_var,
                       command=self.update_auto_modes).grid(row=0, column=0, padx=5)
        
        # Auto page turn toggle
        self.auto_page_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(auto_frame, text="Auto Page Turn",
                       variable=self.auto_page_var,
                       command=self.update_auto_modes).grid(row=0, column=1, padx=5)
        
        # Speed control
        speed_frame = ttk.Frame(controls_frame)
        speed_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Label(speed_frame, text="Speed:").grid(row=0, column=0, padx=5)
        self.speed_scale = ttk.Scale(speed_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.set(5)  # Default speed
        self.speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        # Update on both drag and release for responsive speed changes
        self.speed_scale.bind('<B1-Motion>', self.on_speed_change)     # During drag
        self.speed_scale.bind('<ButtonRelease-1>', self.on_speed_change)  # On release
        
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
            self.book_list.insert(tk.END, file)

    def on_book_select(self, event):
        selection = self.book_list.curselection()
        if selection:
            if self.auto_scroll_var.get():
                self.auto_scroll_var.set(False)
                self.auto_page_var.set(False)
                self.update_auto_modes()
                
            file_path = self.book_list.get(selection[0])
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.current_text = file.read()
                    self.current_position = 0
                    self.display_current_page()
            except Exception as e:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', f"Error reading file: {str(e)}")

    def display_current_page(self):
        start = self.current_position
        end = start + self.page_size
        if end > len(self.current_text):
            end = len(self.current_text)
        
        current_page = self.current_text[start:end]
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', current_page)
        
        # Update button states
        self.prev_btn['state'] = 'normal' if start > 0 else 'disabled'
        self.next_btn['state'] = 'normal' if end < len(self.current_text) else 'disabled'

    def prev_page(self):
        if self.current_position > 0:
            if self.auto_scroll_var.get():
                self.auto_scroll_var.set(False)
                self.auto_page_var.set(False)
                self.update_auto_modes()
            self.current_position = max(0, self.current_position - self.page_size)
            self.display_current_page()

    def next_page(self):
        if self.current_position + self.page_size < len(self.current_text):
            if self.auto_scroll_var.get():
                self.auto_scroll_var.set(False)
                self.auto_page_var.set(False)
                self.update_auto_modes()
            self.current_position += self.page_size
            self.display_current_page()

    def calculate_scroll_params(self):
        """Calculate scroll parameters based on content and speed"""
        speed = self.speed_scale.get()  # 1-10
        chars_per_minute = speed * 200 
        current_page = self.text_area.get('1.0', 'end-1c')
        char_count = len(current_page)
        
        try:
            total_scroll_time = (char_count / chars_per_minute) * 60  # seconds
            viewport_height = self.text_area.winfo_height()
            self.text_area.update_idletasks()
            line_info = self.text_area.dlineinfo('1.0')
            if line_info:
                line_height = line_info[3]
                num_lines = int(self.text_area.index('end-1c').split('.')[0])
                content_height = num_lines * line_height
            else:
                content_height = viewport_height
                
            total_height = max(viewport_height, content_height)
            
            # Calculate pixels per second for smooth scrolling
            # Ensure minimum scroll speed for very large content
            min_scroll_time = 20  # Maximum 20 seconds per page
            total_scroll_time = min(total_scroll_time, min_scroll_time)
            pixels_per_second = total_height / total_scroll_time
            min_pixels_per_interval = 1
            pixels_per_interval = max(pixels_per_second * 0.05, min_pixels_per_interval)
            
            return {
                'scroll_interval': 50,
                'pixels_per_interval': pixels_per_interval,
                'total_time': int(total_scroll_time * 1000)
            }
            
        except Exception as e:
            # Fallback to basic scroll parameters if calculations fail
            return {
                'scroll_interval': 50,
                'pixels_per_interval': 1,
                'total_time': 10000
            }

    def calculate_delay(self, text):
        """Calculate delay time based on content and speed"""
        char_count = len(text)
        speed = self.speed_scale.get()
        return min(max(int((char_count / (speed * 20)) * 1000), 3000), 10000)

    def calculate_bottom_delay(self):
        """Calculate delay time for bottom of page based on content and speed"""
        current_page = self.text_area.get('1.0', 'end-1c')
        last_paragraph = current_page.split('\n\n')[-1] if '\n\n' in current_page else current_page[-500:]
        return self.calculate_delay(last_paragraph)

    def schedule_page_turn(self):
        """Schedule page turn with current delay"""
        if hasattr(self, 'page_turn_id') and self.page_turn_id is not None:
            try:
                self.root.after_cancel(self.page_turn_id)
            except ValueError:
                pass
        delay = self.calculate_bottom_delay()
        self.page_turn_id = self.root.after(delay, self.handle_page_turn)

    def auto_scroll(self):
        if not self.auto_scroll_var.get():
            return
            
        current_pos = self.text_area.yview()[1]
        
        if current_pos >= 1.0:
            if self.auto_page_var.get():
                self.schedule_page_turn()
            else:
                self.auto_scroll_var.set(False)
                self.update_auto_modes()
            return

        if current_pos == 0.0 and not hasattr(self, 'scroll_params'):
            current_page = self.text_area.get('1.0', 'end-1c')
            first_paragraph = current_page.split('\n\n')[0] if '\n\n' in current_page else current_page[:500]
            delay = self.calculate_delay(first_paragraph)
            self.auto_scroll_id = self.root.after(delay, self.auto_scroll)
            return
            
        if not hasattr(self, 'scroll_params'):
            self.scroll_params = self.calculate_scroll_params()
            
        self.text_area.yview_scroll(int(self.scroll_params['pixels_per_interval']), 'pixels')
        
        self.auto_scroll_id = self.root.after(
            self.scroll_params['scroll_interval'], 
            self.auto_scroll
        )

    def handle_page_turn(self):
        """Handle turning to the next page after reaching bottom"""
        self.page_turn_id = None
        
        if self.auto_page_var.get():
            self.next_page()
            self.text_area.yview_moveto(0)
            if hasattr(self, 'scroll_params'):
                delattr(self, 'scroll_params')
            self.auto_scroll_var.set(True)
            self.auto_scroll()

    def update_auto_modes(self):
        if self.auto_scroll_id:
            try:
                self.root.after_cancel(self.auto_scroll_id)
            except ValueError:
                pass
            self.auto_scroll_id = None
            
        if hasattr(self, 'page_turn_id') and self.page_turn_id is not None:
            try:
                self.root.after_cancel(self.page_turn_id)
            except ValueError:
                pass
            self.page_turn_id = None
        
        if hasattr(self, 'scroll_params'):
            delattr(self, 'scroll_params')
        
        if self.auto_scroll_var.get() or self.auto_page_var.get():
            self.play_btn.configure(text="Pause")
        else:
            self.play_btn.configure(text="Play")
        
        if self.auto_scroll_var.get():
            self.auto_scroll()

    def on_window_resize(self, event):
        """Handle window resize events"""
        if (event.widget == self.root and 
            (event.width != self.root.winfo_width() or 
             event.height != self.root.winfo_height()) and
            hasattr(self, 'scroll_params')):
            self.root.update_idletasks()
            delattr(self, 'scroll_params')
            if self.auto_scroll_var.get():
                self.auto_scroll()

    def adjust_speed(self, delta):
        """Adjust reading speed by the given delta"""
        current = self.speed_scale.get()
        new_speed = min(max(current + delta, 1), 10)
        if new_speed != current:
            self.speed_scale.set(new_speed)
            self.on_speed_change(None)

    def on_speed_change(self, event):
        """Handle speed slider changes"""
        if hasattr(self, 'scroll_params'):
            delattr(self, 'scroll_params')
            if self.auto_scroll_var.get():
                if self.text_area.yview()[1] >= 1.0 and self.auto_page_var.get():
                    self.schedule_page_turn()
                else:
                    self.auto_scroll()

    def on_manual_scroll(self, event):
        """Handle manual scrolling while auto-scroll is active"""
        if not self.auto_scroll_var.get():
            return
            
        if (hasattr(event, 'delta') or
            hasattr(event, 'num') or
            event.type == tk.EventType.Motion or
            event.type == tk.EventType.KeyPress
        ):
            self.auto_scroll_var.set(False)
            self.auto_page_var.set(False)
            self.update_auto_modes()

    def toggle_scroll(self):
        current_state = self.auto_scroll_var.get() or self.auto_page_var.get()
        self.auto_scroll_var.set(not current_state)
        self.auto_page_var.set(not current_state)
        self.update_auto_modes()

    def cleanup(self):
        """Clean up resources and event bindings"""
        if self.auto_scroll_id:
            try:
                self.root.after_cancel(self.auto_scroll_id)
            except ValueError:
                pass
            self.auto_scroll_id = None
            
        if hasattr(self, 'page_turn_id') and self.page_turn_id is not None:
            try:
                self.root.after_cancel(self.page_turn_id)
            except ValueError:
                pass
            self.page_turn_id = None

        self.current_text = ""
        if hasattr(self, 'scroll_params'):
            delattr(self, 'scroll_params')

        self.root.unbind('<Configure>')
        self.root.unbind('<space>')
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        
        self.text_area.unbind('<MouseWheel>')
        self.text_area.unbind('<Button-4>')
        self.text_area.unbind('<Button-5>')
        self.text_area.unbind('<B1-Motion>')
        self.text_area.unbind('<Prior>')
        self.text_area.unbind('<Next>')
        self.text_area.unbind('<Up>')
        self.text_area.unbind('<Down>')
        self.text_area.unbind('<space>')
        
        self.speed_scale.unbind('<B1-Motion>')
        self.speed_scale.unbind('<ButtonRelease-1>')
        
        self.book_list.unbind('<<ListboxSelect>>')

    def on_close(self):
        """Handle window close event"""
        if self.auto_scroll_var.get():
            self.auto_scroll_var.set(False)
            self.auto_page_var.set(False)
            self.update_auto_modes()
        
        # Clean up resources before destroying the window
        self.cleanup()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = BookBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
