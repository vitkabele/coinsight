import pandas as pd


def read(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, usecols=['Datetime', 'Type', 'Sub Type', 'Amount', 'Value', 'Rate', 'Fee'],
                     parse_dates=[0], infer_datetime_format=True,
                     converters={'Sub Type': str.upper, 'Type': str.upper}) \
        .rename(columns={'Rate': 'Price', 'Datetime': 'Date'})
    df['Exchange'] = 'BitStamp'

    df[['Amount', 'Amount Currency']] = df.Amount.str.split(' ', expand=True)
    df[['Price', 'Price Currency']] = df.Price.str.split(' ', expand=True)
    df[['Fee', 'Fee Currency']] = df.Fee.str.split(' ', expand=True)
    df1 = df.pipe(filter_types).pipe(normalize_withdrawals).pipe(normalize_fee).pipe(fix_types).pipe(calculate_total)
    df1.loc[df1['Type'] == 'SELL', 'Amount'] = -1 * df1['Amount']
    df1.loc[df1['Type'] == 'WITHDRAWAL', 'Amount'] = -1 * df1['Amount']
    return df1


def normalize_withdrawals(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df.Type == 'WITHDRAWAL', 'Price Currency'] = df['Amount Currency']
    df.loc[df.Type == 'WITHDRAWAL', 'Fee Currency'] = df['Amount Currency']
    return df


def filter_types(df: pd.DataFrame) -> pd.DataFrame:
    market_index = df['Type'] == 'MARKET'
    df.loc[market_index, 'Type'] = df['Sub Type']
    del df['Sub Type']
    wanted_index = df['Type'].str.contains('BUY|SELL|DEPOSIT|WITHDRAWAL')
    # Without the .copy() there is SettingWithCopyWarning which I do not fully understand since loc should only
    # return slice
    return df.loc[wanted_index].copy()


def normalize_fee(df: pd.DataFrame) -> pd.DataFrame:
    fee_index = df['Fee'].isnull()
    df.loc[fee_index, 'Fee'] = 0
    df.loc[fee_index, 'Fee Currency'] = df['Price Currency']
    return df


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    return df.astype({'Amount': float, 'Price': float, 'Fee': float})


def calculate_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    The field Total represents the total change to the secondary currency account.
    When buying it is Spend + Fee, when selling it is Received - Fee
    :param df: Original dataframe
    :return: Modified dataframe
    """
    index_loc = df['Fee Currency'] == df['Price Currency']
    df.loc[~index_loc, 'Fee'] = df['Fee'] * df['Price']

    df.loc[df.Type == 'SELL', 'Total'] = df['Amount'] * df['Price'] - df['Fee']
    df.loc[df.Type == 'BUY', 'Total'] = -1 * (df['Amount'] * df['Price'] + df['Fee'])
    df.loc[df.Type == 'WITHDRAWAL', 'Total'] = -df.Fee
    df.loc[df.Type == 'DEPOSIT', 'Total'] = -df.Fee

    return df
