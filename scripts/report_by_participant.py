import pandas as pd

from data.settings import (
    WAVE1_DATA, WAVE2_DATA, SUBMISSIONS_URL,
    PARTICIPANTS_DATA)


def create_submission_url(submission_id):
    if pd.notna(submission_id):
        return f'https://admin.contest.yandex.ru/submissions/{submission_id}'
    return submission_id


def main():
    participants_data = pd.read_csv(PARTICIPANTS_DATA)
    # print(len(participants_data))
    # print(participants_data.head())

    inf_w1 = pd.read_csv(WAVE1_DATA)
    inf_w2 = pd.read_csv(WAVE2_DATA)

    talent_id = int(input("Введите TalentID пользователя: ").strip())
    # print(talent_id)
    # print(type(talent_id))

    row = participants_data[participants_data['TalentID'] == talent_id]
    if row.empty:
        print("TalentID не найден.")
        return

    user_id_wave1 = row['user_id_wave1'].values[0]
    user_id_wave2 = row['user_id_wave2'].values[0]

    report = pd.DataFrame(columns=['wave', 'task_id', 'user_id_1', 'user_id_2', 'submission_1', 'submission_2', 'overlap_percentage'])

    if pd.notna(user_id_wave1):
        df_wave1 = inf_w1[(inf_w1['user_id_1'] == user_id_wave1) | (inf_w1['user_id_2'] == user_id_wave1)].copy()
        df_wave1.loc[:, 'wave'] = 1
        df_wave1 = df_wave1.dropna(how='all')
        if not df_wave1.empty:
            report = pd.concat([report, df_wave1], ignore_index=True)

    if pd.notna(user_id_wave2):
        df_wave2 = inf_w2[(inf_w2['user_id_1'] == user_id_wave2) | (inf_w2['user_id_2'] == user_id_wave2)].copy()
        df_wave2.loc[:, 'wave'] = 2
        df_wave2 = df_wave2.dropna(how='all')  # Удаляем пустые строки
        if not df_wave2.empty:
            report = pd.concat([report, df_wave2], ignore_index=True)

    report['submission_1'] = report['submission_1'].apply(create_submission_url)
    report['submission_2'] = report['submission_2'].apply(create_submission_url)

    # print(report)
    report.to_csv(f'data/report{talent_id}.csv', sep=';', index=False) 

if __name__ == "__main__":
    main()
