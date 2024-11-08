import os
import time
from config.config import OPENAI_API_KEY
from openai import OpenAI
from datasets import load_dataset_builder
from transformers import AutoTokenizer

def main():
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    # data_builder = load_dataset_builder('imdb')
    # print(data_builder.description)

    input_string = "HOWDY, how aré yoü?"
    print(input_string)

    # Download the tokenizer
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    # Normalize the input string
    output = tokenizer.backend_tokenizer.normalizer.normalize_str(input_string)

    print(output)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    main()

