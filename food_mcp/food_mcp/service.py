"""PantryService: Business logic layer for MCP tools, resources, and prompts."""

from pathlib import Path
from typing import Optional

from .database import Database
from .pantry import PantryItem


class PantryService:
    """Service layer that handles all MCP tool operations for pantry management."""

    def __init__(self, db_path: str | None = None):
        """Initialize the service with a database connection."""
        if db_path is None:
            # Use user's home directory by default for write permissions
            db_path = str(Path.home() / ".pantry_mcp" / "pantry_data.json")
        self.db = Database(db_path)

    # ==================== MCP TOOLS ====================

    def add_to_pantry(self, items: list[PantryItem]) -> str:
        """
        Add items to the pantry inventory.

        Args:
            items: List of PantryItem objects with: name, general_name, quantity, reciept_name, expiration_time (optional)

        Returns:
            Confirmation message with added items
        """
        # Add to database
        self.db.add_items(items)

        # Format response
        item_list = "\n".join([
            f"  - {item.general_name}: {item.quantity} ({item.name})"
            for item in items
        ])

        return f"Added {len(items)} item(s) to pantry:\n{item_list}"

    def remove_from_pantry(self, items: list[str]) -> str:
        """
        Remove items from the pantry inventory.

        Args:
            items: List of general_names to remove

        Returns:
            Confirmation message with removed items
        """
        self.db.remove_items(items)

        item_list = ", ".join(items)
        return f"Removed {len(items)} item(s) from pantry: {item_list}"

    def update_pantry_item(
        self,
        general_name: str,
        quantity: Optional[str] = None,
        name: Optional[str] = None
    ) -> str:
        """
        Update quantity or details of an existing pantry item.

        Args:
            general_name: The general name of the item to update
            quantity: New quantity (optional)
            name: New name (optional)

        Returns:
            Confirmation with updated item details
        """
        try:
            updated_item = self.db.update_item(general_name, quantity, name)

            changes = []
            if quantity:
                changes.append(f"quantity to {quantity}")
            if name:
                changes.append(f"name to {name}")

            change_str = " and ".join(changes)

            return f"Updated {updated_item.general_name}: {change_str}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def get_pantry(self) -> str:
        """
        Get the entire pantry inventory. Use this tool if you need to find a specific item,
        or a group of items.

        Returns:
            JSON string of all pantry items
        """
        pantry = self.db.get_pantry()
        return pantry.model_dump_json(indent=2)


    # ==================== MCP RESOURCES ====================

    def get_pantry_resource(self) -> str:
        """
        Get pantry inventory as JSON for MCP resource.

        Returns:
            JSON string of pantry data
        """
        pantry = self.db.get_pantry()
        return pantry.model_dump_json(indent=2)

    # ==================== MCP PROMPTS ====================

    def add_receipt_to_pantry_prompt(self) -> str:
        """
        Prompt template for processing receipt images.

        Returns:
            Detailed prompt for Claude to process receipt images and extract grocery items
        """
        prompt = """
I've uploaded a receipt image. Please:

1. Carefully read all text from the receipt
2. Identify only FOOD and GROCERY items (ignore non-food items like paper towels, soap, toiletries, etc.)
3. For each food item, extract:
   - name: The exact name as it appears on the receipt (e.g., "Organic Valley 2% Milk")
   - general_name: A normalized, simple name (e.g., "milk", "eggs", "chicken breast")
   - quantity: The quantity with unit as a single string (e.g., "12", "2.5lbs", "1 gallon")
   - reciept_name: The name from this receipt (singular, not a list)
   - expiration_time: Calculate an estimated expiration date based on the item type
     * Fresh meat/poultry (chicken, beef, pork): 2-3 days from now, or ask the user if they have a better estimate
     * Fresh fish/seafood: 1-2 days from now, or ask the user if they have a better estimate
     * Milk/dairy: 7 days from now
     * Fresh produce (vegetables, fruits): 5-7 days from now
     * Bread: 5 days from now
     * Eggs: 3-4 weeks from now
     * Dry goods (flour, rice, pasta): 6-12 months from now
     * Canned goods: 1-2 years from now
     Use ISO 8601 format: "2024-01-15T12:00:00"

4. For some items such as chicken, beef, etc. you may need to make a guess as to the quantity. To
make a good guess, please use Web Search to find the product information. For instance, if the
reciept is from Food Bazar, then search for "Chicken Legs from Food Bazar". This will give you the
price and quantity. Based on the price and quantity, and the price paid on the recipt, do the math on
how much quantity I bought.

5. Call the add_to_pantry tool with this JSON format:
{
  "items": [
    {
      "name": "Large Organic Eggs AA",
      "general_name": "eggs",
      "quantity": "12",
      "reciept_name": "Large Organic Eggs AA",
      "expiration_time": "2024-02-15T12:00:00"
    },
    {
      "name": "Whole Milk",
      "general_name": "milk",
      "quantity": "1 gallon",
      "reciept_name": "Whole Milk",
      "expiration_time": "2024-01-29T12:00:00"
    },
    {
      "name": "King Arthur All-Purpose Flour",
      "general_name": "flour",
      "quantity": "5lbs",
      "reciept_name": "King Arthur All-Purpose Flour",
      "expiration_time": "2024-07-22T12:00:00"
    }
  ]
}

6. After successfully adding items, provide a summary of what was added to my pantry.

Important notes:
- Be careful with quantities: "2 @ $3.99" means quantity is "2", not the price
- Include the unit with the quantity as a single string: "2.5lbs", "1 gallon", "12"
- Ignore sales tax, subtotals, totals, and store information
- Ignore duplicate line items (some receipts list items twice)
- If an item quantity is unclear, default to "1"
- Use simple, lowercase general_names: "milk" not "Whole Milk", "eggs" not "Large Eggs"
- Only include items that would be stored in a kitchen pantry
- time_added will be auto-set, so you don't need to include it
- Each purchase creates a separate pantry entry, even if you already have that item
"""
        return prompt
