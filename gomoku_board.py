"""Gomoku game board implementation."""


class GomokuBoard:
    """Represents a Gomoku game board."""
    
    def __init__(self, size=10):
        """Initialize the board.
        
        Args:
            size: Board size (default 10x10)
        """
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.move_history = []
        
    def display(self):
        """Display the board in the terminal."""
        print("\n   ", end="")
        for i in range(self.size):
            print(f"{i:2}", end=" ")
        print("\n   " + "---" * self.size)
        
        for i in range(self.size):
            print(f"{i:2}|", end="")
            for j in range(self.size):
                print(f" {self.board[i][j]} ", end="")
            print("|")
        print("   " + "---" * self.size)
    
    def is_valid_move(self, row, col):
        """Check if a move is valid.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if the move is valid, False otherwise
        """
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        return self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        """Place a stone on the board.
        
        Args:
            row: Row index
            col: Column index
            player: Player symbol ('X' or 'O')
            
        Returns:
            True if the move was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        self.move_history.append((row, col, player))
        return True
    
    def check_winner(self, row, col, player):
        """Check if the last move resulted in a win.
        
        Args:
            row: Row index of the last move
            col: Column index of the last move
            player: Player symbol
            
        Returns:
            True if the player won, False otherwise
        """
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal \
            (1, -1)   # Diagonal /
        ]
        
        for dr, dc in directions:
            count = 1  # Count the current stone
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
    
    def is_full(self):
        """Check if the board is full.
        
        Returns:
            True if the board is full, False otherwise
        """
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def get_board_state(self):
        """Get the current board state as a string.
        
        Returns:
            String representation of the board
        """
        state = ""
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == ' ':
                    state += f"({i},{j}):empty "
                else:
                    state += f"({i},{j}):{cell} "
        return state.strip()
    
    def get_empty_positions(self):
        """Get all empty positions on the board.
        
        Returns:
            List of tuples (row, col) for empty positions
        """
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    empty.append((i, j))
        return empty
