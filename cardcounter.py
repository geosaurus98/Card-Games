from collections import defaultdict

# === CONFIGURATION ===
NUM_DECKS = 6
CARDS_PER_DECK = 52
TOTAL_CARDS = NUM_DECKS * CARDS_PER_DECK

card_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Full deck setup
card_counts = defaultdict(int)
for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
    card_counts[rank] = 4 * NUM_DECKS

running_count = 0
cards_seen = []

print(f"\n🃏 Blackjack Helper — Hi-Lo Counter | {NUM_DECKS} decks")
print("Enter cards as '10', 'J', 'A', etc. Type 'status' for summary, 'reset' to start over, 'exit' to quit.")

while True:
    entry = input("\nEnter card: ").strip().upper()

    if entry == 'EXIT':
        break
    elif entry == 'RESET':
        running_count = 0
        cards_seen = []
        for rank in card_counts:
            card_counts[rank] = 4 * NUM_DECKS
        print("🔄 Count and history reset.")
        continue
    elif entry == 'STATUS':
        cards_left = sum(card_counts.values())
        decks_remaining = max(1, cards_left / 52)
        true_count = running_count / decks_remaining

        print(f"\n📊 Running Count: {running_count}")
        print(f"📘 True Count: {true_count:.2f}")
        print(f"🧾 Cards Remaining: {cards_left}")
        print("📌 Remaining Card Counts:")
        for rank in sorted(card_counts.keys(), key=lambda r: (r.isdigit(), r)):
            print(f"  {rank}: {card_counts[rank]}")
        continue

    # Handle actual cards
    if entry in card_values and card_counts[entry] > 0:
        running_count += card_values[entry]
        card_counts[entry] -= 1
        cards_seen.append(entry)

        cards_left = sum(card_counts.values())
        decks_remaining = max(1, cards_left / 52)
        true_count = running_count / decks_remaining

        print(f"✔️ Counted {entry}")
        print(f"Running Count: {running_count}, True Count: {true_count:.2f}")
    else:
        print("❌ Invalid card or too many of that card entered.")
