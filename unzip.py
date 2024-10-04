import os
import csv
import zipfile
import argparse
import tempfile
import time


def create_report(file_list, report_name):
    with open(report_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path', 'Size (Bytes)'])
        for file_path, file_size in file_list:
            writer.writerow([file_path, file_size])


def process_archive(archive_path, min_size, report_name):

    archive_name = archive_path.split('/')[-1]

    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        file_list = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                relative_path = os.path.relpath(file_path, temp_dir)
                if file_size >= min_size:
                    file_list.append((relative_path, file_size))

        if not report_name:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            report_name = f'report-{archive_name}-{timestamp}.csv'

        create_report(file_list, report_name)
        print(f"Отчет успешно создан: {report_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Программа для создания отчета по архиву.")

    parser.add_argument('archive',
                        help="Путь к архиву для обработки")

    parser.add_argument('-s', '--min_size',
                        type=int, default=0,
                        default=100,
                        help="Минимальный размер файла для учета (в байтах)")
    parser.add_argument('-r', '--report_name',
                        type=str,
                        default=None,
                        help="Имя файла отчета")

    args = parser.parse_args()

    process_archive(args.archive, args.min_size, args.report_name)


if __name__ == "__main__":
    main()
