# pynablf
Command line script to re-format Länsförsäkringar bank transaction exports to YNAB CSV format.

## Usage
Login to Länsförsäkringar bank and go to the account you want and hit "Exporta till Excel". Use the downloaded CSV file as input.

## Credits
Original version for Swedbank by https://github.com/emilerl


```
$ ./pynablf.py -h
usage: pynablf.py [-h] [-w WHITELIST] [-q] input output

Convert Länsförsäkringar Excel (CSV) export to YNAB compatible CSV.

positional arguments:
  input                 Input file from Länsförsäkringar
  output                Output file for YNAB

optional arguments:
  -h, --help            show this help message and exit
  -w WHITELIST, --whitelist WHITELIST
                        White list dates. Eg. 2018-01
  -q, --quiet           Quiet
```
