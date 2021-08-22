import pandas as pd


def read(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, parse_dates=['Timestamp'], converters={'Transaction Type': str.upper})
    df['Exchange'] = 'CoinBase'
    del df['Notes']
    df1 = df.pipe(get_primary_currency).pipe(rename_cols).pipe(fix_total)
    df1['Type'] = df1['Type'].replace({'RECEIVE': 'DEPOSIT', 'SEND': 'WITHDRAWAL'})
    return df1


def rename_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        'Timestamp': 'Date',
        'Transaction Type': 'Type',
        'Quantity Transacted': 'Amount',
        'Asset': 'Amount Currency',
        df.columns[4]: 'Price',
        df.columns[5]: 'Total',
        df.columns[6]: 'Fee',
    })


def get_primary_currency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Coinbase allows user to trade with only one primary currency and therefore it puts the name
    of the currency in column headers

    :param df: DataFrame
    :return: modified DataFrame
    """
    subtotal = df.columns[5].split()[0]
    fees = df.columns[7].split()[0]
    assert fees == subtotal
    df['Price Currency'] = fees
    del df[df.columns[5]]
    return df


def fix_total(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df['Type'] == 'BUY', 'Total'] = -1 * df['Total']
    df.loc[df['Type'] == 'SELL', 'Amount'] = -1 * df['Amount']
    df.loc[df['Type'] == 'SEND', 'Amount'] = -1 * df['Amount']
    return df
