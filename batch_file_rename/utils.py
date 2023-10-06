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

# Function to paginate a list
def paginate_list(lst, page_size):
    for i in range(0, len(lst), page_size):
        yield lst[i:i + page_size]
