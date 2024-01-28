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
    "SYS_ver": gd('version')
}


def signal_handler(sig, frame):
    PyOS_quit("X is pressed")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def call_without_parentheses(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def PyOS_quit(reason, code=0):
    print(f"\nOS shutting down because {reason}")

    print("\npress enter to exit, this is for bug report")
    leave = input(">>>")
    sys.exit(code)


# literally just parsing

def parse_command(entered):
    # commands
    command = (entered.split(" "))[0]

    # modifiers and arguments
    mod_and_args = entered.removeprefix(f"{command} ")

    # temporary
    mod_tmp = mod_and_args.split(" ")

    # modifiers
    modifiers = []
    for i in mod_tmp:
        if i.startswith("-"):
            modifiers.append(i)

    arguments_tmp = (mod_and_args.removeprefix(" ".join(modifiers))).removesuffix(" ".join(modifiers))
    arguments = arguments_tmp.split("\\")

    # Return the function name, modifiers, and arguments
    return command, modifiers, arguments


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
    print(f"\nPyOS version {gd('version')}\n")
    print("""GNU GENERAL PUBLIC LICENSE
   Version 3, 29 June 2007
""")


def loop():
    global memory

    user = input(fore.RESET + back.RESET + ">>>")
    try:
        comfunc, commod, comargs = parse_command(user)
        print(parse_command(user))

        tmp = f"commands.{comfunc}({comargs}, {commod}, {memory})"

        if comfunc == "exit":

            PyOS_quit("exit command was used")
        elif comfunc in valid_commands:
            # main command stuff

            returned = eval(tmp)
            if isinstance(returned, str):
                print(returned)
            else:
                memory = returned
        else:
            closest_command = suggest_command(comfunc)
            print(fore.RED + f"Invalid command: '{comfunc}'. Did you mean '{closest_command}'?")
    except IndexError:
        print(fore.RED + "Empty command! Please enter a command.")


start()
while 1:
    loop()