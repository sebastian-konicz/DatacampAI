import os
import time
import requests
from config.config import OPENAI_API_KEY
from openai import OpenAI
# from IPython.display import Image
import base64
from PIL import Image
from io import BytesIO

def main():
    # https://www.datacamp.com/tutorial/a-comprehensive-guide-to-the-dall-e-3-api
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    client = OpenAI(api_key=OPENAI_API_KEY)

    # opening aritcle text
    with open('article_image_summary.txt', 'r') as file:
        # Wczytywanie całej zawartości pliku
        file = file.read()

    prompt = f"""
    W potrójnym cudzysłowiu znajduje się podsumowanie treści artykułu. Na podstawie podsumowania stwórz obraz, który będzie nawiązywał do treści artykułu i dobrze go zobrazuje odbiorcom na platformie LinkedIn.
    '''{file}'''
    """

    print("PROMPT:", prompt)

    def get_image_from_DALL_E_3_API(prompt):

        image_dimension = "1024x1024"
        image_quality = "standard"
        model = "dall-e-3"
        nb_final_image = 1

        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=image_dimension,
            quality=image_quality,
            n=nb_final_image,
        )

        image_url = response.data[0].url

        print(image_url)
        print(response.data[0])

        # Pobierz obraz z URL
        image_response = requests.get(image_url)

        # Sprawdź, czy pobieranie obrazu się powiodło
        if image_response.status_code == 200:
            # Otwórz obraz za pomocą PIL i zapisz go jako plik
            image = Image.open(BytesIO(image_response.content))
            image.save("generated_image.png")
            print("Obraz został zapisany jako 'generated_image.png'")
        else:
            print("Błąd podczas pobierania obrazu")

    get_image_from_DALL_E_3_API(prompt)

    # text_response = get_response(prompt)

    # def get_response(prompt):
    #     response = client.chat.completions.create(
    #         model="gpt-4o-mini",  # lub inny dostępny model
    #         messages=[
    #             {"role": "system", "content": "Jesteś osobą poszerzającą wiedzę o AI, która dzieli się swoimi przemyśleniami na portalu LinkedIn w formie podsumowań arykułów, które przeczytała."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         # max_tokens=20,
    #         temperature=0.25
    #     )
    #     return response.choices[0].message.content
    #
    # text_response = get_response(prompt)
    #
    # print("RESPONSE:\n", text_response)

    # with open('article_image_summary.txt', 'w', encoding='utf-8') as f:
    #     f.write(f"{text_response}")

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    main()

