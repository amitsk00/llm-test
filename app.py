import configparser
import os
import requests
import json 

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



def callOpenAi():
    if boolFlow:
        print("\n\nCalling OpenAI func")

    headers = {"Authorization": f"Bearer {myKey}"}
    url = f"{myBaseUrl}/chat/completions"

    currMessage = "How to ensure cost efficient check of string fields which can have mixed case values"
    startMessage = [
        {"role": "system", "content": "You are a coding assistant who helps write efficient queries in BigQuery and SQL"},
        {"role": "user", "content": currMessage}
    ]
    # startMessage = {
    #     "role": "system", "content": "You are a coding assistant who helps write efficient queries in BigQuery and SQL",
    #     "role": "user", "content": currMessage
    # }

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

    currJsonObj = response.json()
    currJsonObj = currJsonObj.replace("'", '"')
    data = json.loads(currJsonObj)
    llmAnswer = data.choices[0].message.content
    
    printReqMetaDataToken(data.usage)
    print(llmAnswer)



def callChatCompletions(message):
    if boolFlow:
        print("\n\nCalling chat-completions func")

    startMessage = [
        {"role": "system", "content": "You are a helpful AI assistant."},
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
    answer =  response.choices[0].message.content

    return answer





if __name__ == "__main__":
    print("Start")
    answer = ""
    message = "give me 5 lines about England and India test series"

    ######################
    # OpenAI based

    checkKey()

    answer = callOpenAi()

    # print("\n===========================\n")
    # answer = callChatCompletions(message)
    # printInBox(answer)





    print("End")
    ############################
