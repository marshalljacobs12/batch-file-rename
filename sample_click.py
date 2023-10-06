import os
import click
import re
import shutil

# Define ANSI escape codes for styling
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

# Function to paginate a list
def paginate_list(lst, page_size):
    for i in range(0, len(lst), page_size):
        yield lst[i:i + page_size]

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


@click.command()
def batch_rename():
    """
    Batch rename files in a directory interactively with backups.
    """
    try:
        # Gather user input for the directory path.
        path = custom_path_prompt(f"{YELLOW}Enter the directory path{RESET}")

        # Gather user input for the search text.
        search = click.prompt(f"{YELLOW}Enter the text or regex pattern to search for in filenames{RESET}")

        # Gather user input for the replacement text, allowing an empty string.
        replace = click.prompt(f"{YELLOW}Enter the text to replace the search text with{RESET}", default="")

        # Gather user input for whether to use regex.
        use_regex = click.confirm(f"{YELLOW}Use regular expressions for search?{RESET}")

        # Create a backup directory for storing backup copies of files.
        backup_dir = os.path.join(path, "backup")
        os.makedirs(backup_dir, exist_ok=True)

        # List all files in the specified directory.
        files = os.listdir(path)

        # Create a list to store renaming information.
        renaming_info = []

        for filename in files:
            # Split the filename into filename and extension parts.
            filename_parts = os.path.splitext(filename)
            filename_without_extension = filename_parts[0]
            file_extension = filename_parts[1]

            if use_regex:
                if re.search(search, filename_without_extension):
                    new_filename_without_extension = re.sub(search, replace, filename_without_extension)
                else:
                    continue
            else:
                # Check if the search text is in the filename.
                if search in filename_without_extension:
                    new_filename_without_extension = filename_without_extension.replace(search, replace)
                else:
                    continue

            # Reconstruct the full filename with the updated filename part and the original extension.
            new_filename = f"{new_filename_without_extension}{file_extension}"

            # Append the renaming information to the list.
            renaming_info.append((filename, new_filename))

            # Construct the full paths for the old and new filenames.
            old_path = os.path.join(path, filename)
            new_path = os.path.join(path, new_filename)

            # Construct the full paths for backup copies.
            backup_path = os.path.join(backup_dir, filename)

            # Create a backup copy of the original file.
            shutil.copy2(old_path, backup_path)

        # Paginate the renaming information (show 10 at a time)
        page_size = 10
        paginated_info = list(paginate_list(renaming_info, page_size))
        current_page = 0

        # Calculate the maximum width of old and new filenames
        max_old_name_width = max(len(old_name) for old_name, _ in renaming_info)
        max_new_name_width = max(len(new_name) for _, new_name in renaming_info)

        # Display paginated renaming information with aligned spacing
        while current_page < len(paginated_info):
            click.clear()
            click.echo(f"{GREEN}Renaming Information (Page {current_page+1} of {len(paginated_info)}):{RESET}")#.format(current_page + 1, len(paginated_info)))
            for old_name, new_name in paginated_info[current_page]:
                formatted_old_name = old_name.ljust(max_old_name_width)
                formatted_new_name = new_name.ljust(max_new_name_width)
                click.echo(f"{GREEN}Old Name: {formatted_old_name} => New Name: {formatted_new_name}{RESET}")
            # Check if there are more pages to display
            if current_page < len(paginated_info) - 1:
                click.echo(f"{GREEN}---Press Enter to See More---{RESET}")
                key = click.getchar()
                if key == '\r':
                    current_page += 1
            else:
                # No more pages to display
                break

        # Prompt the user for confirmation before applying the renaming.
        if click.confirm(f"{YELLOW}Apply the renaming changes?{RESET}"):
            for old_name, new_name in renaming_info:
                os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
            click.echo(f"{YELLOW}Batch renaming complete.{RESET}")

        # Prompt the user to confirm cleanup of backups.
        if click.confirm(f"{YELLOW}Delete backup copies?{RESET}"):
            shutil.rmtree(backup_dir)
            click.echo(f"{YELLOW}Backup copies deleted.{RESET}")

    except Exception as e:
        click.echo(f"{RED}An error occurred: {str(e)}{RESET}")

if __name__ == '__main__':
    batch_rename()
