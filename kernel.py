from com import *
import signal
import sys
import json
import Levenshtein
from colorama import Fore as fore, Back as back

# data stuff
with open("system.json", "r") as file:
    data = json.load(file)


# load data
def getdata(name):
    return data[name]


# Just shortcut of getdata()
def gd(name): return getdata(name)


# variables
memory = {
    # pre-defined system constant
    "SYS_version": gd('version')
}


def signal_handler(sig, frame):
    PyOS_quit("X is pressed")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def call_without_parentheses(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def PyOS_quit(reason):
    print(f"\nOS shutting down because {reason}")

    print("\npress enter to exit, this is for bug report")
    leave = input(">>>")
    sys.exit(0)


# literally just parsing

def parse_command(command):
    # Split the command string by spaces
    tokens = command.split()
    # Initialize lists for modifiers and arguments
    modifiers = []
    arguments = []
    # Initialize a flag to track if we are currently parsing a single argument
    parsing_argument = False
    # Initialize a variable to hold the current argument being parsed
    current_argument = ""
    # Iterate over each token in the command string
    for token in tokens[1:]:  # Skip the first token (the command name)
        # If the token starts with "-", it's a modifier
        if token.startswith("-"):
            modifiers.append(token)
        else:
            # If we're currently parsing an argument
            if parsing_argument:
                # If the token ends with "\", it's a continuation of the current argument
                if token.endswith("\\"):
                    # Strip the "\" character and add the token to the current argument
                    current_argument += token.rstrip("\\")
                else:
                    # If the token doesn't end with "\", it's the last part of the argument
                    current_argument += token
                    # Add the complete argument to the list of arguments
                    arguments.append(current_argument)
                    # Reset the current argument
                    current_argument = ""
                    # Reset the flag indicating we're parsing an argument
                    parsing_argument = False
            else:
                # If the token contains "\", split it into multiple arguments
                if "\\" in token:
                    # Split the token by "\" and remove any empty strings resulting from adjacent spaces
                    split_arguments = [arg.strip() for arg in token.split("\\") if arg.strip()]
                    # Add the split arguments to the list of arguments
                    arguments.extend(split_arguments)
                else:
                    # If the token doesn't contain "\", it's a single argument
                    arguments.append(token)
                    # Set the flag indicating we're parsing an argument
                    parsing_argument = True
    # Return the function name, modifiers, and arguments
    return tokens[0], modifiers, arguments


# literally just parsing above

# List of valid command names
valid_commands = ["exit", "py", "bat", "say", "var"]


# Function to suggest the closest command name
def suggest_command(command):
    closest_command = min(valid_commands, key=lambda x: Levenshtein.distance(command, x))
    return closest_command


# |--------------|#
# | Actual Stuff |#
# |--------------|#


def start():
    print(f'version {gd("version")}')


def loop():
    user = input(fore.WHITE + back.BLACK + ">>>")
    try:
        comfunc, commod, comargs = parse_command(user)

        tmp = f"commands.{comfunc}({comargs},{commod},{memory})"

        if comfunc in valid_commands:
            exec(tmp)
        else:
            closest_command = suggest_command(comfunc)
            print(fore.RED + f"Invalid command: '{comfunc}'. Did you mean '{closest_command}'?")
    except IndexError:
        print(fore.RED + "Empty command! Please enter a command.")
    except Exception as err:
        print(back.RED + fore.BLACK + f"An error occurred: {err}")
        PyOS_quit("of unknown error")


start()
while 1:
    loop()
