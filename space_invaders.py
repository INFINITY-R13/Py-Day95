import tkinter as tk
import random

class SpaceInvaders:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.move_player(-20))
        self.root.bind('<Right>', lambda e: self.move_player(20))
        self.root.bind('<space>', lambda e: self.shoot())
        self.root.bind('r', lambda e: self.restart() if self.game_over else None)
        
        self.reset_game()
        self.game_loop()
    
    def reset_game(self):
        self.canvas.delete('all')
        
        self.score = 0
        self.game_over = False
        
        # Player
        self.player_x = 375
        self.player_y = 550
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y, 
            self.player_x + 50, self.player_y + 30, 
            fill='green'
        )
        
        # Aliens
        self.aliens = []
        self.alien_direction = 5
        self.create_aliens()
        
        # Bullets
        self.bullets = []
        
        # Score display
        self.score_text = self.canvas.create_text(
            50, 20, text=f"Score: {self.score}", 
            fill='white', font=('Arial', 16)
        )
    
    def create_aliens(self):
        for row in range(4):
            for col in range(10):
                x = col * 70 + 50
                y = row * 50 + 50
                alien = self.canvas.create_rectangle(
                    x, y, x + 40, y + 30, fill='red'
                )
                self.aliens.append(alien)
    
    def move_player(self, dx):
        if self.game_over:
            return
        coords = self.canvas.coords(self.player)
        if 0 <= coords[0] + dx <= 750:
            self.canvas.move(self.player, dx, 0)
            self.player_x += dx
    
    def shoot(self):
        if self.game_over:
            return
        bullet = self.canvas.create_rectangle(
            self.player_x + 22, self.player_y - 10,
            self.player_x + 28, self.player_y,
            fill='white'
        )
        self.bullets.append(bullet)
    
    def move_aliens(self):
        edge_hit = False
        for alien in self.aliens:
            coords = self.canvas.coords(alien)
            if coords[2] >= 800 or coords[0] <= 0:
                edge_hit = True
                break
        
        if edge_hit:
            self.alien_direction *= -1
            for alien in self.aliens:
                self.canvas.move(alien, 0, 20)
        
        for alien in self.aliens:
            self.canvas.move(alien, self.alien_direction, 0)
    
    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -10)
            coords = self.canvas.coords(bullet)
            if coords[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
    
    def check_collisions(self):
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.coords(bullet)
            if not bullet_coords:
                continue
            
            for alien in self.aliens[:]:
                alien_coords = self.canvas.coords(alien)
                if not alien_coords:
                    continue
                
                if (bullet_coords[0] < alien_coords[2] and
                    bullet_coords[2] > alien_coords[0] and
                    bullet_coords[1] < alien_coords[3] and
                    bullet_coords[3] > alien_coords[1]):
                    
                    self.canvas.delete(bullet)
                    self.canvas.delete(alien)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if alien in self.aliens:
                        self.aliens.remove(alien)
                    self.score += 10
                    self.canvas.itemconfig(
                        self.score_text, 
                        text=f"Score: {self.score}"
                    )
                    break
    
    def check_game_over(self):
        for alien in self.aliens:
            coords = self.canvas.coords(alien)
            if coords[3] >= 520:
                self.game_over = True
                self.canvas.create_text(
                    400, 300, 
                    text="GAME OVER!\nPress R to restart", 
                    fill='red', 
                    font=('Arial', 32),
                    justify='center'
                )
                return
        
        if len(self.aliens) == 0:
            self.create_aliens()
    
    def game_loop(self):
        if not self.game_over:
            self.move_aliens()
            self.move_bullets()
            self.check_collisions()
            self.check_game_over()
        
        self.root.after(50, self.game_loop)
    
    def restart(self):
        self.reset_game()

def main():
    root = tk.Tk()
    game = SpaceInvaders(root)
    root.mainloop()

if __name__ == "__main__":
    main()
