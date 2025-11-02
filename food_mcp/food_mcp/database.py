import json
from pathlib import Path
from typing import Optional

from .pantry import Pantry, PantryItem


class Database:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.pantry: Pantry = self.load_data()

    def load_data(self) -> Pantry:
        """Load pantry data from JSON file. Creates empty pantry if file doesn't exist."""
        if not self.db_path.exists():
            # Create empty pantry if file doesn't exist
            empty_pantry = Pantry(items=[])
            self.save_data(empty_pantry)
            return empty_pantry

        try:
            with open(self.db_path, 'r') as f:
                data = json.load(f)
                return Pantry(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted pantry data file: {e}")

    def save_data(self, pantry: Pantry) -> None:
        """Save pantry data to JSON file."""
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.db_path, 'w') as f:
            f.write(pantry.model_dump_json(indent=2))

    def add_items(self, items: list[PantryItem]) -> Pantry:
        """Add items to pantry. Always appends new items (no merging)."""
        for new_item in items:
            # Always add as a new item (append-only behavior)
            self.pantry.items.append(new_item)

        # Save to disk
        self.save_data(self.pantry)
        return self.pantry

    def remove_items(self, general_names: list[str]) -> Pantry:
        """Remove items from pantry by general_name."""
        self.pantry.items = [
            item for item in self.pantry.items
            if item.general_name not in general_names
        ]

        # Save to disk
        self.save_data(self.pantry)
        return self.pantry

    def update_item(
        self,
        general_name: str,
        quantity: Optional[str] = None,
        name: Optional[str] = None
    ) -> PantryItem:
        """Update an existing pantry item's quantity or name."""
        item = self.find_item(general_name)

        if not item:
            raise ValueError(f"Item with general_name '{general_name}' not found in pantry")

        # Update fields if provided
        if quantity is not None:
            item.quantity = quantity
        if name is not None:
            item.name = name
            item.reciept_name = name

        # Save to disk
        self.save_data(self.pantry)
        return item

    def get_pantry(self) -> Pantry:
        """Get the entire pantry inventory."""
        return self.pantry

    def find_item(self, general_name: str) -> Optional[PantryItem]:
        """Find an item by its general_name."""
        for item in self.pantry.items:
            if item.general_name == general_name:
                return item
        return None