import configparser
import os
from datetime import datetime 

import requests
import json 

# import pydantic
from pydantic import BaseModel
import uuid

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

#############################
# dict to store message history
session_store = {}

class ChatMessage(BaseModel):
    session_id: str | None = None
    message: str


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




# @app.get("/chat/{message}")
@app.post("/chat")
def chat_to_llm(chat_message: ChatMessage):
    curr_session = chat_message.session_id

    if not curr_session or curr_session not in session_store:
        # New session: create a unique ID and initialize history        
        curr_session = str(uuid.uuid4())
        print(f"new session to be created with f{curr_session}")
        session_store[curr_session] = []

    session_store[curr_session].append({"role": "user", "content": chat_message.message})
    conversation_history = session_store[curr_session]


    ret_answer = {}
    print(f"\n\nLLM being called at {datetime.now()}")
    answer , curr_tokens , curr_cost  = callChatCompletions(conversation_history)

    llm_response = {"role": "assistant", "content": answer}
    session_store[curr_session].append(llm_response)

    ret_answer["answer"] = answer
    ret_answer["tokens"] = curr_tokens
    ret_answer["cost"] = curr_cost
    ret_answer["session_id"] = curr_session

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
    # chat_message_obj = ChatMessage(message=message)
    # # answer = chat_to_llm(chat_message_obj)
    # answer , curr_tokens, curr_cost = callChatCompletions(message)
    # printInBox(answer)
    # print("\n===========================\n")





    # print("End")
    ############################
