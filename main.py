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

def display_card(card):
    top_of_card = card.get('top_of_card', '')
    center_of_card = card.get('center_of_card', '').replace('\\n', '\n')
    bottom_of_card = card.get('bottom_of_card', '')

    table = Table.grid(expand=True)
    table.add_column(justify="center", no_wrap=True)
    
    table.add_row("[bold]" + top_of_card + "[/bold]")
    table.add_row("")
    table.add_row(center_of_card)
    table.add_row("")
    table.add_row("[italic]" + bottom_of_card + "[/italic]")
    
    card_panel = Panel.fit(table, title="Card", border_style="bold white")
    console.print(card_panel)

def shuffle_deck(deck, discard_pile):
    deck.extend(discard_pile)
    discard_pile.clear()
    random.shuffle(deck)
    console.print("[bold green]Deck shuffled.[/bold green]")

def draw_card(deck, discard_pile):
    if deck:
        card = deck.pop(0)
        discard_pile.append(card)
        display_card(card)
    else:
        console.print("[bold red]The deck is empty![/bold red]")

def main():
    file_path = 'cards.csv'  # Replace with your CSV file path
    deck = read_csv(file_path)
    discard_pile = []
    
    while True:
        command = input("Enter command (draw, shuffle, exit): ").strip().lower()
        if command == "draw":
            draw_card(deck, discard_pile)
        elif command == "shuffle":
            shuffle_deck(deck, discard_pile)
        elif command == "exit":
            break
        else:
            console.print("[bold red]Invalid command! Please enter draw, shuffle, or exit.[/bold red]")

if __name__ == "__main__":
    main()
