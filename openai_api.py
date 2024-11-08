import os
import time
from config.config import OPENAI_API_KEY
from openai import OpenAI

def main():
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    client = OpenAI(api_key=OPENAI_API_KEY)

    # opening aritcle text
    with open('article_result.txt', 'r') as file:
        # Wczytywanie całej zawartości pliku
        file = file.read()

    prompt = f"""
    Podsumuj po polsku artykuł z znajdujący się w potrójnym cudzysłowiu. 
    Na koniec wypowiedzi podkreśl najważniejsżą myśl przewodnią dla czytelnika wynikającą z artykułu.
    Na samym końcu wypowiedzi dodaj 5 hasztagów, które odnoszą się do artykułu.  
    Swoją odpowiedź podziel na paragrafy, które będą się zaczynały od emotikony nawiązującej do treści paragrafu.
    Odpowiedź ma mieć maksymalnie 2000 znaków.
    '''{file}'''
    """

    print("PROMPT:", prompt)

    def get_response(prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lub inny dostępny model
            messages=[
                {"role": "system", "content": "Jesteś osobą poszerzającą wiedzę o AI, która dzieli się swoimi przemyśleniami na portalu LinkedIn w formie podsumowań arykułów, które przeczytała."},
                {"role": "user", "content": prompt}
            ],
            # max_tokens=20,
            temperature=0.25
        )
        return response.choices[0].message.content

    text_response = get_response(prompt)

    print("RESPONSE:\n", text_response)

    with open('post_text.txt', 'w', encoding='utf-8') as f:
        f.write(f"{text_response}")

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    main()

