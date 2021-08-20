import argparse
import pandas as pd
from Exchanges.Bitstamp import read as read_bitstamp
from Exchanges.Coinmate import read as read_coinmate


def sort_df_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df[['Exchange', 'Date', 'Type', 'Amount', 'Amount Currency', 'Price', 'Price Currency', 'Fee', 'Total']]


def print_stats(df: pd.DataFrame) -> None:
    grouped = df.groupby('Amount Currency')['Amount'].sum()
    sumtotal = df.groupby('Price Currency')['Total'].sum()
    print(grouped.add(sumtotal, fill_value=0).round(10))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unify the format of crypto exchange logs')
    parser.add_argument('input_files', type=str, help='Input file with data from supported exchange', nargs='+')
    parser.add_argument('-s', '--stats', action='store_true', help='Print various statistics for input data')
    parser.add_argument('-i', '--intermediate', action='store_true', help='Store processed output for each input file')
    parser.add_argument('-O', '--output', help='Output file', default='summary_results.csv')
    args = parser.parse_args()
    results = []

    for i in args.input_file:
        if i.startswith('bitstamp'):
            data = read_bitstamp(i)
        elif i.startswith('coinmate'):
            data = read_coinmate(i)
        else:
            print(f"Unknown file {i}")
            continue

        results.append(data)

        if args.stats:
            print(f'Results for {i}:')
            print_stats(data)

        if args.intermediate:
            data.pipe(sort_df_cols).to_csv(f'{i.removesuffix(".csv")}.processed.csv', index=False, date_format='%Y-%m-%d %H:%M', decimal=',', sep=';')

    combined_results = pd.concat(results).sort_values(by='Date')
    if args.stats:
        print('Summary statistics:')
        print_stats(combined_results)
    combined_results.pipe(sort_df_cols).to_csv(args.output, index=False, date_format='%Y-%m-%d %H:%M', decimal=',', sep=';')
