# BookBot Enhancement Plan

## Features to Implement

### GUI Interface (bookbot_gui.py)
- [x] Create main window with ttk styling
- [x] Add book selection interface
  - [x] Allow multiple book selection
  - [x] Display book titles
  - [x] Show word count for each selected book

### Terminal Interface (bookbot_reader.py)
- [x] Create terminal-based UI using curses
- [x] Implement book selection menu
- [x] Display book content in terminal
- [x] Add navigation controls

### Book Management
- [x] Implement local book reading
- [x] Display book titles
- [ ] Implement book fetching from Project Gutenberg
  - [ ] Add search functionality
  - [ ] Download and cache books locally
- [ ] Display additional metadata (author, etc.)

### Reading Interface
- [x] Create text display area
  - [x] Implement page turning mode
  - [x] Add auto-scrolling mode
  - [x] Add speed control
- [x] Add reading progress through pagination
- [x] Implement basic text display

### Settings
- [x] Add mode toggle (page turn vs auto-scroll)
- [x] Create speed control
- [ ] Save user preferences

## Technical Tasks
- [x] Refactor existing code into modular structure
- [x] Create book management class
- [x] Implement text processing utilities
- [ ] Add configuration management
- [x] Create UI layout manager (both GUI and Terminal)
- [x] Implement event handlers for user interactions
