import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import time

# === Game constants ===
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'jack': 10, 'queen': 10, 'king': 10, 'ace': 11
}
CARD_FOLDER = "cards"
CARD_BACK_FILE = "back_card.png"

# === Game logic ===
def create_deck():
    return [(rank, suit) for rank in ranks for suit in suits]

def deal_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    value = sum(ranks[card[0]] for card in hand)
    aces = [card for card in hand if card[0] == 'A']
    while value > 21 and aces:
        value -= 10
        aces.pop()
    return value

def can_split(hand):
    return len(hand) == 2 and hand[0][0] == hand[1][0]

# === GUI Class ===
class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.money = 100
        self.wins = 0
        self.losses = 0
        self.ties = 0

        self.deck = []
        self.player_hands = []
        self.current_hand_index = 0
        self.dealer_hand = []
        self.bet = 0
        self.card_images = {}
        self.card_back_image = None

        self.start_screen()

    def load_card_image(self, card):
        rank, suit = card
        filename = f"{rank.lower()}_of_{suit.lower()}.png"
        path = os.path.join(CARD_FOLDER, filename)
        if path not in self.card_images:
            image = Image.open(path).resize((80, 115))
            self.card_images[path] = ImageTk.PhotoImage(image)
        return self.card_images[path]

    def load_card_back_image(self):
        path = os.path.join(CARD_FOLDER, CARD_BACK_FILE)
        if not self.card_back_image:
            image = Image.open(path).resize((80, 115))
            self.card_back_image = ImageTk.PhotoImage(image)
        return self.card_back_image

    def start_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Blackjack!", font=("Helvetica", 16)).pack(pady=10)
        self.money_label = tk.Label(self.root, text=f"Money: ${self.money}")
        self.money_label.pack()

        tk.Label(self.root, text="Enter your bet:").pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        tk.Button(self.root, text="Start Game", command=self.start_round).pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()

    def game_over_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Game Over", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Wins: {self.wins}").pack()
        tk.Label(self.root, text=f"Losses: {self.losses}").pack()
        tk.Label(self.root, text=f"Ties: {self.ties}").pack()
        tk.Label(self.root, text=f"Final Balance: ${self.money}").pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack(pady=5)

    def next_round_prompt(self):
        self.clear_screen()
        tk.Label(self.root, text="Do you want to play another round?", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Yes", command=self.start_screen).pack(pady=5)
        tk.Button(self.root, text="No", command=self.game_over_screen).pack(pady=5)

    def split_hand(self):
        if not can_split(self.player_hands[self.current_hand_index]):
            return

        hand = self.player_hands[self.current_hand_index]
        card1 = hand[0]
        card2 = hand[1]

        # Replace current hand with split + new card
        self.player_hands[self.current_hand_index] = [card1, deal_card(self.deck)]
        # Insert second split hand right after
        self.player_hands.insert(self.current_hand_index + 1, [card2, deal_card(self.deck)])

        self.split_button.config(state=tk.DISABLED)
        self.animate_display(hide_dealer=True)

    def finish_round(self):
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card(self.deck))
            self.animate_display(hide_dealer=False)

        dealer_total = calculate_hand_value(self.dealer_hand)
        results = []

        for hand in self.player_hands:
            player_total = calculate_hand_value(hand)
            if player_total > 21:
                results.append(-self.bet)
                self.losses += 1
            elif dealer_total > 21 or player_total > dealer_total:
                results.append(self.bet)
                self.wins += 1
            elif dealer_total > player_total:
                results.append(-self.bet)
                self.losses += 1
            else:
                results.append(0)
                self.ties += 1

        total_result = sum(results)
        self.money += total_result

        result_msg = ""
        for i, r in enumerate(results):
            if r > 0:
                result_msg += f"Hand {i+1}: You win!\n"
            elif r < 0:
                result_msg += f"Hand {i+1}: Dealer wins.\n"
            else:
                result_msg += f"Hand {i+1}: Tie.\n"

        self.update_display(hide_dealer=False)
        messagebox.showinfo("Round Result", result_msg.strip())
        self.next_round_prompt()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_round(self):
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet <= 0 or self.bet > self.money:
                raise ValueError("Invalid bet amount.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.deck = create_deck()
        random.shuffle(self.deck)

        self.player_hands = [[deal_card(self.deck), deal_card(self.deck)]]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]

        self.current_hand_index = 0

        # ** FIX: Setup the UI before updating display **
        self.setup_game_ui()

        self.animate_display(hide_dealer=True)

    
    def animate_display(self, hide_dealer=False):
        self.update_display(hide_dealer=hide_dealer)
        self.root.update()
        time.sleep(0.2)

    def setup_game_ui(self):
        self.clear_screen()
        self.money_label = tk.Label(self.root, text=f"Money: ${self.money}")
        self.money_label.pack()

        self.dealer_frame = tk.LabelFrame(self.root, text="Dealer's Hand")
        self.dealer_frame.pack(pady=5)

        self.player_frame = tk.LabelFrame(self.root, text="Player's Hands")
        self.player_frame.pack(pady=5)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        self.hit_button = tk.Button(self.controls_frame, text="Hit", command=self.hit)
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.controls_frame, text="Stand", command=self.stand)
        self.stand_button.grid(row=0, column=1, padx=10)

        self.split_button = tk.Button(self.controls_frame, text="Split", command=self.split_hand)
        self.split_button.grid(row=0, column=2, padx=10)
        self.split_button.config(state=tk.DISABLED)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def update_display(self, hide_dealer=False):
        self.clear_frame(self.dealer_frame)
        self.clear_frame(self.player_frame)

        dealer_total = calculate_hand_value(self.dealer_hand) if not hide_dealer else "???"
        tk.Label(self.dealer_frame, text=f"Total: {dealer_total}").pack()

        if hide_dealer:
            back_img = self.load_card_back_image()
            tk.Label(self.dealer_frame, image=back_img).pack(side=tk.LEFT)
            card_img = self.load_card_image(self.dealer_hand[1])
            tk.Label(self.dealer_frame, image=card_img).pack(side=tk.LEFT)
        else:
            for card in self.dealer_hand:
                card_img = self.load_card_image(card)
                tk.Label(self.dealer_frame, image=card_img).pack(side=tk.LEFT)

        for i, hand in enumerate(self.player_hands):
            frame = tk.LabelFrame(self.player_frame, text=f"Hand {i + 1}{' (Active)' if i == self.current_hand_index else ''}")
            frame.pack(pady=5)
            tk.Label(frame, text=f"Total: {calculate_hand_value(hand)}").pack()
            for card in hand:
                card_img = self.load_card_image(card)
                tk.Label(frame, image=card_img).pack(side=tk.LEFT)

        self.money_label.config(text=f"Money: ${self.money}")

    def hit(self):
        current_hand = self.player_hands[self.current_hand_index]
        current_hand.append(deal_card(self.deck))
        self.animate_display(hide_dealer=True)
        if calculate_hand_value(current_hand) > 21:
            messagebox.showinfo("Result", f"Hand {self.current_hand_index + 1} busted!")
            self.finish_round()

    def stand(self):
        self.finish_round()

# === Run the game ===
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
