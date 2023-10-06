import os
import click

RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

color_map = {
    'r': RED,
    'y': YELLOW,
    'g': GREEN,
}

# Function to get string with specified color
def color_string(color, str):
    return f"{color_map[color]}{str}{RESET}"

# Custom input function to resolve the path if needed and validate its existence
def custom_path_prompt(prompt):
    while True:
        # Prompt the user for the path
        user_input = click.prompt(prompt, type=str)

        # Replace ~ with the home directory path
        if user_input.startswith("~"):
            user_input = os.path.expanduser(user_input)

        # Resolve '.' and '..' to their absolute paths
        resolved_path = os.path.abspath(user_input)

        # Check if the resolved path exists
        if os.path.exists(resolved_path):
            return resolved_path
        else:
            # click.echo("Error: Path {} does not exist.".format(resolved_path))
            click.echo(f"{RED}Error: Path '{resolved_path}' does not exist. Please try again.{RESET}")

# Function to paginate a list
def paginate_list(lst, page_size):
    for i in range(0, len(lst), page_size):
        yield lst[i:i + page_size]
