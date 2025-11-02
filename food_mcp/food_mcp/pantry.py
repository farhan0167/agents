from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PantryItem(BaseModel):
    name: str = Field(description="The name of the pantry item as it appears in the reciept.")
    general_name: str = Field(description="The general name of the pantry item. For example, 'chicken', 'ny strip', or 'eggs'.")
    quantity: str = Field(
        description="""
        The quantity of the pantry item. This could be a weight(lbs), volume, or number of items.
        Example: 1lb, 2cups, etc.
        """,
    )
    reciept_name: str = Field(
        description="Name of the item as found in the reciept.",
    )
    time_added: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the item was added to the pantry. Auto-set to current time.",
    )
    expiration_time: Optional[datetime] = Field(
        default=None,
        description="Estimated expiration date/time for the item. Should be calculated by LLM based on item type.",
    )
    
class Pantry(BaseModel):
    items: list[PantryItem]