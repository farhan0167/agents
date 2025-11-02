from fastmcp import FastMCP
from food_mcp.service import PantryService

# Initialize MCP server
mcp = FastMCP("Pantry MCP Server")

# Initialize service
service = PantryService()

# Register tools (using bound methods per FastMCP best practices)
mcp.tool(service.add_to_pantry)
mcp.tool(service.remove_from_pantry)
mcp.tool(service.update_pantry_item)
mcp.tool(service.get_pantry)

# Register resource
mcp.resource("pantry://inventory")(service.get_pantry_resource)

# Register prompt
mcp.prompt()(service.add_receipt_to_pantry_prompt)

if __name__ == "__main__":
    mcp.run(transport="stdio")