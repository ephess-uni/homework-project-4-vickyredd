from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
import csv


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_date = date_obj.strftime('%d %b %Y')
        reformatted_dates.append(reformatted_date)
    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_objects = [start_date + timedelta(days=i) for i in range(n)]
    return date_objects


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_objects = date_range(start_date, len(values))
    result = [(date, value) for date, value in zip(date_objects, values)]
    return result


def fees_report(infile, outfile):
    """
    Calculates late fees per patron id and writes a summary report to outfile.
    """
    fees_dict = defaultdict(float)

    # Read input CSV file and calculate late fees
    with open(infile, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            patron_id = row['patron_id']
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                fees_dict[patron_id] += late_fee

    # Ensure all patrons have a fee entry
    all_patrons = set()
    with open(infile, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_patrons.add(row['patron_id'])
    for patron in all_patrons:
        fees_dict[patron]  # Ensure every patron has an entry

    # Write summary report to output CSV file
    with open(outfile, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, late_fee in fees_dict.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(late_fee)})



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
