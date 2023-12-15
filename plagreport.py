"""
Plagiarism Checker

This script checks overlap in the text files within a specified folder.

Usage:
    python plagreport.py -f /path/to/your/folder
                          [-r report_name]
                          [-p minimum_percentage]
                          [-s minimum_size]
                          [-t file_types]

Arguments:
    -f, --folder    : Path to the folder containing text files. Default: current directory (.)
    -r, --report    : Name of the report file. Default: report_[current_datetime].csv
    -p, --min-percent : Minimum overlap percentage for reporting. Default: 60
    -s, --min-size   : Minimum text length for analysis. Default: 140
    -t, --types     : File types to check (comma-separated). Default: txt,py,cpp,c,js,cs,csv

Example:
    python plagreport.py -f /path/to/your/folder -r custom_report.csv -p 70  -t txt,py
"""

import os
from zlib import compress
import argparse
from datetime import datetime

MIN_PERCENTAGE = 60
DEFAULT_FILE_TYPES = 'txt,py,cpp,c,js,cs,csv'
REPORT_NAME = 'report'
DEFAULT_MIN_SIZE = 140

min_size = DEFAULT_MIN_SIZE

def overlap_percentage(file1, file2):
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            text1 = f1.read().encode()
            text2 = f2.read().encode()
    except:
        return 0

    if len(text1) < min_size or len(text2) < min_size:
        return 0

    compressed_both = compress((text1 + text2))
    compressed_individual = compress(text1) + compress(text2)
    overlap_percentage = (
            (len(compressed_individual) - len(compressed_both)) /
            len(compressed_individual) * 2 * 100
    )
    return overlap_percentage

def check_plagiarism(
        folder_path,
        report_file=None,
        min_percentage=MIN_PERCENTAGE,
        file_types=None
):
    if report_file is None:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{REPORT_NAME}_{current_datetime}.csv"

    if file_types is None:
        files = [f for f in os.listdir(folder_path)]
    else:
        files = [
            f for f in os.listdir(folder_path)
            if f.endswith(tuple(file_types))
        ]

    with open(report_file, 'w') as report:
        report.write("File1;File2;Overlap Percentage\n")

        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1 = os.path.join(folder_path, files[i])
                file2 = os.path.join(folder_path, files[j])

                percentage = overlap_percentage(file1, file2)

                if percentage >= min_percentage:
                    report.write(f"{files[i]};{files[j]};{percentage:.2f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='check plagiarism in text files.')
    parser.add_argument(
        '-f', '--folder', type=str, default='.',
        help='Path to the folder containing text files')
    parser.add_argument(
        '-r', '--report', type=str, default=None,
        help='name of the report file')
    parser.add_argument(
        '-p', '--min-percent', type=float, default=MIN_PERCENTAGE,
        help=(f'minimum overlap percentage for reporting. '
              f'Default: {MIN_PERCENTAGE}'))
    parser.add_argument(
        '-s', '--min-size', type=float, default=MIN_PERCENTAGE,
        help=f'minimum text length for analyzing. Default: {DEFAULT_MIN_SIZE}')
    parser.add_argument(
        '-t', '--types', type=str, default=None,
        help=f'file types to check (comma-separated)')

    args = parser.parse_args()

    folder_path = args.folder
    report_file = args.report
    min_percentage = args.min_percent
    min_size = args.min_size
    file_types = None if args.types is None else args.types.split(',')

    check_plagiarism(folder_path, report_file, min_percentage, file_types)
    print('Report successfully done.')
