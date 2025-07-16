from mcp.server.fastmcp import FastMCP

from typing import List, Dict, Any

mcp = FastMCP("Stroy Board MCP Server")


@mcp.tool()
def get_server_prompts() -> List[Dict[str, Any]]:
    """List all avaiable prompt templates."""
    return [
        {
            "name" : "layout",
            "description" : "Set camera Layout or ratio, framing, and aspect ratio.",
            "arguments": [
                {"name": "layout", "type": "string", "description": "The layout to set, e.g., 'portrait', 'landscape', 'square'."},
                {"name": "framing", "type": "string", "description": "The framing to set, e.g., 'close-up', 'medium', 'wide'."},
            ]
        },
        {
            "name" : "clothing",
            "description" : "Set clothing for the character. e.g., 'style','color','accessories'.",
            "arguments": [
                {"name": "style", "type": "string", "description": "The style of clothing, e.g., 'casual', 'formal', 'sporty'."},
                {"name": "color", "type": "string", "description": "The color of the clothing, e.g., 'red', 'blue', 'black'."},
                {"name": "accessories", "type": "string", "description": "Any accessories to include, e.g., 'hat', 'glasses', 'jewelry'."}
            ]
        },
        {
            "name" : "facial_expression",
            "description" : "Set facial expression for the character. e.g., 'happy', 'sad', 'angry'.",
            "arguments": [
                {"name": "expression", "type": "string", "description": "The facial expression to set, e.g., 'happy', 'sad', 'angry'."},
                {"name": "intensity", "type": "string", "description": "The intensity of the expression, e.g., 'subtle', 'moderate', 'strong'."}
            ]
        },
        {
            "name" : "pose",
            "description" : "Set pose for the character. e.g., 'standing', 'sitting', 'lying down'.",
            "arguments": [
                {"name": "pose", "type": "string", "description": "The pose to set, e.g., 'standing', 'sitting', 'lying down'."},
                {"name": "action", "type": "string", "description": "Any specific action, e.g., 'running', 'jumping', 'dancing'."}
            ]
        }
    ]

@mcp.prompt("layout")
def layout_prompt(layout: str, framing: str):
    pass

@mcp.prompt("clothing")
def clothing_prompt(style: str, color: str, accessories: str):
    pass

@mcp.prompt("facial_expression")
def facial_expression_prompt(expression: str, intensity: str):
    pass

@mcp.prompt("pose")
def pose_prompt(pose: str, action: str):
    pass

@mcp.tool()
def layout_generator(layout: str, framing: str):
    pass

@mcp.tool()
def clothing_generator(style: str, color: str, accessories: str):
    pass

@mcp.tool()
def facial_expression_generator(expression: str, intensity: str):
    pass

@mcp.tool()
def pose_generator(pose: str, action: str):
    pass


if __name__ == "__main__":
    mcp.run("stdio")
    
