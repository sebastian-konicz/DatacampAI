import os
import time
import numpy as np
from PIL import Image
from transformers import image_transforms, pipeline
import matplotlib.pyplot as plt
from transformers import AutoModel

def main():
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    # filename = 'hlasko'
    filename = 'papcio'

    original_image = Image.open(cwd +f'/data/img/{filename}.jpg')

    print(original_image)

    # image_array = np.array(original_image)
    #
    # print(image_array)

    imgplot = plt.imshow(original_image)
    plt.show()

    model = AutoModel.from_pretrained("openbmb/MiniCPM-Llama3-V-2_5", trust_remote_code=True)
    classifier = pipeline(task="image-classification", model=model)

    results = classifier(original_image, top_k=2)

    print(results[0]['label'])
    print(results)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    main()

