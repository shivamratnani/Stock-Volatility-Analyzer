def log_failed_analysis(symbol: str, period: str, error: str) -> None:
    """Log failed analysis attempts"""
    with open('failed_analysis.txt', 'a') as f:
        f.write(f"{symbol}: {error}\n") 