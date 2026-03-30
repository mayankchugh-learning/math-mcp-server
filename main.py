#arith_server.py
from __future__ import annotations
from fastmcp import FastMCP

mcp = FastMCP("arithmetic")

def _as_number(x):
    # Accpet ints/floats or numeric strings; raise clean errorr otherwise
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        return float(x.strip())
    raise TypeError(f"Expeted a number (int/float or numeric string)")


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Return a + b"""
    return _as_number(a) + _as_number(b)

@mcp.tool()
async def subtract(a: float, b: float) -> float:
    return _as_number(a) - _as_number(b)

@mcp.tool()
async def multiply(a: float, b: float) -> float:
    return _as_number(a) * _as_number(b)

@mcp.tool()
async def divide(a: float, b: float) -> float:
    return _as_number(a) / _as_number(b)

@mcp.tool()
async def power(a: float, b: float) -> float:
    return _as_number(a) ** _as_number(b)

@mcp.tool()
async def modulus(a: float, b: float) -> float:
    return _as_number(a) % _as_number(b)

@mcp.tool()
async def floor_divide(a: float, b: float) -> float:
    return _as_number(a) // _as_number(b)

@mcp.tool()
async def absolute(a: float) -> float:
    return abs(_as_number(a))

# Start the server
if __name__ == "__main__":
    mcp.run()
