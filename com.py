import subprocess

class commands:

    # just run python code
    def py(script,m):
        try:
            exec(script[0])
        except Exception as error:
            print(error)
    
    def bat(s, m):
        script = s[0]
        # Add "@echo off" to hide commands if "-o" modifier is present
        if "-o" in m:
            script = "@echo off\n" + script
        # Run the script
        result = subprocess.run(script, shell=True, capture_output=True, text=True)
        # Check the return code
        if result.returncode == 0:
            # Script executed successfully
            return result.stdout
        else:
            # Script execution failed, return the captured stderr
            return result.stderr

    # literally just print()
    def say(s,m, memory):
        if "-n" in m:
            print(s[0], end=" ")
        else:
            print(s[0])
    
    # declare variable
    def var(s, m, memory):
        name = s[0].lower()
        value = s[1]
        kind = s[2]

        if kind == "int":
            try:
                memory[name] = int(value)
            except ValueError as v:
                print(f"{v} || not a number")
        elif kind == "str":
            memory[name] = value
        elif kind == "bool":
            try:
                memory[name] = bool(int(value))
            except ValueError:
                memory[name] = bool((value))
        elif (kind == "dy"):
            # bool
            if (value == True) or (value == False):
                memory[name] = bool((value))

            isstr = False
            for i in list("qwertyuiopasdfghjklzxcvbnm"):
                if i in list(value):
                    isstr == True
                    break
            

        return memory