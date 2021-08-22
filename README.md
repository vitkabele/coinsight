# coINsight

Get insight on your crypto

Are you investing in crypto? Are you using multiple exchanges? Do you have hard time keeping order in your investments?

If you answered yes to the questions above, you might be interested in this project.
It is a data transformer of transaction history exported from different exchanges to unified format.
Such format can be further analysed, visualised or imported to other tools.

## Usage

1. Download the transaction log from your exchange(s) of choice
2. Run the `./main.py -O may-june.csv bitstamp-may.csv coinbase-june.csv`. This aggregates the two input files to single output `may-june.csv`.
The file must be prefixed with the name of exchange. This is how the script decides what parser to use.
Files may be placed in separate directories named by exchange and then passed as parameters as `bitstamp/*.csv coinbase/*.csv`.
When the files are named correctly this arrangement enables iteratively adding files i.e. by backing the exchange log each month.

### Supported input formats

* Bitstamp CSV
* Coinmate CSV
* Coinbase CSV (file header must be removed manually in advance)

### Output format

Output contains the following columns:

* Exchange
* Date: date in the format `%Y-%m-%d %H:%M`, e.g. `2021-08-08 17:24`
* Type: BUY, SELL, WITHDRAWAL, DEPOSIT
* Amount: The amount bought, sold etc.
* Amount Currency: The manipulated currency (typically BTC, ETH, ...)
* Price: 
* Fee:
* Price Currency: The second currency of the transaction (typically USD, EUR, ...). Also the currency of the fee
* Total: `Amount * Price + Fee [* Price]`
* Total Currency: Same as Price Currency