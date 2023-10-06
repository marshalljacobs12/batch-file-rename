import os
import re
import shutil
import click

from .utils import color_string, paginate_list

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
            click.echo(color_string('r', f"Error: Path '{resolved_path}' does not exist. Please try again."))

@click.command()
def batch_rename():
    """
    Batch rename files in a directory interactively with backups.
    """
    try:
        # Gather user input for the directory path.
        path = custom_path_prompt(color_string('y', "Enter the directory path"))

        # Gather user input for the search text.
        search = click.prompt(color_string('y', "Enter the text or regex pattern to search for in filenames"))

        # Gather user input for the replacement text, allowing an empty string.
        replace = click.prompt(color_string('y', "Enter the text to replace the search text with"), default="")

        # Gather user input for whether to use regex.
        use_regex = click.confirm(color_string('y', "Use regular expressions for search?"))

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
            click.echo(color_string('g', f"Renaming Information (Page {current_page+1} of {len(paginated_info)}):"))
            for old_name, new_name in paginated_info[current_page]:
                formatted_old_name = old_name.ljust(max_old_name_width)
                formatted_new_name = new_name.ljust(max_new_name_width)
                click.echo(color_string('g', f"Old Name: {formatted_old_name} => New Name: {formatted_new_name}"))
            # Check if there are more pages to display
            if current_page < len(paginated_info) - 1:
                click.echo(color_string('g', "---Press Enter to See More---"))
                key = click.getchar()
                if key == '\r':
                    current_page += 1
            else:
                # No more pages to display
                break

        # Prompt the user for confirmation before applying the renaming.
        if click.confirm(color_string('y', "Apply the renaming changes?")):
            for old_name, new_name in renaming_info:
                os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
            click.echo(color_string('y', "Batch renaming complete."))

        # Prompt the user to confirm cleanup of backups.
        if click.confirm(color_string('y', "Delete backup copies?")):
            shutil.rmtree(backup_dir)
            click.echo(color_string('y', "Backup copies deleted."))
    except Exception as e:
        click.echo(color_string('r', f"An error occurred: {str(e)}"))