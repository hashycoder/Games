import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 5
SYMBOL_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        # Game state
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def draw_grid(self):
        """Draw the tic-tac-toe grid"""
        # Draw horizontal lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, 
                           (0, i * CELL_SIZE), 
                           (WINDOW_SIZE, i * CELL_SIZE), 
                           LINE_WIDTH)
        
        # Draw vertical lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, 
                           (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, WINDOW_SIZE), 
                           LINE_WIDTH)
    
    def draw_symbols(self):
        """Draw X's and O's on the board"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(row, col)
    
    def draw_x(self, row, col):
        """Draw an X in the specified cell"""
        start_x = col * CELL_SIZE + 50
        start_y = row * CELL_SIZE + 50
        end_x = (col + 1) * CELL_SIZE - 50
        end_y = (row + 1) * CELL_SIZE - 50
        
        pygame.draw.line(self.screen, RED, (start_x, start_y), (end_x, end_y), 8)
        pygame.draw.line(self.screen, RED, (start_x, end_y), (end_x, start_y), 8)
    
    def draw_o(self, row, col):
        """Draw an O in the specified cell"""
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 50
        
        pygame.draw.circle(self.screen, BLUE, (center_x, center_y), radius, 8)
    
    def get_cell_from_mouse(self, mouse_pos):
        """Convert mouse position to grid coordinates"""
        x, y = mouse_pos
        if y > WINDOW_SIZE:  # Click is in the status area
            return None, None
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row, col
    
    def make_move(self, row, col):
        """Make a move if the cell is empty"""
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Tie'
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return True
        
        # Check columns
        for col in range(GRID_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def draw_status(self):
        """Draw the current game status"""
        status_y = WINDOW_SIZE + 20
        
        if self.game_over:
            if self.winner == 'Tie':
                text = "It's a Tie!"
                color = GRAY
            else:
                text = f"Player {self.winner} Wins!"
                color = RED if self.winner == 'X' else BLUE
            
            status_text = self.font.render(text, True, color)
            text_rect = status_text.get_rect(center=(WINDOW_SIZE // 2, status_y))
            self.screen.blit(status_text, text_rect)
            
            # Draw reset instruction
            reset_text = self.small_font.render("Press SPACE to play again", True, BLACK)
            reset_rect = reset_text.get_rect(center=(WINDOW_SIZE // 2, status_y + 50))
            self.screen.blit(reset_text, reset_rect)
        else:
            text = f"Player {self.current_player}'s Turn"
            color = RED if self.current_player == 'X' else BLUE
            status_text = self.font.render(text, True, color)
            text_rect = status_text.get_rect(center=(WINDOW_SIZE // 2, status_y))
            self.screen.blit(status_text, text_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        row, col = self.get_cell_from_mouse(event.pos)
                        if row is not None and col is not None:
                            self.make_move(row, col)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_symbols()
            self.draw_status()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.run()