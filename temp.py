import google.generativeai as genai

import configparser
import os 

# Get the base directory of the current Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

gemma_api_key = config["GEMMA"]["api_key"]
gemma_model = config["GEMMA"]["model"]
GEMMA_MAX_TOKENS = config["GEMMA"]["max_tokens"]




# Set up the API key
genai.configure(api_key=gemma_api_key)

# Create a chat model with parameters
model = genai.GenerativeModel(
    model_name= gemma_model,
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "max_output_tokens": 512,  # Adjust as needed
    }
)

# Start a conversation
chat = model.start_chat(history=[])

# Send a message
response = chat.send_message("Hello, how are you?")
print(response.text)
