import tkinter as tk
from datetime import datetime, timedelta

class PongGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkinter Pong")

        # Create canvas
        self.canvas = tk.Canvas(master, width=1600, height=800, bg='green')
        self.canvas.pack()

        # Initialize paddles and ball
        self.paddle1 = self.canvas.create_rectangle(30, 300, 50, 500, fill="white")
        self.paddle2 = self.canvas.create_rectangle(1550, 300, 1570, 500, fill="white")
        self.ball = self.canvas.create_oval(790, 390, 810, 410, fill="white")

        # Ball and game settings
        self.ball_speed = 10  # Increased ball speed for more realistic gameplay
        self.ball_dx = self.ball_speed
        self.ball_dy = -self.ball_speed

        # Paddle movement settings
        self.paddle_speed = 20
        self.paddles_motion = {'w': 0, 's': 0, 'Up': 0, 'Down': 0}
        self.game_active = True

        # Score variables
        self.score1 = 0
        self.score2 = 0

        # Score and timer labels
        self.score1_label = tk.Label(master, text=f"{self.score1}", font=('Arial', 24))
        self.score1_label.pack(side='left')
        self.timer_label = tk.Label(master, text="00:00", font=('Arial', 24))
        self.timer_label.pack(side='bottom')
        self.score2_label = tk.Label(master, text=f"{self.score2}", font=('Arial', 24))
        self.score2_label.pack(side='right')

        # Timer setup
        self.start_time = datetime.now()
        self.update_timer()

        # Movement handlers and game controls
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        # Update game method
        self.update_game()

    def on_key_press(self, event):
        if event.keysym in ['w', 's', 'Up', 'Down']:
            self.paddles_motion[event.keysym] = 1
        elif event.keysym == 'space':
            self.game_active = not self.game_active
        elif event.keysym == 'Escape':
            if tk.messagebox.askyesno("Exit Game", "Do you really want to quit the game?"):
                self.master.destroy()

    def on_key_release(self, event):
        if event.keysym in ['w', 's', 'Up', 'Down']:
            self.paddles_motion[event.keysym] = 0

    def move_paddles(self):
        if self.game_active:
            if self.paddles_motion['w']:
                if self.canvas.coords(self.paddle1)[1] > 0:
                    self.canvas.move(self.paddle1, 0, -self.paddle_speed)
            if self.paddles_motion['s']:
                if self.canvas.coords(self.paddle1)[3] < 800:
                    self.canvas.move(self.paddle1, 0, self.paddle_speed)
            if self.paddles_motion['Up']:
                if self.canvas.coords(self.paddle2)[1] > 0:
                    self.canvas.move(self.paddle2, 0, -self.paddle_speed)
            if self.paddles_motion['Down']:
                if self.canvas.coords(self.paddle2)[3] < 800:
                    self.canvas.move(self.paddle2, 0, self.paddle_speed)

    def update_timer(self):
        if self.game_active:
            now = datetime.now()
            elapsed = now - self.start_time
            self.timer_label.config(text=str(timedelta(seconds=elapsed.seconds))[:7])
            self.master.after(1000, self.update_timer)

    def update_game(self):
        if self.game_active:
            self.move_paddles()  # Update paddle positions based on keys pressed

            # Ball movement
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            ball_coords = self.canvas.coords(self.ball)

            # Wall collision
            if ball_coords[1] <= 0 or ball_coords[3] >= 800:
                self.ball_dy = -self.ball_dy
            
            # Paddle collision
            if (ball_coords[0] <= 50 and ball_coords[2] >= 30 and self.canvas.coords(self.paddle1)[3] >= ball_coords[1] and self.canvas.coords(self.paddle1)[1] <= ball_coords[3]):
                self.ball_dx = -self.ball_dx
            elif (ball_coords[2] >= 1550 and ball_coords[0] <= 1570 and self.canvas.coords(self.paddle2)[3] >= ball_coords[1] and self.canvas.coords(self.paddle2)[1] <= ball_coords[3]):
                self.ball_dx = -self.ball_dx

            # Score update
            if ball_coords[0] <= 0:
                self.score2 += 1
                self.score2_label.config(text=f"{self.score2}")
                self.canvas.coords(self.ball, 790, 390, 810, 410)
                self.ball_dx = self.ball_speed
            elif ball_coords[2] >= 1600:
                self.score1 += 1
                self.score1_label.config(text=f"{self.score1}")
                self.canvas.coords(self.ball, 790, 390, 810, 410)
                self.ball_dx = -self.ball_speed

        self.master.after(20, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
