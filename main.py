import argparse
import functools
from functools import partial
import pandas as pd


coinmate_types = {'QUICK_BUY': 'BUY', 'QUICK_SELL': 'SELL'}


def table_translate(key: str, translation_table: {str: str}) -> str:
    return translation_table[key] if key in translation_table else key


def read_coinmate(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=';', header=0, parse_dates=[0], infer_datetime_format=True,
                     usecols=['Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee',
                              'Fee Currency'],
                     converters={'Type': partial(table_translate, translation_table=coinmate_types)})
    return df


def read_bitstamp(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, header=0, usecols=['Datetime', 'Sub Type', 'Amount', 'Value', 'Rate', 'Fee'],
                     parse_dates=[0], infer_datetime_format=True,
                     converters={'Sub Type': str.upper})\
        .rename(columns={'Rate': 'Price', 'Sub Type': 'Type', 'Datetime': 'Date'})
    df[['Amount', 'Amount Currency']] = df.Amount.str.split(' ', expand=True)
    df[['Price', 'Price Currency']] = df.Price.str.split(' ', expand=True)
    df[['Fee', 'Fee Currency']] = df.Fee.str.split(' ', expand=True)
    return df


def sort_df_cols(df1: pd.DataFrame) -> pd.DataFrame:
    return df1[['Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee', 'Fee Currency']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unify the format of crypto exchange logs')
    parser.add_argument('--input_format', required=True, help='Input format', choices=['bitstamp', 'coinmate'])
    parser.add_argument('input_file', type=str, help='Input file with data from supported exchange')
    args = parser.parse_args()

    parsers = {'bitstamp': read_bitstamp, 'coinmate': read_coinmate}
    data: pd.DataFrame = parsers[args.input_format](args.input_file)

    sort_df_cols(data).to_csv('out.csv', index=False, date_format='%Y-%m-%d %H:%M')
    print("Bye")
