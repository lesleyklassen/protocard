import csv
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def read_csv(file_path):
    cards = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards.append(row)
    return cards

def display_card(card, face_down=False):
    if face_down:
        card_content = "[bold red]Card is face down[/bold red]"
    else:
        top_of_card = card.get('top_of_card', '')
        center_of_card = card.get('center_of_card', '').replace('\\n', '\n')
        bottom_of_card = card.get('bottom_of_card', '')
        card_content = f"[bold]{top_of_card}[/bold]\n\n{center_of_card}\n\n[italic]{bottom_of_card}[/italic]"

    card_panel = Panel.fit(card_content, title="Card", border_style="bold white")
    console.print(card_panel)

def display_hand(hand):
    if not hand:
        console.print("[bold red]No cards in hand[/bold red]")
        return

    hand_table = Table(expand=True)
    for card in hand:
        top_of_card = card.get('top_of_card', '')
        center_of_card = card.get('center_of_card', '').replace('\\n', '\n')
        bottom_of_card = card.get('bottom_of_card', '')
        card_content = f"[bold]{top_of_card}[/bold]\n\n{center_of_card}\n\n[italic]{bottom_of_card}[/italic]"
        card_panel = Panel.fit(card_content, border_style="bold white")
        hand_table.add_column(justify="center", no_wrap=True)  # Add a column for each card
        hand_table.columns[-1].header = card_panel  # Set the column header to be the card panel
    console.print(hand_table)



def shuffle_deck(deck, discard_pile):
    if not discard_pile:
        console.print("[bold red]Cannot shuffle. Discard pile is empty! Play some cards to move them to the discard pile first.[/bold red]")
        return
    deck.extend(discard_pile)
    discard_pile.clear()
    random.shuffle(deck)
    console.print("[bold green]Deck shuffled. Cards in deck: {}[/bold green]".format(len(deck)))


def reset_deck(original_deck, deck, discard_pile, hand=None, table=None):
    deck.clear()
    deck.extend(original_deck)
    discard_pile.clear()
    if hand is not None:
        hand.clear()
    if table is not None:
        table.clear()
    console.print("[bold red]Deck reset to original state.[/bold red]")

