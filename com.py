import subprocess


class commands:
    def __getitem__(self, item):
        return item

    # just run python code
    def py(script, m, memory):
        try:
            exec(script[0])
            return " "
        except Exception as error:
            return error

    def bat(s, m, memory):
        script = s[0]
        # Add "@echo off" to hide commands if "-o" modifier is present
        if "-o" in m:
            script = "@echo off\n" + script
        # Run the script
        result = subprocess.run(script, shell=True, capture_output=True, text=True)
        # Check the return code
        return result

    # literally just print()
    def say(s, m, memory):
        if s[0][0] == "%":
            key = s[0][1:]  # Remove the '%' prefix
            if key in memory:
                value = memory[key]
            else:
                value = f"Undefined variable: {key}"
        else:
            value = s[0]

        if "-n" in m:
            print(value, end=" ")
        else:
            print(value)

        return " "

    # declare variable
    def var(s, m, mem):
        memory = mem
        name = s[0].lower()
        value = s[1]
        try:
            kind = s[2]
        except IndexError:
            return "no variable type entered"

        if kind == "int":
            try:
                memory[name] = int(value)
            except ValueError as v:
                return f"{v} || not a number"

        elif kind == "str":
            memory[name] = value

        elif kind == "bool":
            try:
                memory[name] = bool(int(value))
            except ValueError:
                memory[name] = bool(value)

        return memory