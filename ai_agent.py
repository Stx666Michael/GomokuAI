"""AI agent for playing Gomoku using Ollama."""

import requests
import json
import re


class GomokuAI:
    """AI agent that uses Ollama's model to play Gomoku."""
    
    def __init__(self, name, player_symbol, model="gpt-oss:20b"):
        """Initialize the AI agent.
        
        Args:
            name: Name of the AI agent
            player_symbol: Symbol for this player ('X' or 'O')
            model: Ollama model to use (default: gpt-oss:20b)
        """
        self.name = name
        self.player_symbol = player_symbol
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def get_move(self, board):
        """Get the next move from the AI.
        
        Args:
            board: GomokuBoard instance
            
        Returns:
            Tuple (row, col) for the next move, or None if no valid move
        """
        # Get empty positions
        empty_positions = board.get_empty_positions()
        
        if not empty_positions:
            return None
        
        # First, check for immediate winning move
        winning_move = self._find_winning_move(board, self.player_symbol, empty_positions)
        if winning_move:
            print(f"[STRATEGY] Found winning move!")
            return winning_move
        
        # Second, check if we need to block opponent's winning move
        opponent = 'O' if self.player_symbol == 'X' else 'X'
        blocking_move = self._find_winning_move(board, opponent, empty_positions)
        if blocking_move:
            print(f"[STRATEGY] Blocking opponent's winning move!")
            return blocking_move
        
        # If no immediate tactical move, use LLM for strategic decision
        # Create a simple board representation for the AI
        board_str = self._format_board_for_ai(board)
        
        # Create prompt for the AI
        prompt = self._create_prompt(board, board_str)
        
        # Debug: Print prompt length
        print(f"[DEBUG] Prompt length: {len(prompt)} characters")
        
        # Get response from Ollama
        move = self._query_ollama(prompt, board, empty_positions)
        
        return move
    
    def _format_board_for_ai(self, board):
        """Format the board in a readable way for the AI.
        
        Args:
            board: GomokuBoard instance
            
        Returns:
            String representation of the board
        """
        result = "Current board state:\n"
        result += "   "
        for i in range(board.size):
            result += f"{i:2} "
        result += "\n"
        
        for i in range(board.size):
            result += f"{i:2} "
            for j in range(board.size):
                cell = board.board[i][j]
                result += f" {cell} "
            result += "\n"
        
        return result
    
    def _create_prompt(self, board, board_str):
        """Create a prompt for the AI model.
        
        Args:
            board: GomokuBoard instance
            board_str: Formatted board string
            
        Returns:
            Prompt string
        """
        opponent = 'O' if self.player_symbol == 'X' else 'X'
        
        # Get empty positions for the prompt
        empty_positions = board.get_empty_positions()
        
        # Get recent moves for context
        recent_moves = ""
        if board.move_history:
            recent_moves = "\nRecent moves:\n"
            for i, (r, c, p) in enumerate(board.move_history[-5:]):
                recent_moves += f"Move {len(board.move_history) - 5 + i + 1}: Player {p} at ({r},{c})\n"
        
        # Show some example valid moves
        example_moves = ""
        if len(empty_positions) > 0:
            examples = empty_positions[:min(10, len(empty_positions))]
            example_moves = "\nSome available positions: " + ", ".join([f"({r},{c})" for r, c in examples])
        
        prompt = f"""You are an expert Gomoku player. You play as '{self.player_symbol}' and your opponent plays as '{opponent}'.

{board_str}{recent_moves}{example_moves}

GAME RULES:
- Board size: {board.size}x{board.size}
- Win condition: Get 5 of your stones in a row (horizontal, vertical, or diagonal)
- '{self.player_symbol}' = your stones, '{opponent}' = opponent's stones, ' ' (space) = empty cells

CRITICAL: You can ONLY place your stone on EMPTY cells (marked with space ' ').
DO NOT choose positions that already have '{self.player_symbol}' or '{opponent}'.

STRATEGY:
1. Try to create or extend your own lines of stones
2. Block opponent's lines if they're getting close to 5
3. Choose empty positions near existing stones for better chances

IMPORTANT: Respond with ONLY row,col of an EMPTY position.
Format: row,col (e.g., "5,3" or "0,0")

NOTE: If you have a thinking process, try to make it as concise as possible.

Choose an empty position:"""
        
        return prompt
    
    def _query_ollama(self, prompt, board, empty_positions):
        """Query the Ollama API for a move.
        
        Args:
            prompt: The prompt to send to the AI
            board: GomokuBoard instance
            empty_positions: List of valid empty positions
            
        Returns:
            Tuple (row, col) for the move
        """
        try:
            # Query Ollama with streaming enabled
            print(f"[DEBUG] Sending request to Ollama with model: {self.model}")
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,  # Enable streaming
                    "options": {
                        #"temperature": 0.3,
                        #"top_k": 10,
                        #"top_p": 0.9,
                    }
                },
                timeout=60,
                stream=True  # Enable streaming in requests
            )
            
            print(f"[DEBUG] Received streaming response with status: {response.status_code}")
            
            if response.status_code == 200:
                # Collect the streamed response
                thinking_parts = []
                response_parts = []
                last_result = {}
                
                print("[AI THINKING] ", end="", flush=True)
                
                # Process the stream
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            last_result = chunk
                            
                            # Stream thinking field
                            if "thinking" in chunk and chunk["thinking"]:
                                thinking_parts.append(chunk["thinking"])
                                print(chunk["thinking"], end="", flush=True)
                            
                            # Collect response field
                            if "response" in chunk and chunk["response"]:
                                response_parts.append(chunk["response"])
                                
                        except json.JSONDecodeError:
                            continue
                
                print()  # New line after thinking
                
                # Combine all parts
                full_thinking = "".join(thinking_parts)
                ai_response = "".join(response_parts).strip()
                
                # Debug: Print the full AI response and metadata
                print(f"[DEBUG] AI raw response: '{ai_response}'")
                print(f"[DEBUG] Response metadata: done={last_result.get('done')}, done_reason={last_result.get('done_reason')}")
                
                # Check if response is empty and log additional info
                if not ai_response:
                    print(f"[DEBUG] Empty response after streaming")
                
                # Parse the response
                move = self._parse_move(ai_response, empty_positions)
                
                if move:
                    return move
                else:
                    print(f"{self.name} generated invalid move: {ai_response}, choosing strategic fallback")
                    return self._get_strategic_fallback(board, empty_positions)
            else:
                print(f"[ERROR] Ollama API error: {response.status_code}")
                print(f"[ERROR] Response: {response.text}")
                return self._get_strategic_fallback(board, empty_positions)
                
        except requests.exceptions.Timeout as e:
            print(f"[ERROR] Timeout when querying Ollama: {e}")
            return self._get_strategic_fallback(board, empty_positions)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request exception when querying Ollama: {e}")
            return self._get_strategic_fallback(board, empty_positions)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON decode error: {e}")
            print(f"[ERROR] Raw response text: {response.text if 'response' in locals() else 'N/A'}")
            return self._get_strategic_fallback(board, empty_positions)
        except Exception as e:
            print(f"[ERROR] Unexpected exception when querying Ollama: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to strategic position
            return self._get_strategic_fallback(board, empty_positions)
    
    def _parse_move(self, response, empty_positions):
        """Parse the AI's response to extract the move.
        
        Args:
            response: The AI's response string
            empty_positions: List of valid empty positions
            
        Returns:
            Tuple (row, col) if valid, None otherwise
        """
        if not response:
            print(f"[DEBUG] Empty response received")
            return None
            
        print(f"[DEBUG] Parsing response: '{response[:200]}'")  # Show first 200 chars
        
        # Try to find numbers in the format "row,col" or "row, col"
        patterns = [
            r'(\d+)\s*,\s*(\d+)',  # Match "row,col" or "row, col"
            r'row\s*[:=]?\s*(\d+).*col(?:umn)?\s*[:=]?\s*(\d+)',  # Match "row: 5, column: 3"
            r'\((\d+)\s*,\s*(\d+)\)',  # Match "(row, col)"
            r'(\d+)\s+(\d+)',  # Match "row col" with space
        ]
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                try:
                    row = int(match.group(1))
                    col = int(match.group(2))
                    
                    print(f"[DEBUG] Pattern {i} matched: ({row}, {col})")
                    
                    # Verify the move is valid
                    if (row, col) in empty_positions:
                        print(f"[DEBUG] Valid move found: ({row}, {col})")
                        return (row, col)
                    else:
                        print(f"[DEBUG] Move ({row}, {col}) not in empty positions")
                except (ValueError, IndexError) as e:
                    print(f"[DEBUG] Error parsing match: {e}")
                    continue
        
        print(f"[DEBUG] No valid move found in response")
        return None
    
    def _find_winning_move(self, board, player, empty_positions):
        """Find a winning move for the specified player.
        
        Args:
            board: GomokuBoard instance
            player: Player symbol to check for winning moves
            empty_positions: List of empty positions
            
        Returns:
            Tuple (row, col) if a winning move exists, None otherwise
        """
        # Try each empty position
        for row, col in empty_positions:
            # Temporarily place the stone
            board.board[row][col] = player
            
            # Check if this creates a win
            if board.check_winner(row, col, player):
                # Remove the temporary stone
                board.board[row][col] = ' '
                return (row, col)
            
            # Remove the temporary stone
            board.board[row][col] = ' '
        
        return None
    
    def _get_strategic_fallback(self, board, empty_positions):
        """Get a strategic fallback move when LLM fails.
        
        Args:
            board: GomokuBoard instance
            empty_positions: List of valid empty positions
            
        Returns:
            Tuple (row, col) for a strategic position
        """
        if not empty_positions:
            return None
        
        # Strategy 1: If board is empty, play center
        if len(empty_positions) == board.size * board.size:
            center = board.size // 2
            return (center, center)
        
        # Strategy 2: Find positions adjacent to existing stones (more strategic)
        adjacent_positions = []
        for row, col in empty_positions:
            # Check if this position is adjacent to any existing stone
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < board.size and 0 <= nc < board.size:
                        if board.board[nr][nc] != ' ':
                            adjacent_positions.append((row, col))
                            break
                if (row, col) in adjacent_positions:
                    break
        
        # If we found adjacent positions, pick one (preferably near center)
        if adjacent_positions:
            center = board.size // 2
            # Sort by distance to center
            adjacent_positions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
            return adjacent_positions[0]
        
        # Strategy 3: Fallback to center area
        center = board.size // 2
        empty_positions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
        return empty_positions[0]
