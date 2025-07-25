# Card Games Collection

A collection of interactive card game implementations with a graphical user interface (GUI) built using **Python**, **Tkinter**, and **Pillow (PIL)**. The project currently includes:

- **Higher or Lower** — Guess if the next card will be higher or lower.
- **Blackjack** — A simplified version of the classic Blackjack game with betting and splitting.
- **Blackjack Card Counter Helper** — A command-line tool to help track card counts using the Hi-Lo counting system.

---

## **Features**

### **1. Higher or Lower**
- Fully interactive GUI using Tkinter.
- Card preview with **card back image**.
- Dynamic **probability hints** for higher/lower guesses.
- Score and high-score tracking.
- Restart and quit functionality.

### **2. Blackjack**
- Play against the dealer with a starting balance of `$100`.
- Bet system with input validation.
- Ability to **split hands**.
- Live card animations (simple time delays).
- Tracks **wins, losses, and ties**.
- Displays the dealer's hidden card until the round ends.

### **3. Blackjack Card Counter Helper**
- CLI tool that simulates a **Hi-Lo counting system** for 6 decks.
- Tracks:
  - Running count
  - True count (based on decks remaining)
  - Remaining cards by rank
- Commands:
  - `status` — View current count and remaining cards.
  - `reset` — Reset the count and deck.
  - `exit` — Quit the tool.

---

## **Requirements**
- Python 3.8+
- **Dependencies:**
  - `tkinter` (comes pre-installed with Python on most platforms)
  - `Pillow` for image handling:
    ```bash
    pip install Pillow
    ```

---

## **Project Structure**
```
card-games/
│
├── cards/                  # Folder containing card images (e.g., 2_of_hearts.png, back_card.png)
├── higher_lower.py         # Higher or Lower game
├── blackjack.py            # Blackjack game with betting and splitting
├── blackjack_counter.py    # Hi-Lo card counting helper
└── README.md               # Project documentation
```

---

## **How to Run**
Run the following commands in your terminal:

### **Higher or Lower**
```bash
python higher_lower.py
```

### **Blackjack**
```bash
python blackjack.py
```

### **Blackjack Card Counter**
```bash
python blackjack_counter.py
```

---

## **Future Improvements**
- Add sound effects for game events.
- Implement multiplayer or AI-based dealer logic.
- Expand to include additional card games (e.g., Poker, Solitaire).

---

## **Author**
**George Johnson**

---

## **License**
This project is open-source under the MIT License.
