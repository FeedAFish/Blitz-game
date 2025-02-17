# Blitz Game Collection

A collection of classic games built with Pygame including Snake, Tic-Tac-Toe, 2048 and Lines.

## Features

- Multiple game modes
- Interactive UI with hovering effects
- Auto-updating system
- Error logging
- Cross-platform support

## Prerequisites

- Python 3.10+
- Pygame
- Docker (optional)

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Blitz-game.git
cd Blitz-game

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Docker Support
```bash
# Build image
docker build -t blitz-game .

# Run container
docker run --rm -e DISPLAY=host.docker.internal:0 blitz-game
```
### Development Setup

- Install VcXsrv (Windows) or X11 (Linux)
- Configure display settings
- Run the development server

## Error Handling
Errors are logged to error.log with timestamps for debugging.

## Updates & Changelog

### Version 0.2
- Added new game modes
- Improved UI interactions
- Fixed audio issues
- Enhanced error logging

### Version 0.3
- Added 2048
- Remove XO game for furthur dev.

### Version 0.4
- Added Animal game with basic mechanics of 7 levels

### Version 0.5
- Add Bejeweled Diamond Game