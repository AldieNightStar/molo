from typing import Dict

class Command:
    def __init__(self, name: str, args: str) -> None:
        self.name = name
        self.args = args
    def __str__(self) -> str:
        return f"Command<{self.name}: {self.args}>"
    def __repr__(self) -> str:
        return self.__str__()

class CommandRegistry:
    def __init__(self):
        self.reg: Dict[str, str] = {
            # Basic functions
            "goto": "mgoto($$);",
            "перейти": "mgoto($$);"
        }
    def renderCommand(self, cmd: Command) -> str:
        val = self.reg.get(cmd.name, None)
        if val == None:
            print(f"WARN: Function '{cmd.name} is not registered.")
            return f"// no such function: {cmd.name}"
        # TODO: also replace "##" with escaped "args"
        return val.replace("$$", cmd.args)
    def register(self, name: str, val: str):
        self.reg[name] = val