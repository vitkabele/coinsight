import argparse
import pandas as pd
from Exchanges.Bitstamp import read as read_bitstamp
from Exchanges.Coinmate import read as read_coinmate


def sort_df_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df[['Exchange', 'Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee', 'Total']]


def print_stats(df: pd.DataFrame) -> None:
    grouped = df.groupby('Amount Currency')['Amount'].sum()
    sumtotal = df.groupby('Price Currency')['Total'].sum()
    print("Holdings:")
    print(grouped.add(sumtotal, fill_value=0).round(10))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unify the format of crypto exchange logs')
    parser.add_argument('input_file', type=str, help='Input file with data from supported exchange', nargs='+')
    args = parser.parse_args()

    for i in args.input_file:
        if i.startswith('bitstamp'):
            data = read_bitstamp(i)
        elif i.startswith('coinmate'):
            data = read_coinmate(i)

        print_stats(data)
        data.pipe(sort_df_cols).to_csv(f'{i}.processed.csv', index=False, date_format='%Y-%m-%d %H:%M', decimal=',', sep=';')

