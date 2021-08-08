# Crypto portfolio analyser

Are you investing in crypto? Are you using multiple exchanges? Do you have hard time keeping order in your investments?

If you answeared yes to the questions above, you might be interested in this project.

## What is it 

This project aims to convert exported CSV transaction history to unified format.
Such format can be further analysed, visualised or imported to other tools.

### Supported input formats

* Bitstamp exported CSV
* Coinmate exported CSV

### Output format

Output contains the following columns:

* Date: date in the format `%Y-%m-%d %H:%M`, e.g. `2021-08-08 17:24`
* Type: BUY, SELL, WITHDRAWAL, DEPOSIT
* Amount: The amount bought, sold etc.
* Amount Currency: The manipulated currency (typically BTC, ETH, ...)
* Price: 
* Fee:
* Price Currency: The second currency of the transaction (typically USD, EUR, ...). Also the currency of the fee
* Total: `Amount * Price + Fee [* Price]`
* Total Currency: Same as Price Currency