def precedence(op):
    if op in ('+', '-'): return 1
    if op in ('*', '/', '%'): return 2
    return 0

def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0: raise ZeroDivisionError("Div By Zero")
        return a / b
    if op == '%':
        if b == 0: raise ZeroDivisionError("Modulo By Zero")
        return a % b
    return 0

def evaluate(expression):
    if not expression: return "0"
    expression = expression.replace('×', '*').replace('÷', '/')
    tokens = []
    i = 0
    n = len(expression)
    if n > 0 and expression[0] in ('*', '/', '%'): raise ValueError("Invalid Start")
    while i < n:
        char = expression[i]
        if char == ' ':
            i += 1
            continue
        if char.isdigit() or char == '.':
            num_str = ""
            dot_count = 0
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                if expression[i] == '.':
                    dot_count += 1
                    if dot_count > 1: raise ValueError("Invalid Number")
                num_str += expression[i]
                i += 1
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
            continue
        if char in ('+', '-', '*', '/', '%'):
            tokens.append(char)
            i += 1
            continue
        raise ValueError(f"Invalid Char: {char}")
    if not tokens: return "0"
    if isinstance(tokens[-1], str): raise ValueError("Incomplete Expr")
    values, ops = [], []
    try:
        j = 0
        while j < len(tokens):
            token = tokens[j]
            if isinstance(token, (int, float)):
                values.append(token)
            else:
                while (ops and precedence(ops[-1]) >= precedence(token)):
                    if len(values) < 2: raise ValueError("Invalid Expr")
                    val2, val1, op = values.pop(), values.pop(), ops.pop()
                    values.append(apply_op(val1, val2, op))
                ops.append(token)
            j += 1
        while ops:
            if len(values) < 2: raise ValueError("Invalid Expr")
            val2, val1, op = values.pop(), values.pop(), ops.pop()
            values.append(apply_op(val1, val2, op))
        if not values: return "0"
        result = values[0]
        if isinstance(result, float) and result.is_integer(): return str(int(result))
        return f"{result:.8g}"
    except ZeroDivisionError as e: raise e
    except Exception: raise ValueError("Error")
