import pandas as pd

def display_dataframe(df: pd.DataFrame, title: str = ""):
    """format and display dataframes"""
    if df.empty:
        print("\nNo data available")
        return
        
    if title:
        print(f"\n{title}")
    print("-" * 80)
    
    if 'Change%' in df.columns:
        df = df.copy()
        df['Change%'] = df['Change%'].apply(lambda x: f"{x:+.2f}%")
        df['Start Price'] = df['Start Price'].apply(lambda x: f"${x:,.2f}")
        df['End Price'] = df['End Price'].apply(lambda x: f"${x:,.2f}")
        df['Volume'] = df['Volume'].apply(lambda x: f"{x:,}")
    
    print(df.to_string(index=False))
    print("-" * 80)

def validate_dates(start_date: str, end_date: str):
    # Your existing validate_dates implementation here
    pass