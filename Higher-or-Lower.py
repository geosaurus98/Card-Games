import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# === Game Constants ===
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}  # Assign values to ranks
CARD_FOLDER = "cards"  # Folder with card images
CARD_BACK_FILE = "back_card.png"  # Card back image

def create_deck():
    """Create a standard deck of cards."""
    return [(rank, suit) for suit in suits for rank in ranks]

# === GUI Class ===
class HigherLowerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Higher or Lower")
        
        # Game variables
        self.card_images = {}
        self.current_card = None
        self.next_card = None
        self.score = 0
        self.high_score = 0
        self.deck = []

        # Track hint visibility
        self.hint_visible = False

        # Load card back image for preview
        self.card_back_image = self.load_card_back_image()
        
        # Setup UI and start the game
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        """Set up all UI elements."""
        # Score labels
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=5)

        self.high_score_label = tk.Label(self.root, text="High Score: 0", font=("Helvetica", 12))
        self.high_score_label.pack(pady=5)

        # Card display area (current card + preview)
        self.card_frame = tk.Frame(self.root)
        self.card_frame.pack(pady=10)

        self.card_label = tk.Label(self.card_frame)
        self.card_label.pack(side=tk.LEFT, padx=5)

        self.next_card_preview = tk.Label(self.card_frame, image=self.card_back_image)
        self.next_card_preview.pack(side=tk.LEFT, padx=5)

        # Live hint label
        self.hint_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.hint_label.pack(pady=5)

        # Buttons for game controls
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.higher_button = tk.Button(button_frame, text="Higher", width=10, command=lambda: self.make_guess('h'))
        self.higher_button.grid(row=0, column=0, padx=5)

        self.lower_button = tk.Button(button_frame, text="Lower", width=10, command=lambda: self.make_guess('l'))
        self.lower_button.grid(row=0, column=1, padx=5)

        self.toggle_hint_button = tk.Button(button_frame, text="Show Hint", width=10, command=self.toggle_hint)
        self.toggle_hint_button.grid(row=0, column=2, padx=5)

        self.restart_button = tk.Button(button_frame, text="Restart", width=10, command=self.start_game)
        self.restart_button.grid(row=0, column=3, padx=5)

        self.quit_button = tk.Button(button_frame, text="Quit", width=10, command=self.root.destroy)
        self.quit_button.grid(row=0, column=4, padx=5)

    def load_card_image(self, card):
        """Load the card image from the cards folder."""
        rank, suit = card
        filename = f"{rank}_of_{suit}.png"
        path = os.path.join(CARD_FOLDER, filename)
        if path not in self.card_images:
            image = Image.open(path).resize((100, 145))
            self.card_images[path] = ImageTk.PhotoImage(image)
        return self.card_images[path]

    def load_card_back_image(self):
        """Load the back of a card for the preview."""
        path = os.path.join(CARD_FOLDER, CARD_BACK_FILE)
        image = Image.open(path).resize((100, 145))
        return ImageTk.PhotoImage(image)

    def start_game(self):
        """Start a new game: shuffle deck and draw the first card."""
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.current_card = self.deck.pop()
        self.show_card(self.current_card)
        self.higher_button.config(state=tk.NORMAL)
        self.lower_button.config(state=tk.NORMAL)
        self.update_hint()

    def show_card(self, card):
        """Display a card on the screen."""
        card_img = self.load_card_image(card)
        self.card_label.config(image=card_img)
        self.card_label.image = card_img

    def toggle_hint(self):
        """Toggle visibility of the hint label."""
        self.hint_visible = not self.hint_visible
        if self.hint_visible:
            self.hint_label.pack(pady=5)
            self.toggle_hint_button.config(text="Hide Hint")
            self.update_hint()
        else:
            self.hint_label.pack_forget()
            self.toggle_hint_button.config(text="Show Hint")

    def update_hint(self):
        """Update the live hint label."""
        if not self.hint_visible:
            return  # Do nothing if hint is hidden

        if not self.deck:
            self.hint_label.config(text="No cards left in the deck.")
            return

        current_value = rank_values[self.current_card[0]]
        filtered_deck = [card for card in self.deck if rank_values[card[0]] != current_value]

        if not filtered_deck:
            self.hint_label.config(text="All remaining cards are the same as current!")
            return

        higher_count = sum(1 for card in filtered_deck if rank_values[card[0]] > current_value)
        lower_count = sum(1 for card in filtered_deck if rank_values[card[0]] < current_value)

        total_remaining = len(filtered_deck)
        higher_prob = (higher_count / total_remaining) * 100
        lower_prob = (lower_count / total_remaining) * 100

        self.hint_label.config(
            text=f"Prob. Higher: {higher_prob:.1f}% | Prob. Lower: {lower_prob:.1f}%"
        )

    def make_guess(self, guess):
        """Process player's guess: higher or lower."""
        if not self.deck:
            messagebox.showinfo("Game Over", f"Deck empty! Final Score: {self.score}")
            self.end_game()
            return

        self.next_card = self.deck.pop()
        current_value = rank_values[self.current_card[0]]
        next_value = rank_values[self.next_card[0]]
        self.show_card(self.next_card)

        if next_value == current_value:
            messagebox.showinfo("Tie", "The card is the same value! No win/loss. Continue...")
            self.current_card = self.next_card
            self.update_hint()
            return

        if (guess == 'h' and next_value > current_value) or (guess == 'l' and next_value < current_value):
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.update_high_score()
            self.current_card = self.next_card
        else:
            messagebox.showinfo("Game Over", f"Wrong guess! Final Score: {self.score}")
            self.end_game()

        self.update_hint()

    def update_high_score(self):
        """Update the high score if current score is higher."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")

    def end_game(self):
        """Disable buttons after game ends."""
        self.update_high_score()
        self.higher_button.config(state=tk.DISABLED)
        self.lower_button.config(state=tk.DISABLED)
        self.hint_label.config(text="Game Over!")

# === Run the game ===
if __name__ == "__main__":
    root = tk.Tk()
    game = HigherLowerGUI(root)
    root.mainloop()
