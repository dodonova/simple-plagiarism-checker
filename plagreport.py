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
    -r, --report    : Name of the report file. Default: report_[current_datetime].csv
    -p, --min-percent : Minimum overlap percentage for reporting. Default: 60
    -s, --min-size   : Minimum text length for analysis. Default: 140

Example:
    python plagreport.py -f /path/to/your/folder -r custom_report.csv -p 70  -t txt,py
"""

import argparse
import os
import re
import pandas as pd
from itertools import combinations
from zlib import compress
from tqdm import tqdm
import logging
import tempfile
import zipfile
import time
from datetime import datetime
import concurrent.futures


MIN_PERCENTAGE = 80
REPORT_NAME = 'report'
DEFAULT_MIN_SIZE = 140
YANDEX_FORMAT = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

compressed_text_cache = {}


def get_overlap_percentage(text1, text2):
    if text1 not in compressed_text_cache:
        compressed_text_cache[text1] = len(compress(text1.encode('utf-8')))
    if text2 not in compressed_text_cache:
        compressed_text_cache[text2] = len(compress(text2.encode('utf-8')))

    compressed_both = compress((text1 + text2).encode('utf-8'))
    compressed_individual = (compressed_text_cache[text1] +
                             compressed_text_cache[text2])

    overlap_percentage = (
        (compressed_individual - len(compressed_both)) /
        compressed_individual * 2 * 100
    )
    return overlap_percentage


def get_overlap_percentage_v1(text1, text2):
    compressed_both = compress((text1 + text2).encode('utf-8'))
    compressed_individual = (len(compress(text1.encode('utf-8'))) +
                             len(compress(text2.encode('utf-8'))))
    overlap_percentage = (
        (compressed_individual - len(compressed_both)) /
        compressed_individual * 2 * 100
    )
    return overlap_percentage


def get_submissions(archive_path, min_size):
    """
    Распаковывает архив с посылками из Яндекс Контеста.
    Создает JSON  со всеми данными из архива посылок.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        file_list = []
        submissions = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                relative_path = os.path.relpath(file_path, temp_dir)
                if file_size >= min_size:
                    file_list.append((relative_path, file_size))

                    if YANDEX_FORMAT:
                        match = re.search(r'.+\/(.+)\/(\w+)-(\d+)-', file_path)
                        if match:
                            user_id = match.group(1)
                            task_id = match.group(2)
                            submission_id = match.group(3)
                        else:
                            logging.error((f'Имя файла  не соответствует правилу именования архива решений из Яндекс Контест: {file_path}'))
                            continue

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            submission_text = f.read()
                    except Exception as e:
                        logging.error(f"Ошибка {e} при чтении файла \n{file_path}")

                        submission_text = ''

                    if YANDEX_FORMAT:
                        submissions.append({
                            'filename': relative_path,
                            'user_id': user_id,
                            'task_id': task_id,
                            'submission_id': submission_id,
                            'submission_text': submission_text
                        })
                    else:
                        submissions.append({
                            'filename': relative_path,
                            'submission_text': submission_text
                        })

        return submissions


def create_report(report_filename, report_data):
    if report_filename is None:
        folder_path = os.path.join(os.getcwd(), 'reports')
        os.makedirs(folder_path, exist_ok=True)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{folder_path}/{REPORT_NAME}_{current_datetime}.csv"

    report_df = pd.DataFrame(report_data)
    report_df.to_csv(report_filename, index=False)
    return report_filename


