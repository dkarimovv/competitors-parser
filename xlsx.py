import os
import pandas as pd
from datetime import datetime

def create_csv(inns: list, data: list, flag: str):
    # Столбцы, которые нам нужны для итоговой таблицы
    headers = ['Конкурент', 'Страница', 'Инфомарция']
    
    # Создаем название файла только с сегодняшней датой
    today_date = datetime.now().strftime("%Y_%m_%d")
    output = f'reports/output_{today_date}.csv'
    
    # Проверяем, существует ли папка 'reports', если нет, создаем ее
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    if flag == 'all_data':
        print('Создаем таблицу с полной информацией')
        output = output.replace('output', 'all_data')
    elif flag == 'actual_data':
        print('Создаем таблицу с самой актуальной информацией')
        output = output.replace('output', 'actual_data')

    combined_data = []  # Сюда будем собирать все данные

    for inn, inn_data in zip(inns, data):
        if not inn_data: 
            continue

        # Берем последнюю запись
        last_record = inn_data[0] 
        selected_record = [inn, last_record[0], last_record[1]]

        combined_data.append(selected_record)

    # Создаем DataFrame только с нужными столбцами
    df = pd.DataFrame(combined_data, columns=headers)

    # Сохраняем данные в CSV файл
    df.to_csv(output, index=False)
    
    print(f"Данные успешно записаны в файл {output}")
