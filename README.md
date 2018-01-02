# pynabsb
Command line script to re-format Swedbank transaction exports to YNAB CSV format.

## Usage
Login to Swedbank and go to the account you want and hit "Export". Use the downloaded CSV file as input.

```
$ ./pynabsb.py -h
usage: pynabsb.py [-h] [-w WHITELIST] [-q] input output

Convert Swedbank CSV export to YNAB compatible CSV.

positional arguments:
  input                 Input file from Swedbank
  output                Output file for YNAB

optional arguments:
  -h, --help            show this help message and exit
  -w WHITELIST, --whitelist WHITELIST
                        White list dates. Eg. 2018-01
  -q, --quiet           Quiet
```
