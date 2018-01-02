#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pynabsb


TESTCSV = """SKYDDAT BELOPP;2018-01-01;-46,00;-
SKYDDAT BELOPP;2018-01-01;-46,00;-
MAXI ICA STORMAR;2018-01-02;-1 551,10;10
LF;2018-01-02;-484,00;19"""

TESTCSV_RESULT = "Date,Payee,Memo,Outflow,Inflow\r\n2018-01-01,SKYDDAT BELOPP,,46.00,\r\n2018-01-01,SKYDDAT BELOPP,,46.00,\r\n2018-01-02,MAXI ICA STORMAR,,1551.10,\r\n2018-01-02,LF,,484.00,\r\n"
TESTCSV_RESULT_DATEFILTER = "Date,Payee,Memo,Outflow,Inflow\r\n2018-01-01,SKYDDAT BELOPP,,46.00,\r\n2018-01-01,SKYDDAT BELOPP,,46.00,\r\n"
TESTQIF_RESULT="""!Type:Bank
D2018-01-01
T-46.00
PSKYDDAT BELOPP
^
!Type:Bank
D2018-01-01
T-46.00
PSKYDDAT BELOPP
^
!Type:Bank
D2018-01-02
T-1551.10
PMAXI ICA STORMAR
^
!Type:Bank
D2018-01-02
T-484.00
PLF
^
"""

class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        self.csvpath = "/tmp/transactions.csv"
        self.outpath = "/tmp/results.csv"
        self.outpath_qif = "/tmp/results.qif"
        with open(self.csvpath, "wb") as csvfile:
            csvfile.write(TESTCSV)

    def test_parse_simple(self):
        data = pynabsb.parse_sb_csv(self.csvpath)
        self.assertEquals(4, len(data))

    def test_parse_contents(self):
        data = pynabsb.parse_sb_csv(self.csvpath)
        self.assertEquals("SKYDDAT BELOPP", data[0]["Payee"])
        self.assertEquals("2018-01-01", data[0]["Date"])
        self.assertEquals("-46,00", data[0]["Outflow"])
        self.assertEquals("", data[0]["Inflow"])
        self.assertEquals("", data[0]["Memo"])

    def test_conversion(self):
        data = pynabsb.parse_sb_csv(self.csvpath)
        pynabsb.convert_sb_data(data, self.outpath)

        result = None
        with open(self.outpath, "rb") as outfile:
            result = outfile.read()

        self.assertEquals(TESTCSV_RESULT, result)

    def test_conversion_date_filter(self):
        data = pynabsb.parse_sb_csv(self.csvpath)
        pynabsb.convert_sb_data(data, self.outpath, date_filter="2018-01-01")

        result = None
        with open(self.outpath, "rb") as outfile:
            result = outfile.read()

        self.assertEquals(TESTCSV_RESULT_DATEFILTER, result)

    def test_qif(self):
        data = pynabsb.parse_sb_csv(self.csvpath)
        pynabsb.convert_sb_data_qif(data, self.outpath_qif)

        result = None
        with open(self.outpath_qif, "rb") as outfile:
            result = outfile.read()

        self.assertEquals(TESTQIF_RESULT, result)

    def tearDown(self):
        if os.path.exists(self.csvpath):
            os.unlink(self.csvpath)
        if os.path.exists(self.outpath):
            os.unlink(self.outpath)
        if os.path.exists(self.outpath_qif):
            os.unlink(self.outpath_qif)

if __name__ == '__main__':
    unittest.main()
