# BookBot

A versatile book reading application with multiple interfaces:

## Components

### main.py
Boot.dev course.

### bookbot_gui.py
A graphical user interface (GUI) version using ttk widgets that provides:
- Multiple book selection
- Reading interface with page turning
- Auto-scroll functionality
- Speed control
- Modern styling with ttk theme
(Requires X11/display server)

### bookbot_reader.py
A terminal-based (CLI) reader that works in all environments:
- Navigate books using arrow keys
- Toggle between page-turn and auto-scroll modes
- Adjustable scroll speed
- Works in any terminal environment
- No external dependencies beyond Python standard library

## Usage

For word/character analysis:
```bash
python3 main.py
```

For GUI interface (requires display server):
```bash
python3 bookbot_gui.py
```

For terminal reader:
```bash
python3 bookbot_reader.py
```

Place your .txt books in the `books/` directory to make them available to all interfaces.
