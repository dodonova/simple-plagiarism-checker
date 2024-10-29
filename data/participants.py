import pandas as pd
import re
# import glob

# csv_files = glob.glob('*.csv')

FILE_LIST = [
    'reports/inf-w2-A.csv',
    'reports/inf-w2-B.csv',
    'reports/inf-w2-C.csv',
    'reports/inf-w2-D.csv',
    'reports/inf-w2-E.csv',
]

csv_files = FILE_LIST

all_data = []

def process_user_id(user_id):
    return user_id[-9:]


def process_filename(filename):
    match = re.search(r'(\d{9})(?!.*\d{9})', filename)
    return match.group(1) if match else filename




for file in csv_files:
    df = pd.read_csv(file)

    df['user_id_1'] = df['user_id_1'].apply(process_user_id)
    df['user_id_2'] = df['user_id_2'].apply(process_user_id)
    
    df['filename_1'] = df['filename_1'].apply(process_filename)
    df['filename_2'] = df['filename_2'].apply(process_filename)
    
    all_data.append(df)

combined_data = pd.concat(all_data, ignore_index=True)
combined_data.to_csv('inf-w2-ALL.csv', index=False)
print("Отчет успешно сохранен в report.csv")
