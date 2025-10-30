# Gomoku AI vs AI

Two AI agents play Gomoku (Five in a Row) against each other using Ollama's extended thinking models.

## Features

- 6x6 Gomoku board (configurable in code)
- Two AI agents powered by Ollama using `gpt-oss:20b` with extended thinking capabilities
- Real-time streaming of AI thinking process
- Terminal-based board display after each move
- Automatic win detection (5 in a row)
- Strategic AI play with:
  - Immediate winning move detection
  - Defensive blocking of opponent's winning moves
  - LLM-powered strategic decision-making for complex situations
  - Move validation and fallback strategies

## Requirements

- Python 3.7+
- Ollama installed and running locally
- `gpt-oss:20b` model downloaded in Ollama (or any other extended thinking model)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Ensure you have the gpt-oss model downloaded:
```bash
ollama pull gpt-oss:20b
```

## Usage

Run the game:
```bash
python main.py
```

The game will:
- Display the initial empty board
- Show each AI's thinking process in real-time (streamed output)
- Display each AI's move with coordinates
- Update and display the board after each move
- Announce the winner when someone gets 5 in a row
- End in a draw if the board fills up or max moves (100) is reached

## Customization

### Change AI Model

To use a different Ollama model, edit `main.py` and change:
```python
player1 = GomokuAI("AI Player 1", "X", model="your-model-name")
player2 = GomokuAI("AI Player 2", "O", model="your-model-name")
```

### Adjust Board Size

In `main.py`, modify the `BOARD_SIZE` variable:
```python
BOARD_SIZE = 6  # Change to desired size (e.g., 10, 15, etc.)
```

## Game Rules

- Players alternate placing stones on the board
- Player 1 (X) goes first
- First player to get 5 stones in a row (horizontally, vertically, or diagonally) wins
- If the board fills up without a winner, the game is a draw

## Files

- `main.py` - Main game loop with configurable board size and AI setup
- `gomoku_board.py` - Board implementation with game logic, win detection, and move validation
- `ai_agent.py` - AI agent using Ollama API with:
  - Streaming support for extended thinking models
  - Strategic move detection (winning/blocking)
  - LLM-powered decision making
  - Robust error handling and fallback strategies
- `requirements.txt` - Python dependencies (requests library)

## AI Strategy

The AI uses a hybrid approach:

1. **Tactical Priority**: First checks for immediate winning moves or blocking requirements
2. **Strategic Thinking**: Uses LLM reasoning for complex board positions
3. **Fallback Logic**: Smart position selection near existing stones if LLM fails

## Extended Thinking Models

This implementation leverages Ollama's extended thinking capabilities, which:
- Show real-time reasoning process through streaming
- Allow models to "think through" complex game positions
- Provide more strategic and thoughtful gameplay
