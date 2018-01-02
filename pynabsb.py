#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple tool to re-format the exported CSV from the Swedbank Internet
banking site to the format that can be imported into YNAB.

Simply go to the account you want to export data for and click export.
"""
import argparse
import csv

FIELD_NAMES = ["Date", "Payee", "Memo", "Outflow", "Inflow"]


def parse_sb_csv(csvpath, delimiter=";"):
    """Reads a Swedbank CSV export and parses it into a JSON array
    compatible with YNAB.
    """
    result = []
    with open(csvpath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            transaction = {
                "Date": row[1],
                "Payee": row[0],
                "Inflow": row[2] if not row[2][0] == '-' else "",
                "Outflow": row[2] if row[2][0] == '-' else "",
                "Memo": ""
            }
            result.append(transaction)
    return result


def convert_sb_data(data, outfile, delimiter=",", header=True, date_filter=""):
    """Writes JSON formatted data from parse_sb_csv into a CSV file
    compatible with YNAB.
    """
    records = 0
    with open(outfile, "wb") as output:
        writer = csv.DictWriter(output, delimiter=delimiter, fieldnames=FIELD_NAMES)
        if header:
            writer.writeheader()
        for row in data:
            if date_filter:
                if not date_filter in row["Date"]:
                    continue

            # Strip leading minus and any spaces. Ensure period as decimal point.
            row["Inflow"] = row["Inflow"].replace(" ", "").replace(",", ".")
            row["Outflow"] = row["Outflow"][1:].replace(" ", "").replace(",", ".")
            writer.writerow(row)
            records += 1
    return records


def convert_sb_data_qif(data, outfile, date_filter=""):
    """Writes JSON formatted data from parse_sb_csv into a QIF file
    compatible with YNAB.
    """
    def _create_qif_record(date, amount, payee):
        return """!Type:Bank
D%s
T%s
P%s
^
""" % (date, amount, payee)
    records = 0
    with open(outfile, "wb") as output:
        for row in data:
            if date_filter:
                if not date_filter in row["Date"]:
                    continue
            # Strip any spaces. Ensure period as decimal point.
            row["Inflow"] = row["Inflow"].replace(" ", "").replace(",", ".")
            row["Outflow"] = row["Outflow"].replace(" ", "").replace(",", ".")
            output.write(
                _create_qif_record(
                    row["Date"],
                    row["Outflow"] if row["Outflow"] else row["Inflow"],
                    row["Payee"]))
            records += 1
    return records


def main():
    """Main. Parse arguments and execute conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert Swedbank CSV export to YNAB compatible CSV.",
        prog="pynabsb.py")
    parser.add_argument('input', help="Input file from Swedbank")
    parser.add_argument('output', help="Output file for YNAB")
    parser.add_argument('-w', '--whitelist', help="White list dates. Eg. 2018-01")
    parser.add_argument('--qif', action="store_true", help="Output in QIF format.")
    parser.add_argument('-q', '--quiet', action="store_true", help="Quiet")
    args = parser.parse_args()
    parsed_data = parse_sb_csv(args.input)
    num_records = 0
    if args.qif:
        num_records = convert_sb_data_qif(parsed_data, args.output, date_filter=args.whitelist)
    else:
        num_records = convert_sb_data(parsed_data, args.output, date_filter=args.whitelist)
    if not args.quiet:
        print "R:%d <- %s\nW:%d -> %s" % (len(parsed_data), args.input, num_records, args.output)


if __name__ == '__main__':
    main()
