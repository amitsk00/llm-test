import configparser
import os
from datetime import datetime 

import requests
import json 

import pydantic

from myUtils import printInBox ,  printMetaDataToken , getUserInput , printReqMetaDataToken
from myUtils import color_user, color_llm  ,config , Fore 
from myUtils import BASE_DIR, CONFIG_DIR, CONFIG_FILE
from app_llm import checkKey , callOpenAi , callChatCompletions

import uvicorn
# Example for FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Define the origins that are allowed to make requests
origins = [
    "http://localhost:3000",  # Your React app's development server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



config = configparser.ConfigParser()
config.read(CONFIG_FILE)

boolFlow = config.getboolean("GENERIC", "flagFlow")
boolDebug = config.getboolean("GENERIC", "flagDebug")


# # currentLlm = "OPENAI35"
# currentLlm = "PERPLEXITY"

# # Read configs 
# myKey = config[currentLlm]["api_key"]
# myModel = config[currentLlm]["model"]
# myEmbedModel = config[currentLlm]["embed_model"]  
# maxTokens = int(config[currentLlm]["max_tokens"])

# if not currentLlm.startswith("OPENAI"):
#     myBaseUrl = config[currentLlm]["base_url"]


@app.get("/")
def read_root():
    # Return a dictionary that will be converted to JSON
    return {"Hello": "World"}




@app.get("/chat/{message}")
def chat_to_llm(message: str):
    ret_answer = {}
    print(f"\n\nLLM being called at {datetime.now()}")
    answer , curr_tokens , curr_cost  = callChatCompletions(message)
    ret_answer["answer"] = answer
    ret_answer["tokens"] = curr_tokens
    ret_answer["cost"] = curr_cost

    return ret_answer



if __name__ == "__main__":
    # print("Start")


    checkKey()

    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000 )

    answer = ""
    

    ######################
    # OpenAI based

    

    # answer = callOpenAi()
    # print("\n===========================\n")


    # message = "give me 5 lines about Ganesh festival in Pune"
    # # answer = callChatCompletions(message)
    # answer = chat_to_llm(message)
    # printInBox(answer)
    # print("\n===========================\n")





    # print("End")
    ############################
