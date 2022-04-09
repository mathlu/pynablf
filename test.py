#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pynablf


TESTCSV = """\"Kontonummer\";\"Kontonamn\";\"\";\"Saldo\";\"Tillgängligt belopp\"
\"123456789\";\"Privatkonto\";\"\";\"99 999,99\";\"11 222,33\"

\"Bokföringsdatum\";\"Transaktionsdatum\";\"Transaktionstyp\";\"Meddelande\";\"Belopp\"
\"2022-01-12\";\"2022-01-11\";\"Kortköp\";\"Wolt,Stockholm,SE\";\"-164,00\"
\"2022-01-12\";\"2022-01-11\";\"Kortköp\";\"PAYPAL *AMAGICOM AB,35314369001,SE\";\"-53,85\"
\"2022-01-11";\"2022-01-10\";\"Kortköp\";\"COOP SALUHALLEN,NORRKÖPING,SE\";\"-45,95\""""

TESTCSV_RESULT = "Date,Payee,Memo,Outflow,Inflow\r\n2022-01-11,\"Wolt,Stockholm,SE\",,164.00,\r\n2022-01-11,\"PAYPAL *AMAGICOM AB,35314369001,SE\",,53.85,\r\n2022-01-10,\"COOP SALUHALLEN,NORRKÖPING,SE\",,45.95,\r\n"

TESTCSV_RESULT_DATEFILTER = "Date,Payee,Memo,Outflow,Inflow\r\n2022-01-10,\"COOP SALUHALLEN,NORRK\xc3\x96PING,SE\",,45.95,\r\n"

class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        self.csvpath = "/tmp/transactions.csv"
        self.outpath = "/tmp/results.csv"
        with open(self.csvpath, "wb") as csvfile:
            csvfile.write(TESTCSV)

    def test_parse_simple(self):
        data = pynablf.parse_lf_csv(self.csvpath)
        self.assertEquals(3, len(data))

    def test_parse_contents(self):
        data = pynablf.parse_lf_csv(self.csvpath)
        self.assertEquals("Wolt,Stockholm,SE", data[0]["Payee"])
        self.assertEquals("2022-01-11", data[0]["Date"])
        self.assertEquals("-164,00", data[0]["Outflow"])
        self.assertEquals("", data[0]["Inflow"])
        self.assertEquals("", data[0]["Memo"])

    def test_conversion(self):
        data = pynablf.parse_lf_csv(self.csvpath)
        pynablf.convert_lf_data(data, self.outpath)

        result = None
        with open(self.outpath, "rb") as outfile:
            result = outfile.read()

        self.assertEquals(TESTCSV_RESULT, result)

    def test_conversion_date_filter(self):
        data = pynablf.parse_lf_csv(self.csvpath)
        pynablf.convert_lf_data(data, self.outpath, date_filter="2022-01-10")

        result = None
        with open(self.outpath, "rb") as outfile:
            result = outfile.read()

        self.assertEquals(TESTCSV_RESULT_DATEFILTER, result)

    def tearDown(self):
        if os.path.exists(self.csvpath):
            os.unlink(self.csvpath)
        if os.path.exists(self.outpath):
            os.unlink(self.outpath)

if __name__ == '__main__':
    unittest.main()
