#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple tool to re-format the exported CSV from the Länsförsäkringar Internet
banking site to the format that can be imported into YNAB.

Simply go to the account you want to export data for and click export.
"""
import argparse
import csv
import re

FIELD_NAMES = ["Date", "Payee", "Memo", "Outflow", "Inflow"]


def parse_lf_csv(csvpath, delimiter=";"):
    """Reads a Länsförsäkringar CSV export and parses it into a JSON array
    compatible with YNAB.
    """
    result = []
    with open(csvpath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if len(row) > 0 and re.search(r'\d{4}-\d{2}-\d{2}', row[0]):
                transaction = {
                    "Date": row[1],
                    "Payee": row[3] if not row[2][0:5] == 'Swish' else row[2],
                    "Inflow": row[4] if not row[4][0] == '-' else "",
                    "Outflow": row[4] if row[4][0] == '-' else "",
                    "Memo": "" if not row[2][0:5] == 'Swish' else row[3]
                }
                result.append(transaction)
    return result


def convert_lf_data(data, outfile, delimiter=",", header=True, date_filter=""):
    """Writes JSON formatted data from parse_lf_csv into a CSV file
    compatible with YNAB.
    """
    records = 0
    with open(outfile, "wb") as output:
        writer = csv.DictWriter(output, delimiter=delimiter, fieldnames=FIELD_NAMES)
        if header:
            writer.writeheader()
        for row in data:
            if "Transaktionsdag" in row["Date"]:
                continue
            if date_filter:
                if not date_filter in row["Date"]:
                    continue

            # Strip leading minus and any spaces. Ensure period as decimal point.
            row["Inflow"] = row["Inflow"].replace(" ", "").replace(",", ".")
            row["Outflow"] = row["Outflow"][1:].replace(" ", "").replace(",", ".")
            writer.writerow(row)
            records += 1
    return records

def main():
    """Main. Parse arguments and execute conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert Länsförsäkringar Excel (CSV) export to YNAB compatible CSV.",
        prog="pynablf.py")
    parser.add_argument('input', help="Input file from Länsförsäkringar")
    parser.add_argument('output', help="Output file for YNAB")
    parser.add_argument('-w', '--whitelist', help="White list dates. Eg. 2018-01")
    parser.add_argument('-q', '--quiet', action="store_true", help="Quiet")
    args = parser.parse_args()
    parsed_data = parse_lf_csv(args.input)
    num_records = 0
    num_records = convert_lf_data(parsed_data, args.output, date_filter=args.whitelist)
    if not args.quiet:
        print "R:%d <- %s\nW:%d -> %s" % (len(parsed_data), args.input, num_records, args.output)


if __name__ == '__main__':
    main()
