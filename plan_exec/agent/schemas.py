from operator import add
from typing_extensions import TypedDict
from typing import Annotated, List, Literal

from langchain.messages import AnyMessage
from pydantic import BaseModel, Field

class Item(BaseModel):
    step: str = Field(description="An item on the to-do list that needs to be completed.")
    status: Literal["todo", "in_progress", "done"] = Field(
        default="todo",
        description="The status of the item",
    )
    
class Todo(BaseModel):
    todo: List[Item] = Field(description="The to-do list, that is, a list of items to be completed.")

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add]
    todo: Todo
    
