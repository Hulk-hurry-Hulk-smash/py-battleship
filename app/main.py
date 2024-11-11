from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def hit(self) -> None:
        """Mark the deck as hit."""
        self.is_alive = False


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks: List[Deck] = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        """Create decks based on the start and end coordinates."""
        decks = []
        if self.start[0] == self.end[0]:  # Horizontal ship
            for col in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(self.start[0], col))
        elif self.start[1] == self.end[1]:  # Vertical ship
            for row in range(self.start[0], self.end[0] + 1):
                decks.append(Deck(row, self.start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        """Find the corresponding deck by coordinates."""
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        """Handle a hit to a specific deck in the ship."""
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(
            self,
            ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.field = {}
        self.ships = [Ship(start, end) for start, end in ships]
        self._create_field()

    def _create_field(self) -> None:
        """Map each deck's coordinates to its respective ship."""
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: Tuple[int, int]) -> str:
        """Simulate a shot at the given location."""
        if location in self.field:
            ship = self.field[location]
            row, column = location
            return ship.fire(row, column)
        else:
            return "Miss!"
