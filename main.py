from mcp.server.fastmcp import FastMCP
from typing import Dict
import httpx

# Initialize FastMCP server
mcp = FastMCP("Currency Converter Demo")

@mcp.tool()
async def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, float]:
    """Convert currency using FX Rates API
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
    
    Returns:
        Dictionary containing the converted amount and exchange rate
    """
    url = f"https://api.fxratesapi.com/convert"
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "places": 2
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        if not data.get("success"):
            return {
                "error": "Failed to convert currency",
            }
            
        return {
            "converted_amount": data["result"],
            "exchange_rate": data["info"]["rate"]
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")