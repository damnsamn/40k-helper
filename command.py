import re
import helpers
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
                print(f'{self.name} {doc}')
            else:
                print(f'No help specified for command "{self.name}"')
            return
        else:
            self.callback_function(*self.args, **self.kwargs)


def command(input):

    # Split input_array into command, followed by args/kwargs
    input_array = re.findall(r'[^\s]*"[^"]+"|[^\s]+', input)

    cmd = input_array[0]
    input_array.pop(0)

    args = []
    kwargs = {}

    for arg in input_array:
        arg = arg.replace("\"", "")
        if(re.search(r"=", arg)):
            key = re.search(r"(.+?)=", arg).groups(0)[0]
            value = re.search(r"=(.+)", arg).groups(0)[0]
            kwargs[key] = value
        else:
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

        case "save_army":
            Command(cmd, saves.save_army, *args, **kwargs)

        case "load_army":
            Command(cmd, saves.load_army, *args, **kwargs)

        case "ls":
            Command(cmd, list_army, *args, **kwargs)

        case "add_model":
            Command(cmd, state.add_model, *args, **kwargs)

        case "exit":
            state.is_active = False


def do_roll(n_dice=6, n_rolls=1):
    """[n_dice?] [n_rolls?]"""
    dice = Dice(int(n_dice))
    n_rolls = int(n_rolls)
    roll = dice.roll(n_rolls)

    if len(roll) == 1:
        roll = roll[0]

    print(roll)


def list_army(index=None):
    if index:  # List index's datasheets
        model = state.army[int(index)]
        print(helpers.colors.MAGENTA + model.name + helpers.colors.END)
        print(f"{helpers.colors.BOLD}M:{helpers.colors.END} {model.M}")
        print(f"{helpers.colors.BOLD}WS:{helpers.colors.END} {model.WS}")
        print(f"{helpers.colors.BOLD}BS:{helpers.colors.END} {model.BS}")
        print(f"{helpers.colors.BOLD}S:{helpers.colors.END} {model.S}")
        print(f"{helpers.colors.BOLD}T:{helpers.colors.END} {model.T}")
        print(f"{helpers.colors.BOLD}W:{helpers.colors.END} {model.W}")
        print(f"{helpers.colors.BOLD}A:{helpers.colors.END} {model.A}")
        print(f"{helpers.colors.BOLD}Ld:{helpers.colors.END} {model.Ld}")
        print(f"{helpers.colors.BOLD}Sv:{helpers.colors.END} {model.Sv}")
    else:  # List all
        for i, model in enumerate(state.army):
            print(
                helpers.colors.BOLD +
                f"[{i}]: " +
                helpers.colors.END +
                model.name
            )
