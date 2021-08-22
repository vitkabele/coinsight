import unittest
import pandas.api.types as ptypes
import pandas as pd

from Exchanges.Bitstamp import read as read_bitstamp
from Exchanges.Coinmate import read as read_coinmate
from Exchanges.Coinbase import read as read_coinbase


class TestFormat(unittest.TestCase):

    def check_output(self, df: pd.DataFrame):
        self.assertTrue(ptypes.is_string_dtype(df['Exchange']))
        self.assertTrue(ptypes.is_datetime64_any_dtype(df['Date']))
        self.assertTrue(ptypes.is_string_dtype(df['Type']))
        self.assertTrue(ptypes.is_numeric_dtype(df['Amount']))
        self.assertTrue(ptypes.is_string_dtype(df['Amount Currency']))
        self.assertTrue(ptypes.is_numeric_dtype(df['Price']))
        self.assertTrue(ptypes.is_numeric_dtype(df['Fee']))
        self.assertTrue(ptypes.is_string_dtype(df['Price Currency']))
        self.assertTrue(ptypes.is_numeric_dtype(df['Total']))

    def test_bitstamp(self):
        x = read_bitstamp("tests/bitstamp.csv")
        self.check_output(x)

    def test_coinmate(self):
        x = read_coinmate("tests/coinmate.csv")
        self.check_output(x)

    def test_coinbase(self):
        x = read_coinbase("tests/coinbase.csv")
        self.check_output(x)


