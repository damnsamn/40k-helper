import re
from helpers import style
import saves
import state
import gameplay
from dice import Dice


class Command:
    def __init__(self, command_name, callback_function, *args, **kwargs):
        self.name = command_name
        self.args = args
        self.kwargs = kwargs
        self.callback_function = callback_function

        if self.args.count("?"):
            doc = self.callback_function.__doc__
            if doc:
                print(style.magenta(f'{self.name} {doc}'))
            else:
                print(style.grey(f'No help specified for command "{self.name}"'))
            return
        else:
            try:
                self.callback_function(*self.args, **self.kwargs)
            except TypeError as e:
                print(style.red(format(e)))



def command(input):

    # Split input_array into command, followed by args/kwargs
    input_array = re.findall(r'[^\s]*?"[^"]+"|[^\s]+', input)

    cmd = input_array[0]
    input_array.pop(0)

    args = []
    kwargs = {}

    for arg in input_array:
        arg = arg.replace("\"", "")
        if(re.search(r"=", arg)):
            key = re.search(r"(.+?)=", arg).groups(0)[0]
            value = re.search(r"=(.+)", arg).groups(0)[0]
            value = int(value) if value.isnumeric() else value
            kwargs[key] = value
        else:
            arg = int(arg) if arg.isnumeric() else arg
            args.append(arg)

    # print(cmd, args)

    # parse commands
    match cmd:

        case "roll":
            Command(cmd, do_roll, *args, **kwargs)

        case "hits":
            Command(cmd, gameplay.hits, *args, **kwargs)

        case "wounds":
            Command(cmd, gameplay.wounds, *args, **kwargs)

        case "probabilities":
            Command(cmd, gameplay.probabilities, *args, **kwargs)

        case "save":
            Command(cmd, gameplay.save, *args, **kwargs)

        case "new_army":
            Command(cmd, saves.new_army, *args, **kwargs)

        case "save_army":
            Command(cmd, saves.save_army, *args, **kwargs)

        case "load_army":
            Command(cmd, saves.load_army, *args, **kwargs)

        case "ls":
            Command(cmd, list_army, *args, **kwargs)

        case "add_model":
            Command(cmd, state.add_model, *args, **kwargs)

        case "update_model":
            Command(cmd, state.update_model, *args, **kwargs)

        case "remove_model":
            Command(cmd, state.remove_model, *args, **kwargs)

        case "fight":
            Command(cmd, gameplay.fight, *args, **kwargs)

        case "exit":
            state.is_active = False

        case _:
            print(style.red(f'Command "{cmd}" not found'))


def do_roll(n_dice=6, n_rolls=1):
    """[n_dice?] [n_rolls?]"""
    dice = Dice(n_dice)
    roll = dice.roll(n_rolls)

    if len(roll) == 1:
        roll = roll[0]

    print(roll)


def list_army(index=None):
    if index != None:  # List index's datasheets
        model = state.army[index]
        print(f"{style.magenta(style.bold(model.name))}")
        print(f"{style.bold('M:')} {style.TAB} {model.M}")
        print(f"{style.bold('WS:')} {style.TAB} {model.WS}")
        print(f"{style.bold('BS:')} {style.TAB} {model.BS}")
        print(f"{style.bold('S:')} {style.TAB} {model.S}")
        print(f"{style.bold('T:')} {style.TAB} {model.T}")
        print(f"{style.bold('W:')} {style.TAB} {model.W}")
        print(f"{style.bold('A:')} {style.TAB} {model.A}")
        print(f"{style.bold('Ld:')} {style.TAB} {model.Ld}")
        print(f"{style.bold('Sv:')} {style.TAB} {model.Sv}")
    else:  # List all
        for i, model in enumerate(state.army):
            print(
                style.bold(f"[{i}]: ") + model.name
            )
