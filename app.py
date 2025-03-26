import configparser
import os
from colorama import Fore, Style


from openai import OpenAI
import openai

# from google import genai
import google.generativeai as genai



# Get the base directory of the current Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)


# Read configs 
gpt3_api_key = config["OPENAI35"]["api_key"]
gpt3_model = config["OPENAI35"]["model"]

gemma_api_key = config["GEMMA"]["api_key"]
gemma_model = config["GEMMA"]["model"]
GEMMA_MAX_TOKENS = config["GEMMA"]["max_tokens"]


openai.api_key = gpt3_api_key
clientGpt3 = OpenAI( api_key = gpt3_api_key )

generation_config  = {
    "temperature":0.9,
    "top_p":1,
    "top_k":2,
    "max_output_tokens":GEMMA_MAX_TOKENS ,
    "stop_sequences":["XXX"], # Example stop sequence
}
genai.configure(api_key=gemma_api_key)
# clientGemma = genai.Client(api_key=gemma_api_key , generation_config=generation_config) 
modelGemma = genai.GenerativeModel(
    model_name= gemma_model,
    generation_config=generation_config )

def printInBox(msg):
    print("-------------------------------")
    print(Fore.RED + msg + Style.RESET_ALL)
    print("-------------------------------")

def checkGpt3():
    try:
        response = openai.project
        print("API Key is valid!")
        print(response)
        print("__________________")
    except openai.error.AuthenticationError as e:
        print(f"Authentication failed: {e}")


    try:
        listOfModels = clientGpt3.get_api_list
        print(listOfModels)
    except Exception as e:
        print(e)



def getGeminiHelp():
    print("\n\nList of models that support generateContent:")
    for m in clientGemma.models.list():
        for action in m.supported_actions:
            if action == "generateContent":
                print(m.name)

    print("\n\nList of models that support embedContent:")
    for m in clientGemma.models.list():
        for action in m.supported_actions:
            if action == "embedContent":
                print(m.name)


def callOpenAi():
    print("Calling OpenAI func")
    response = clientGpt3.responses.create(
        model=gpt3_model,
        instructions="You are a coding assistant that talks like a pirate.",
        input="How do I check if a Python object is an instance of a class?",
    )

    print(response.output_text)

def callChatCompletions(message):
    print("Calling chat-completions func")

    response = clientGpt3.chat.completions.create(
        model= gpt3_model,
        messages = [ {"role": "user", "content": f"{message}"  } ]
    )

    print(response)
    print(response.errors)

    # answer =  response["choices"][0]["message"]["content"]
    answer =  response.choices[0].message.content

    return answer


def processGemmaGenerate(prompt):
    print("Processing Gemma")


    response = clientGemma.models.generate_content(
        model= gemma_model , contents=prompt 
    )

    printInBox(response.text)
    print(response.usage_metadata)


def processGemmaChat():
    history = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "model", "content": "I'm doing well, thank you! How can I help you today?"},
        {"role": "user", "content": "What is the capital of France?"}
    ]    
 


    # # TO-DO add logic to add history
    # chat = clientGemma.chats.create(
    #     model= gemma_model , 
    #     history= [] )  
    
    # Start a conversation
    chat = modelGemma.start_chat(history=[])

    
    currMessage = "Where is Pune located?"
    print(f"User: {currMessage}")
    response = chat.send_message(currMessage )
    printInBox(response.text)
    print(response.usage_metadata)

    currMessage = "How many cities are names as Rampur in world?"
    print(f"User: {currMessage}")
    response = chat.send_message(currMessage  )
    printInBox(response.text)
    print(response.usage_metadata)



if __name__ == "__main__":
    print("Start")
    answer = ""
    message = "give me 5 lines about IPL 2025"

    #######################
    # OpenAI based

    # checkGpt3()
    # answer = callChatCompletions(message)
    # callOpenAi()
    # print(answer)


    #######################
    # Google Gemini based
    
    # getGeminiHelp()
    prompt = "give me 3 line details of IPL 2025"
    # processGemmaGenerate(prompt)
    processGemmaChat()

    print("End")