def check_plagiarism(submissions, min_percentage, report_filename):
    """
    Проверяет все посылки в списке submissions на списывание и создает список для отчета.
    """

    # submissions_df.to_csv('all_submissions.csv', index=False)
    report = []


    if YANDEX_FORMAT:
        submissions_df = pd.DataFrame(submissions)
        task_count = submissions_df['task_id'].nunique()
        logging.info('Анализируем данные в формате Яндекс Контест')
        logging.info(f'Количество анализируемых задач: {task_count}')

        def process_pair(task_list, i, j):
            if task_list[i]['user_id'] != task_list[j]['user_id']:
                overlap_percentage = get_overlap_percentage(
                    task_list[i]['submission_text'],
                    task_list[j]['submission_text']
                )
                if overlap_percentage > min_percentage:
                    return {
                        'task_id': task_list[i]['task_id'],
                        'user_id_1': task_list[i]['user_id'],
                        'user_id_2': task_list[j]['user_id'],
                        'filename_1': task_list[i]['filename'],
                        'filename_2': task_list[j]['filename'],
                        'overlap_percentage': overlap_percentage
                    }
            return None

        for task_id in submissions_df['task_id'].unique():
            task_df = submissions_df[submissions_df['task_id'] == task_id]
            task_list = task_df.to_dict(orient='records')

            pairs = [(task_list, i, j) for i in range(len(task_list)) for j in range(i + 1, len(task_list))]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(tqdm(executor.map(lambda p: process_pair(*p), pairs),
                                    desc=f"Задача {task_id}. Обработка файлов",
                                    leave=True))
                report.extend([result for result in results if result])
            
            # for i in tqdm(range(len(task_list)),
            #               desc=f"Задача {task_id}. Обработка файлов",
            #               leave=True):
            #     for j in range(i+1, len(task_list)):
            #         if task_list[i]['user_id'] != task_list[j]['user_id']:
            #             overlap_percentage = get_overlap_percentage(
            #                 task_list[i]['submission_text'],
            #                 task_list[j]['submission_text']
            #             )
            #             if overlap_percentage > min_percentage:
            #                 report.append({
            #                     'task_id': task_list[i]['task_id'],
            #                     'user_id_1': task_list[i]['user_id'],
            #                     'user_id_2': task_list[j]['user_id'],
            #                     'filename_1': task_list[i]['filename'],
            #                     'filename_2': task_list[j]['filename'],
            #                     'overlap_percentage': overlap_percentage
            #                 })

    else:
        logging.info('Данные не в формате архива решений Яндекс контест')
        for i in range(len(submissions)):
            for j in range(i + 1, len(submissions)):
                submission1 = submissions[i]['submission_text']
                submission2 = submissions[j]['submission_text']
                overlap_percentage = get_overlap_percentage(
                    submission1, submission2
                )
                if overlap_percentage > min_percentage:
                    report.append({
                        'filename_1': submissions[i]['filename'],
                        'filename_2': submissions[j]['filename'],
                        'overlap_percentage': overlap_percentage
                    })

    return create_report(report_filename, report)


def main(archive_filename, min_size, min_percentage, report_filename):
    submissions = get_submissions(archive_filename, min_size)
    report = check_plagiarism(submissions, min_percentage, report_filename)
    print(f"Был создан отчет: {report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Проверяет посылки из Яндекс Контеста на списывание.")

    parser.add_argument('archive',
                        help="Путь к архиву для обработки")

    parser.add_argument('-p', '--min_percent',
                        type=float,
                        default=MIN_PERCENTAGE,
                        help=(f'Минимальный процент совпадения. '
                              f'По умолчанию: {MIN_PERCENTAGE}'))
    parser.add_argument('-s', '--min_size',
                        type=int,
                        default=100,
                        help=(f'Минимальный размер файла в байтах. '
                              f'По умолчанию: {DEFAULT_MIN_SIZE}'))
    parser.add_argument('-r', '--report_name',
                        type=str,
                        default=None,
                        help="Имя файла отчета")
    parser.add_argument('-y', '--yandex',
                        action='store_true',
                        dest='yandex_format',
                        help='Указать если данные не в формате Яндекс Контест')
    args = parser.parse_args()

    if hasattr(args, 'yandex_format'):
        YANDEX_FORMAT = args.yandex_format

    main(args.archive, args.min_size, args.min_percent, args.report_name)

    logging.info('Отчет успешно создан')
