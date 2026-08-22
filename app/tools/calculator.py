import ast
import operator

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def safe_eval(node):
    if isinstance(node, ast.Num):  # Python < 3.8 compatibility
        return node.n
    elif isinstance(node, ast.Constant):  # Python >= 3.8
        return node.value
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not permitted.")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not permitted.")
    else:
        raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def calculate(expression: str) -> str:
    """Safely calculates arithmetic expressions for SLA, timing, and fee credits."""
    try:
        clean_expr = expression.replace(",", "").strip()
        parsed = ast.parse(clean_expr, mode='eval')
        res = safe_eval(parsed.body)
        return str(res)
    except Exception as e:
        return f"Calculation error: {str(e)}"