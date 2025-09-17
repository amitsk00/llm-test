import configparser
import os

import requests
import json 

import pydantic

from myUtils import printInBox ,  printMetaDataToken , getUserInput , printReqMetaDataToken
from myUtils import color_user, color_llm  ,config , Fore 
from myUtils import BASE_DIR, CONFIG_DIR, CONFIG_FILE


from openai import OpenAI
import openai





config = configparser.ConfigParser()
config.read(CONFIG_FILE)

boolFlow = config.getboolean("GENERIC", "flagFlow")
boolDebug = config.getboolean("GENERIC", "flagDebug")


# currentLlm = "OPENAI35"
currentLlm = "PERPLEXITY"

# Read configs 
myKey = config[currentLlm]["api_key"]
myModel = config[currentLlm]["model"]
myEmbedModel = config[currentLlm]["embed_model"]  
maxTokens = int(config[currentLlm]["max_tokens"])

if not currentLlm.startswith("OPENAI"):
    myBaseUrl = config[currentLlm]["base_url"]


openai.api_key = myKey
clientLlm = OpenAI( 
    base_url = myBaseUrl,
    api_key = myKey 
    )

llmChatConfig  = {    
    "top_p":1,
    # "top_k":2,
    # "stop_sequences":["XXX"], # Example stop sequence
    "max_tokens":maxTokens  ,
    "temperature":0.9,    
}
 
 
def checkKey():
    try:
        response = openai.project
        print("API Key is valid!")
    except openai.error.AuthenticationError as e:
        print(f"Authentication/KEY failed: {e}")

    ############################
    # NOT WORKING FOR PERPLEXITY

    if not currentLlm == "PERPLEXITY":
        try:
            listOfModels = clientLlm.models.list()
            for m in listOfModels.data:
                printInBox(m.id)
        except Exception as e:
            printInBox(f"Error fetching models: {e}", "red")
            print(e)


def processResponse(data):
    pass 
    list_results = []

    print(data["usage"])

    i_tokens = data["usage"]["total_tokens"]
    f_cost = data["usage"]["cost"]["total_cost"]
    
    for x in data["search_results"]:
        # print(x)
        list_results.append(x["snippet"])

    print(f"total tokens : {i_tokens}")
    print(f"total cost - {f_cost}")

    return list_results



def callOpenAi():
    if boolFlow:
        pass
        print("\n\nCalling Requests method")

    headers = {"Authorization": f"Bearer {myKey}"}
    url = f"{myBaseUrl}/chat/completions"

    currMessage = "How to use partitions in BigQuery"
    currContext = """
        You are a coding assistant who helps write efficient queries in BigQuery. 
        You answer in bullet points, unless asked for details
        """
    startMessage = [
        {"role": "system", "content": currContext},
        {"role": "user", "content": currMessage}
    ]


    try: 
        payload = {
            "model": myModel,
            "messages": startMessage 
        }

        response = requests.post(url, json=payload, headers=headers)        
    except Exception as e:
        print(f"An error occurred in callOpenAi: {e}")
        return "error"

    if response.status_code != 200:
        printInBox(f"Error: {response.status_code} - {response.text}", "red")
        return "error"

    data = response.json() 
    if data:
        llmAnswer = processResponse(data)
        # printReqMetaDataToken(data.usage)
        for line in llmAnswer:
            print(line)
    else:
        print("EMPTY RESPONSE")



def callChatCompletions(message):
    if boolFlow:
        print("\n\nCalling chat-completions func")

    curr_context = "You are a helpful AI assistant who is exprt in GCP BQ. Answer for 50 tokens only"
    curr_context = "You are a helpful AI assistant who is exprt in GCP BQ."
    startMessage = [
        {"role": "system", "content": curr_context},
        {"role": "user", "content": message}
    ]

    try:
        response = clientLlm.chat.completions.create(
            model= myModel,
            **llmChatConfig ,
            messages = startMessage
        )
    except Exception as e:
        print(f"An error occurred in callChatCompletions: {e}")
        return "error"

    # print(response)
    # if response.errors:
    #     printInBox("Errors in response from chat-completions:", "yellow")
    #     for error in response.errors:
    #         printInBox(f"Error: {error.message}", "red")
    #     return "error"
     

    # answer =  response["choices"][0]["message"]["content"]
    llmAnswer =  response.choices[0].message.content
    curr_tokens , curr_cost = printReqMetaDataToken(response.usage)

    return llmAnswer , curr_tokens , curr_cost 



