import pandas as pd


def read(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=';', header=0, parse_dates=[1], infer_datetime_format=True,
                     usecols=['Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee',
                              'Fee Currency'])
    df['Exchange'] = 'CoinMate'
    df['Type'] = df['Type'].replace({'QUICK_BUY': 'BUY', 'QUICK_SELL': 'SELL'})
    df1 = df.pipe(fix_types).pipe(normalize_withdrawals).pipe(calculate_total)
    return df1


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Fee'] = pd.to_numeric(df['Fee'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    return df


def normalize_withdrawals(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df.Type == 'WITHDRAWAL', 'Price Currency'] = df['Amount Currency']
    df.loc[df.Type == 'WITHDRAWAL', 'Fee Currency'] = df['Amount Currency']
    return df


def calculate_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    The field Total represents the total change to the secondary currency account.
    When buying it is Spend + Fee, when selling it is Received - Fee.
    When withdrawal and deposit, the amount is added to the primary account and the fee is subtracted from
    the secondary. This way the primary "Amount" still represents the value deposited/withdraw
    :param df: Original dataframe
    :return: Modified dataframe
    """

    df.loc[df.Type == 'SELL', 'Total'] = -1 * df['Amount'] * df['Price'] - df['Fee']
    df.loc[df.Type == 'BUY', 'Total'] = -1 * (df['Amount'] * df['Price'] + df['Fee'])
    df.loc[df.Type == 'WITHDRAWAL', 'Total'] = -df.Fee
    df.loc[df.Type == 'DEPOSIT', 'Total'] = -df.Fee

    return df
