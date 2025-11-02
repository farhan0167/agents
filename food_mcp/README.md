# Personal Pantry MCP

## Overview

This project is a demonstration of a Model Context Protocol (MCP) server that gives your LLMs insight into your pantry.

As someone who loves to cook, I often end up making the same dish over and over. I wouldn't cook a new dish until I've tried it myself, and after some point I'd essentially just get tired of having the same meal. So I thought: wouldn't it be cool if the LLM applications I use everyday had knowledge of what's in my pantry? That way, I can ask it to construct some dish.

But how do we give LLMs access to our pantry? One way to do this would be by taking a photo of your fridge and every other place you store food, and have the LLM add it to some data store. This is not only more complex for the LLM (although I'm sure LLMs are capable of it), it also adds friction for the user. An alternative would be: every time you come back from the grocery store, you snap a picture of your receipt, and have the LLM add it to your data store. Even though this adds friction, it's more intuitive for the user. And LLMs are pretty capable when it comes to deciphering receipt text. This project exposes an MCP server that provides a simple mechanism to add, update, and remove items from your pantry, along with prompts to do receipt extraction.

## Getting Started

1. Make sure you have uv installed, and run:
    
    ```bash
    uv sync
    ```
2. At the moment this was only tested with Claude Desktop, so make sure you have that installed in your system. Before launching Claude, run the following command from within this directory:
   
    ```bash
    uv run fastmcp install claude-desktop main.py
    ```
3. Open Claude Desktop and start adding your reciepts. 

## System Overview

![./assets/system_diagram.png](image-system)

## Tools

This MCP server exposes several tools to manage your pantry:

### `add_to_pantry`
Add items to your pantry inventory. Each time you add items, they're appended as separate entries - just like how you'd add a new pack of chicken to your fridge without combining it with the old one. This way, each item can have its own expiration date.

**Example use**: "Add 2lbs of chicken breast and a dozen eggs to my pantry"

### `get_pantry`
Check what's currently in your pantry. Use this when you want to see everything you have, or search for specific items.

**Example use**: "Do I have chicken in my pantry?" or "What's in my pantry right now?"

### `remove_from_pantry`
Remove items from your pantry when they're gone or expired.

**Example use**: "Remove expired milk from my pantry"

### `update_pantry_item`
Update the quantity or name of an existing item.

**Example use**: "Update the flour quantity to 3lbs"


## Prompts

### `add_receipt_to_pantry`
This is the main prompt that guides the LLM through processing a receipt image. When you upload a receipt and say "add this to my pantry", the LLM will:

1. Read all the text from your receipt
2. Identify only food and grocery items (it'll skip things like paper towels or soap)
3. Extract relevant information: the item name, a normalized name (like "milk" instead of "Organic Valley 2% Milk"), quantity, and calculate an expiration date
4. Add everything to your pantry automatically

The LLM is smart enough to estimate expiration dates based on what type of food it is - fresh chicken gets a few days, while flour gets several months.

## How It Works

The pantry follows an **append-only** model that matches how real pantries work. When you buy chicken on Monday and again on Thursday, you don't merge them together - they're separate packages with different expiration dates. Same thing here. Each purchase creates a separate entry in your pantry, complete with:

- The exact name from your receipt
- A normalized name for easy searching (e.g., "chicken breast")
- Quantity with units (e.g., "2lbs", "12", "1 gallon")
- When you added it (automatically tracked)
- When it expires (automatically calculated based on food type)