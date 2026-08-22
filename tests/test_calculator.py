from app.tools.calculator import calculate

def test_calculator_basic_arithmetic():
    assert calculate("250 + 50") == "300"
    assert calculate("500 * 0.10") == "50.0"
    assert calculate("(1000 - 250) / 2") == "375.0"

def test_calculator_blocks_arbitrary_code():
    res = calculate("__import__('os').system('ls')")
    assert "error" in res.lower() or "not permitted" in res.lower()