def main():
    file_path = 'cards.csv'  # Replace with your CSV file path
    original_deck = read_csv(file_path)
    deck = original_deck.copy()
    discard_pile = []

    while True:
        console.print("[bold blue]Choose deck type:[/bold blue]\n1. Draw and Play\n2. Draw and Hold\n3. Draw and Place Up\n4. Draw and Place Down\n")
        deck_type = input("Enter the number corresponding to the deck type: ").strip()
        deck = original_deck.copy()
        discard_pile.clear()

        if deck_type == "1":
            console.print("[bold green]You have selected Draw and Play deck.[/bold green]")
            while True:
                command = input("Enter command (draw, shuffle, panic, exit): ").strip().lower()
                if command == "draw":
                    if deck:
                        card = deck.pop(0)
                        discard_pile.append(card)
                        display_card(card)
                    else:
                        console.print("[bold red]The deck is empty![/bold red]")
                elif command == "shuffle":
                    shuffle_deck(deck, discard_pile)
                elif command == "panic":
                    reset_deck(original_deck, deck, discard_pile)
                elif command == "exit":
                    break
                else:
                    console.print("[bold red]Invalid command! Please enter draw, shuffle, panic, or exit.[/bold red]")

        elif deck_type == "2":
            console.print("[bold green]You have selected Draw and Hold deck.[/bold green]")
            hand = []
            max_hand_size = 5
            while True:
                command = input("Enter command (draw, play, view, shuffle, panic, exit): ").strip().lower()
                if command == "draw":
                    if len(hand) < max_hand_size:
                        if deck:
                            card = deck.pop(0)
                            hand.append(card)
                            console.print("[bold green]Card added to hand.[/bold green]")
                        else:
                            console.print("[bold red]The deck is empty![/bold red]")
                    else:
                        console.print(f"[bold red]Hand is full! Maximum of {max_hand_size} cards allowed.[/bold red]")
                elif command == "play":
                    if hand:
                        console.print("[bold blue]Cards in hand:[/bold blue]")
                        display_hand(hand)
                        card_idx = input("Enter the number of the card you want to play: ").strip()
                        if card_idx.isdigit() and 1 <= int(card_idx) <= len(hand):
                            card = hand.pop(int(card_idx) - 1)
                            discard_pile.append(card)
                            console.print("[bold green]Card played and moved to discard pile.[/bold green]")
                            display_card(card)
                        else:
                            console.print("[bold red]Invalid card number![/bold red]")
                    else:
                        console.print("[bold red]No cards in hand to play![/bold red]")
                elif command == "view":
                    display_hand(hand)
                elif command == "shuffle":
                    shuffle_deck(deck, discard_pile)
                elif command == "panic":
                    reset_deck(original_deck, deck, discard_pile, hand)
                elif command == "exit":
                    break
                else:
                    console.print("[bold red]Invalid command! Please enter draw, play, view, shuffle, panic, or exit.[/bold red]")

        elif deck_type == "3":
            console.print("[bold green]You have selected Draw and Place Up deck.[/bold green]")
            table = []
            max_table_size = 5
            while True:
                command = input("Enter command (draw, event, view, shuffle, panic, exit): ").strip().lower()
                if command == "draw":
                    if len(table) < max_table_size:
                        if deck:
                            card = deck.pop(0)
                            table.append(card)
                            console.print("[bold green]Card placed face up on table.[/bold green]")
                            display_card(card)
                        else:
                            console.print("[bold red]The deck is empty![/bold red]")
                    else:
                        console.print(f"[bold red]Table is full! Maximum of {max_table_size} cards allowed.[/bold red]")
                elif command == "event":
                    if table:
                        console.print("[bold blue]Cards on table:[/bold blue]")
                        for idx, card in enumerate(table, start=1):
                            console.print(f"{idx}. {card['top_of_card']}")
                        card_idx = input("Enter the number of the card to trigger an event: ").strip()
                        if card_idx.isdigit() and 1 <= int(card_idx) <= len(table):
                            card = table.pop(int(card_idx) - 1)
                            discard_pile.append(card)
                            console.print("[bold green]Event triggered, card moved to discard pile.[/bold green]")
                            display_card(card)
                        else:
                            console.print("[bold red]Invalid card number![/bold red]")
                    else:
                        console.print("[bold red]No cards on table to trigger an event![/bold red]")
                elif command == "view":
                    console.print("[bold blue]Cards on table:[/bold blue]")
                    for idx, card in enumerate(table, start=1):
                        console.print(f"{idx}. {card['top_of_card']}")
                elif command == "shuffle":
                    shuffle_deck(deck, discard_pile)
                elif command == "panic":
                    reset_deck(original_deck, deck, discard_pile, table=table)
                elif command == "exit":
                    break
                else:
                    console.print("[bold red]Invalid command! Please enter draw, event, view, shuffle, panic, or exit.[/bold red]")

        elif deck_type == "4":
            console.print("[bold green]You have selected Draw and Place Down deck.[/bold green]")
            table = []
            max_table_size = 5
            while True:
                command = input("Enter command (draw, flip, event, view, shuffle, panic, exit): ").strip().lower()
                if command == "draw":
                    if len(table) < max_table_size:
                        if deck:
                            card = deck.pop(0)
                            table.append(card)
                            console.print("[bold green]Card placed face down on table.[/bold green]")
                            display_card(card, face_down=True)
                        else:
                            console.print("[bold red]The deck is empty![/bold red]")
                    else:
                        console.print(f"[bold red]Table is full! Maximum of {max_table_size} cards allowed.[/bold red]")
                elif command == "flip":
                    if table:
                        console.print("[bold blue]Cards on table:[/bold blue]")
                        for idx, card in enumerate(table, start=1):
                            console.print(f"{idx}. [bold red]Face Down[/bold red]")
                        card_idx = input("Enter the number of the card to flip: ").strip()
                        if card_idx.isdigit() and 1 <= int(card_idx) <= len(table):
                            card = table[int(card_idx) - 1]
                            console.print("[bold green]Card flipped and revealed:[/bold green]")
                            display_card(card)
                        else:
                            console.print("[bold red]Invalid card number![/bold red]")
                    else:
                        console.print("[bold red]No cards on table to flip![/bold red]")
                elif command == "event":
                    if table:
                        console.print("[bold blue]Cards on table:[/bold blue]")
                        for idx, card in enumerate(table, start=1):
                            if card_idx.isdigit() and 1 <= int(card_idx) <= len(table):
                                console.print(f"{idx}. [bold red]Face Down[/bold red]")
                            else:
                                console.print(f"{idx}. {card['top_of_card']}")
                        card_idx = input("Enter the number of the card to trigger an event: ").strip()
                        if card_idx.isdigit() and 1 <= int(card_idx) <= len(table):
                            card = table.pop(int(card_idx) - 1)
                            discard_pile.append(card)
                            console.print("[bold green]Event triggered, card moved to discard pile.[/bold green]")
                            display_card(card)
                        else:
                            console.print("[bold red]Invalid card number![/bold red]")
                    else:
                        console.print("[bold red]No cards on table to trigger an event![/bold red]")
                elif command == "view":
                    console.print("[bold blue]Cards on table:[/bold blue]")
                    for idx, card in enumerate(table, start=1):
                        console.print(f"{idx}. [bold red]Face Down[/bold red]" if card_idx.isdigit() and 1 <= int(card_idx) <= len(table) else f"{idx}. {card['top_of_card']}")
                elif command == "shuffle":
                    shuffle_deck(deck, discard_pile)
                elif command == "panic":
                    reset_deck(original_deck, deck, discard_pile, table=table)
                elif command == "exit":
                    break
                else:
                    console.print("[bold red]Invalid command! Please enter draw, flip, event, view, shuffle, panic, or exit.[/bold red]")
        else:
            console.print("[bold red]Invalid deck type! Please restart and choose a valid deck type.[/bold red]")

if __name__ == "__main__":
    main()
