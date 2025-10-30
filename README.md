# Gomoku AI vs AI

Two AI agents play Gomoku (Five in a Row) against each other using Ollama's Gemma models.

## Features

- 10x10 Gomoku board
- Two AI agents powered by Ollama (using gemma2:2b model)
- Terminal-based board display after each move
- Automatic win detection (5 in a row)
- Strategic AI play with move validation

## Requirements

- Python 3.7+
- Ollama installed and running locally
- Gemma2:2b model downloaded in Ollama (or change to gemma3:12b in code)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Ensure you have the Gemma model downloaded:
```bash
ollama pull gemma2:2b
# or
ollama pull gemma3:12b
```

## Usage

Run the game:
```bash
python main.py
```

The game will:
- Display the initial empty board
- Show each AI's move with coordinates
- Update and display the board after each move
- Announce the winner when someone gets 5 in a row
- End in a draw if the board fills up

## Customization

To use gemma3:12b instead of gemma2:2b, edit `main.py` and change:
```python
player1 = GomokuAI("AI Player 1", "X", model="gemma3:12b")
player2 = GomokuAI("AI Player 2", "O", model="gemma3:12b")
```

## Game Rules

- Players alternate placing stones on the board
- Player 1 (X) goes first
- First player to get 5 stones in a row (horizontally, vertically, or diagonally) wins
- If the board fills up without a winner, the game is a draw

## Files

- `main.py` - Main game loop
- `gomoku_board.py` - Board implementation with game logic
- `ai_agent.py` - AI agent using Ollama API
- `requirements.txt` - Python dependencies
