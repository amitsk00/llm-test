import configparser
import os
from colorama import Fore, Style

import sys
import select


DASHES = "-" * 20
# Get the base directory of the current Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

INPUT_TIMEOUT = config.getint("GENERIC", "input_timeout")  # seconds

color_user = getattr(Fore, "GREEN")
color_llm = getattr(Fore, "BLUE")



def printInBox(msg, color="YELLOW"): # Default color is GREEN
    """Prints a message inside a box with a specified colorama Fore color."""

    try:
        # Get the color attribute from Fore using the color string (case-insensitive)
        color_code = getattr(Fore, color.upper())
    except AttributeError:
        # Fallback if the color name is invalid
        print(f"(Invalid color: {color}. Using default YELLOW instead.)")
        color_code = getattr(Fore, "CYAN")
    except Exception as e:
        # General fallback for other potential errors (like msg not being string)
        print(f"(Error applying color: {e}. Printing raw message.)")
        color_code = getattr(Fore, "CYAN")
    
 
    print(color_code + f"{DASHES}"  )
    print(str(msg)  )
    print(f"{DASHES}")
    # print(Style.RESET_ALL)
    print(Fore.RESET)


def printMetaDataToken(metadata):
    if metadata:
        # Use getattr for safety in case an attribute is missing, providing 'N/A' as default
        prompt_tokens = getattr(metadata, 'prompt_token_count', 'N/A')
        candidate_tokens = getattr(metadata, 'candidates_token_count', 'N/A')  
        total_tokens = getattr(metadata, 'total_token_count', 'N/A')

        printInBox( f"Prompt Tokens: {prompt_tokens} and Total Tokens: {total_tokens}" , "yellow")
    else:
        printInBox( "No metadata available." , "red")



def getUserInput():
       
        print(color_user + "You: ", flush=True)
        ready_to_read, _, _ = select.select([sys.stdin], [], [], INPUT_TIMEOUT)

        if ready_to_read:
            user_input = sys.stdin.readline().strip()
            print(Fore.RESET, end='')
        else:
            # Timeout occurred
            print(Fore.RED + f"\nTimeout: No input received for {INPUT_TIMEOUT} seconds. Exiting chat." + Fore.RESET)
            user_input = None

        return user_input
            