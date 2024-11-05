import os
import time
from config.config import OPENAI_API_KEY
import openai

# start time of function
start_time = time.time()

# working directory
cwd = str(os.getcwd())

openai.api_key = OPENAI_API_KEY

# end time of program + duration
end_time = time.time()
execution_time = int(end_time - start_time)
print('\n', 'exectution time = ', execution_time)
print('finish')