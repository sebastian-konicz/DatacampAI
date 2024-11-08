import os
import time
import pandas as pd
from datetime import datetime
import openai_api
# from openai.error import APIError, APITimeoutError
# start time of function
start_time = time.time()

# working directory
cwd = str(os.getcwd())

# Wczytanie pliku JSON
df = pd.read_excel(cwd + f'/paragon_data.xlsx')

products = df['product_name'].drop_duplicates()

prompt =  f"""
Mam listę produktów pozyskaną z e-paragonów ze sklepu biedronka.pl

Dla poszczególych produktów z poniższej listy wypisz w tabeli \ 
jakie mają składniki odżywcze na 100 g (tłuszcze (w tym kwasy tłuszczowe), białka, węglowodany (w tym cukry), błonnik, sól) 
oraz liczbę kalorii na 100 g.
Informacji na temat składników szukaj na stronie https://zakupy.biedronka.pl
Jeśli nie znajdziesz informacji na stronie sklepu biedronka to przeszukaj inne strony.
Dodaj do każdego produktu odnośnik do źródła danych o składnikach odżywczych w formie hiperłącza z adresem strony. 
Dodaj do każdego produktu numer jego kodu kreskowego.

### Tu jest moja lista produktów:
{products}

Zwróć wyniki w formie tabelarycznej, gdzie w pierwszym wierszu odpowiedzi będą odpowiednie nagłówki tabeli.
"""

print(prompt)

response = openai_api.chat.completions.create(
    model="gpt-4o",  # lub inny dostępny model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature = 0.25
)

text_response = response.choices[0].text.strip()

# print(text_response)

# retries = 3  # Liczba ponownych prób
# for attempt in range(retries):
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.25,
#             timeout=30
#         )
#         break  # Wyjdź z pętli, jeśli zapytanie się powiedzie
#     except (APIError, APITimeoutError) as e:
#         print(f"Próba {attempt+1} nie powiodła się: {e}")
#         time.sleep(2)  # Poczekaj przed kolejną próbą
#     else:
#         raise Exception("Nie udało się uzyskać odpowiedzi po kilku próbach.")

# text_response = response.choices[0].text.strip()

# print(text_response)

# rows = text_response.split("\n")

# # Podziel tekst na wiersze
# rows = text_response.split("\n")

# # Podziel każdy wiersz na kolumny i utwórz listę
# data = [row.split(", ") for row in rows]

# # Stworzenie DataFrame'a
# df = pd.DataFrame(data, columns=["Imię", "Wiek"])

# df.to_excel(cwd + f'/paragon_data.xlsx', index=False)

# end time of program + duration
end_time = time.time()
execution_time = int(end_time - start_time)
print('\n', 'exectution time = ', execution_time)
print('finish')
