import os
import time
import pandas as pd
import json
import re
from datetime import datetime
import glob

# start time of function
start_time = time.time()

# working directory
cwd = str(os.getcwd())

# Wczytanie pliku JSON

# --------------------------------------------------------------------------------------------------------------------------------
# loading multiple files
files = glob.glob(cwd + '/data/raw/*.json')

print(files)

data_list = []
for file_path in files:
    with open(file_path, 'r') as file:
        data = json.load(file)
        data_list.append(data)

print('dataframes count:', len(data_list))

# with open('paragon_2410097854165160.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)  # Zdeserializowanie zawartości pliku do obiektu Python

df_list = []

for data in data_list:
    # wyciągniecie timestamp i zmiana w date object
    date_string = data['header'][2]['headerData']['date']
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    # wyciągamy datę w formacie RRRR-MM-DD
    date_value = date_object.strftime("%Y-%m-%d")

    # wyciągamy czas w formacie HH:MM:SS
    time_value = date_object.strftime("%H:%M:%S")

    print("Data:", date_value)
    print("Czas:", time_value)

    items = data['body']

    # Lista na wiersze DataFrame
    rows = []

    # Tymczasowy słownik na dane sellLine
    current_sell_line = None

    # Iterowanie po danych
    for item in items:
        if 'sellLine' in item:
            # Zapisujemy sellLine od razu jako nowy wiersz bez discountLine
            current_sell_line = item['sellLine']
            row = {
                'date': date_value,
                'time': time_value,
                'product_name_raw': current_sell_line['name'],
                'vatId': current_sell_line['vatId'],
                'price': current_sell_line['price'],
                'total': current_sell_line['total'],
                'quantity': current_sell_line['quantity'],
                'discount_base': None,  # Wypełnimy to, jeśli znajdziemy discountLine
                'discount_value': None,
                'isDiscount': None,
                'isPercent': None
            }
            rows.append(row)
        elif 'discountLine' in item and len(rows) > 0:
            # Aktualizujemy ostatni dodany wiersz o discountLine
            discount_line = item['discountLine']
            rows[-1]['discount_base'] = discount_line['base']
            rows[-1]['discount_value'] = discount_line['value']
            rows[-1]['isDiscount'] = discount_line['isDiscount']
            rows[-1]['isPercent'] = discount_line['isPercent']

    # tworzymy DataFrame z zebranych danych i dodajemy do listy dataframów
    df = pd.DataFrame(rows)
    df_list.append(df)

df = pd.concat(df_list)

df['product_name'] = df['product_name_raw'].apply(lambda x: str(x).rstrip(" ABC"))
df['product_name'] = df['product_name'].apply(lambda x: re.sub(
    r'(?<![A-ZĄĆĘŁŃÓŚŹŻ])(?=[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż])|(?<=[a-ząćęłńóśźż])(?=[A-ZĄĆĘŁŃÓŚŹŻ])|(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż])(?=\d)',
    ' ', x))
df['product_name'] = df['product_name'].apply(
    lambda x: re.sub(r'(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])\.(?=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])', ' ', x))
df['product_name'] = df['product_name'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())


# Funkcja do wyodrębniania wartości
def extract_measurements(s):
    match = re.search(r'(\d+(?:,\d+)?)(ml|l|kg|g|ML|L|KG|G)', s)
    if match:
        measure_value = match.group(1)
        measure = match.group(2).lower()  # Konwertuj jednostki miar na małe litery
        return pd.Series([measure_value, measure])
    return pd.Series([None, None])


# Zastosowanie funkcji do kolumny 'string'
df[['measure_value', 'measure']] = df['product_name'].apply(extract_measurements)

df['measure_value'] = df['measure_value'].apply(lambda x: float(str(x).replace(',', '.')) if str(x) != 'None' else x)

df['total_final'] = df.apply(
    lambda x: x['discount_base'] - x['discount_value'] if x['isDiscount'] == True else x['total'], axis=1)
df['total_pln'] = df['total_final'].apply(lambda x: x / 100)

df.fillna('', inplace=True)

# Wyświetlenie DataFrame
print(df)
df.to_excel(cwd + f'/paragon_data.xlsx', index=False)

# end time of program + duration
end_time = time.time()
execution_time = int(end_time - start_time)
print('\n', 'exectution time = ', execution_time)
print('finish')