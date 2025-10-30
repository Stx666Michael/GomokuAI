"""Main game loop for Gomoku AI vs AI."""

import time
from gomoku_board import GomokuBoard
from ai_agent import GomokuAI


def main():
    """Run a game of Gomoku between two AI agents."""
    BOARD_SIZE = 6
    print("=" * 50)
    print("GOMOKU AI vs AI")
    print("=" * 50)
    print("\nTwo AI agents will play Gomoku against each other.")
    print(f"Board size: {BOARD_SIZE}x{BOARD_SIZE}")
    print("Win condition: 5 in a row")
    print("\n" + "=" * 50 + "\n")
    
    # Initialize the board
    board = GomokuBoard(size=BOARD_SIZE)
    
    # Initialize AI players
    player1 = GomokuAI("AI Player 1", "X", model="gpt-oss:20b")
    player2 = GomokuAI("AI Player 2", "O", model="gpt-oss:20b")
    
    # Game state
    current_player = player1
    move_count = 0
    max_moves = 100  # Prevent infinite games
    
    print("Starting game...\n")
    time.sleep(1)
    
    # Display initial empty board
    print("Initial board:")
    board.display()
    print()
    
    # Game loop
    while move_count < max_moves:
        move_count += 1
        
        print(f"\n{'=' * 50}")
        print(f"Move {move_count}: {current_player.name} ({current_player.player_symbol})")
        print('=' * 50)
        
        # Get move from current player
        print(f"{current_player.name} is thinking...")
        move = current_player.get_move(board)
        
        if move is None:
            print("No valid moves available. Game is a draw!")
            break
        
        row, col = move
        print(f"{current_player.name} plays at position ({row}, {col})")
        
        # Make the move
        if not board.make_move(row, col, current_player.player_symbol):
            print(f"Invalid move by {current_player.name}! Game ends.")
            break
        
        # Display the board
        board.display()
        
        # Check for winner
        if board.check_winner(row, col, current_player.player_symbol):
            print(f"\n{'=' * 50}")
            print(f"🎉 {current_player.name} ({current_player.player_symbol}) WINS! 🎉")
            print(f"{'=' * 50}")
            print(f"\nGame ended after {move_count} moves.")
            return
        
        # Check for draw
        if board.is_full():
            print(f"\n{'=' * 50}")
            print("Game is a DRAW! Board is full.")
            print(f"{'=' * 50}")
            return
        
        # Switch players
        current_player = player2 if current_player == player1 else player1
        
        # Small delay for readability
        time.sleep(0.5)
    
    print(f"\n{'=' * 50}")
    print(f"Game ended after {max_moves} moves (maximum reached).")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
