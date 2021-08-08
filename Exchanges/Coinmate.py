import pandas as pd


def read(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=';', header=0, parse_dates=[0], infer_datetime_format=True,
                     usecols=['Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee',
                              'Fee Currency'])
    df['Exchange'] = 'CoinMate'
    df['Type'].replace({'QUICK_BUY': 'BUY', 'QUICK_SELL': 'SELL'})
    return df
