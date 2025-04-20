
from utils import printInBox ,  printMetaDataToken , getUserInput
from utils import color_user, color_llm  ,config , Fore 


import google.generativeai as genai




 


def processGemmaGenerate(prompt):
    print("Processing Gemma")


    response = client_gemma.models.generate_content(
        model= gemma_model , contents=prompt 
    )

    printInBox(response.text)
    print(response.usage_metadata)


def getGemmaResponse(chat_session, user_input):

    try:
        response = chat_session.send_message(user_input)
        # printInBox(response)
        printMetaDataToken(response.usage_metadata)
        return response.text
    except Exception as e:
        print(f"An error occurred while getting the response: {e}")
        return "Sorry, I couldn't process your request at the moment."

    


def talkToGemma():

    gemma_api_key = config["GEMMA"]["api_key"]
    gemma_model = config["GEMMA"]["model"]
    gemma_max_tokens = config.getint("GEMMA", "max_tokens")


    gemma_generation_config  = {
        "temperature":0.9,
        "top_p":1,
        "top_k":2,
        "max_output_tokens":gemma_max_tokens ,
        "stop_sequences":["XXX"], # Example stop sequence
    }
    genai.configure(api_key=gemma_api_key)
    # client_gemma = genai.Client(api_key=gemma_api_key , generation_config=gemma_generation_config) 
    system_instruction_text = "You are a knowledgeable and friendly assistant. Answer questions clearly and provide explanations when helpful. Be precise and concise. If you don't know the answer, say 'I don't know'."
    model_gemma = genai.GenerativeModel(
        model_name= gemma_model,
        generation_config=gemma_generation_config 
        # , system_instruction = system_instruction_text
        )

    history = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "model", "content": "I'm doing well, thank you! How can I help you today?"},
        {"role": "user", "content": "What is the capital of France?"}
    ]    
    chat = model_gemma.start_chat(history=[])


    instruction_prefix = "Be precise and concise. "
    while True: 
        try:
            user_input = getUserInput()
            if user_input is None:
                break 

            # Check if the user wants to exit
            if user_input.lower() in ["quit", "exit"]:
                print(Fore.RED + "Exiting chat..." + Fore.RESET)
                break

            response_text = getGemmaResponse(chat, instruction_prefix + user_input)
            print(color_llm + f"Gemma: \n{response_text}" + Fore.RESET)

        except KeyboardInterrupt:
            # Allow exiting with Ctrl+C
            print("\nExiting chat due to keyboard interrupt...")
            break
        except Exception as e:
            # Catch any other unexpected errors during the loop
            print(f"\nAn unexpected error occurred: {e}")
            # Optionally break or continue depending on desired robustness
            # break
        finally:
            print(Fore.RESET)

 
    print("Gemma Chat ended.")





