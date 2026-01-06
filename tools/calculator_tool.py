import re

_ALLOWED = re.compile(r"^[0-9\.\+\-\*\/\(\)\s]+$")

def calculator_tool_call(data):
    expr = data["expression"]
    if not _ALLOWED.fullmatch(expr):
        return {"ok": False, "error": "Invalid expression"}
    return {"ok": True, "result": eval(expr, {"__builtins__": {}})}
