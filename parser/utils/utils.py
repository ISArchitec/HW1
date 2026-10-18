def is_token_symbol(symbol: str, position: int) -> bool:
    """Check, that symbol can be a part of token (variable or assignment name)"""
    return symbol.isalpha() or symbol == "_" or (symbol.isdecimal() and position > 0)
