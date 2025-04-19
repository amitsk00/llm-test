
# import configparser
# import os
from utils import printInBox , config , Fore , Style

import google.generativeai as genai


# # Get the base directory of the current Python file
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CONFIG_DIR = os.path.join(BASE_DIR, "config")
# CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

# config = configparser.ConfigParser()
# config.read(CONFIG_FILE)

gemini_api_key = config["GEMINI15"]["api_key"]
gemini_model = config["GEMINI15"]["model"]
gemini_max_tokens = int(config["GEMINI15"]["max_tokens"] )


genai.configure(api_key=gemini_api_key)
generation_config  = {
    "temperature":0.9,
    "top_p":1,
    "top_k":2,
    "max_output_tokens":gemini_max_tokens ,
    "stop_sequences":["XXX"], # Example stop sequence
}

system_instruction_text = "You are a knowledgeable and friendly assistant. Answer questions clearly and provide explanations when helpful. Be precise and concise. If you don't know the answer, say 'I don't know'."


model_gemini = genai.GenerativeModel(
    model_name = gemini_model ,
    generation_config = generation_config ,
    system_instruction = system_instruction_text
    )
 
chat = model_gemini.start_chat(history=[])


def get_gemini_response(chat_session, user_input):
    try:
        response = chat_session.send_message(user_input)
        # printInBox(response)
        return response.text
    except Exception as e:
        print(f"An error occurred while getting the response: {e}")
        return "Sorry, I couldn't process your request at the moment."

 

while True:
    try:
        user_input = input(Fore.GREEN + "You: \n")

        # Check if the user wants to exit
        if user_input.lower() in ["quit", "exit"]:
            print(Fore.RED + "Exiting chat...")
            break

        response_text = get_gemini_response(chat, user_input)
        print(Fore.BLUE + f"\nGemini: \n{response_text}\n---------\n" + Style.RESET_ALL)

    except KeyboardInterrupt:
        # Allow exiting with Ctrl+C
        print("\nExiting chat due to keyboard interrupt...")
        break
    except Exception as e:
        # Catch any other unexpected errors during the loop
        print(f"\nAn unexpected error occurred: {e}")
        # Optionally break or continue depending on desired robustness
        # break

print("Chat ended.")