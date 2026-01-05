import re
from pydantic import BaseModel
from typing import Dict, Any

_ALLOWED = re.compile(r"^[0-9\.\+\-\*\/\(\)\s]+$")

class CalculationInput(BaseModel):
    expression: str

def calculator_tool_call(data: Dict[str, Any]) -> Dict[str, Any]:
    expr = data["expression"]
    if not _ALLOWED.fullmatch(expr):
        return {"ok": False, "error": "Invalid expression"}

    return {"ok": True, "result": eval(expr, {"__builtins__": {}})}
