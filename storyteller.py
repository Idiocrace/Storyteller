from time import sleep
import os
import configparser
import sys

addon_dict = {}

def listfiles(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"The path '{directory}' is not a directory.")
    
    # Include the full path for each file
    return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def typer(text, speed=None, tick=None, newline=True):
    if tick is None:
        if speed is not None:
            tick = speed / len(text)
        else:
            raise ValueError("Either 'speed' or 'tick' must be provided.")
    for char in text:
        print(char, flush=True, end='')  # Prevents newline for each character
        if char == ' ':
            sleep(tick * 1.5)  # Longer pause for spaces
        else:
            sleep(tick)
    if newline:
        print()

def typerinp(text, speed=None, tick=None):
    typer(text, speed=speed, tick=tick, newline=False)
    return input()

"""
def installaddon(addon_name):
    addon_dict = {}
    if not os.path.exists(f"{addons_location}/{addon_name}"
"""

typer('Reading config...', tick=0.01)
cfg = configparser.ConfigParser()
print()

config_file = "config.cfg"
if not os.path.exists(config_file):
    typer(f'Config file "{config_file}" not found.', tick=0.01)
    raise FileNotFoundError(f'Config file "{config_file}" not found.')
cfg.read(config_file)

typer('Getting content from "delete-content-after-loading"...', tick=0.01)
delete_content_after_loading = cfg.getboolean('Terminal', 'delete-content-after-loading', fallback=False)
if delete_content_after_loading or not delete_content_after_loading:
    typer(f'Got content from "delete-content-after-loading"; "{delete_content_after_loading}"', tick=0.01)
else:
    typer('An invalid or missing value for "delete-content-after-loading" detected. Replacing with default.', tick=0.01)
    delete_content_after_loading = False
print()


typer('Getting content from "story-files-location"...', tick=0.01)
story_files_location = cfg.get('Terminal', 'story-files-location', fallback=None)
if not story_files_location or not os.path.exists(story_files_location):
    typer('An invalid or missing value for "story-files-location" detected.', tick=0.01)
    raise FileNotFoundError('Invalid or missing value for "story-files-location".')
else:
    typer(f'Got content from "story-files-location"; "{story_files_location}"', tick=0.01)
print()


typer('Getting content from "enable-addons"...', tick=0.01)
enable_addons = cfg.getboolean('Addons', 'enable-addons', fallback=False)
if enable_addons or not enable_addons:
    typer(f'Got content from "enable-addons"; "{enable_addons}"', tick=0.01)
    if enable_addons:
        typer(f'This setting is currently redundant.', tick=0.01)
else:
    typer('An invalid or missing value for "enable-addons" detected. Replacing with default.', tick=0.01)
    enable_addons = False
print()


typer('Getting content from "addons-location"...', tick=0.01)
addons_location = cfg.get('Addons', 'addons-location', fallback=None)
if not addons_location or not os.path.exists(addons_location):
    typer('An invalid or missing value for "addons-location" detected.', tick=0.01)
    raise FileNotFoundError('Invalid or missing value for "addons-location".')
else:
    typer(f'Got content from "addons-location"; "{addons_location}"', tick=0.01)
    typer(f'This setting is currently redundant.', tick=0.01)
print()


typer('Getting content from "PYTHONDONTWRITEBYTECODE"...', tick=0.01)
sys.dontwritebytecode = cfg.get('Extra', 'PYTHONDONTWRITEBYTECODE', fallback=None)
if sys.dontwritebytecode or not sys.dontwritebytecode:
    typer(f'Got content from "PYTHONDONTWRITEBYTECODE"; "{sys.dontwritebytecode}"', tick=0.01)
print()


bigtext = """ _______  _______  _______  ______    __   __  _______  _______  ___      ___      _______  ______   
|       ||       ||       ||    _ |  |  | |  ||       ||       ||   |    |   |    |       ||    _ |  
|  _____||_     _||   _   ||   | ||  |  |_|  ||_     _||    ___||   |    |   |    |    ___||   | ||  
| |_____   |   |  |  | |  ||   |_||_ |       |  |   |  |   |___ |   |    |   |    |   |___ |   |_||_ 
|_____  |  |   |  |  |_|  ||    __  ||_     _|  |   |  |    ___||   |___ |   |___ |    ___||    __  |
 _____| |  |   |  |       ||   |  | |  |   |    |   |  |   |___ |       ||       ||   |___ |   |  | |
|_______|  |___|  |_______||___|  |_|  |___|    |___|  |_______||_______||_______||_______||___|  |_|"""

# Main Program
typer(bigtext, tick=0.00001)
typer('Please load a story file: ', tick=0.01)

files = listfiles(story_files_location)
if not files:
    typer("No files found in the 'story' directory. Exiting.", tick=0.01)
    exit()

# Display filenames without full paths
for n, file in enumerate(files, start=1):
    typer(f'[{n}] : {os.path.basename(file)}', tick=0.01)

# Loop to validate user input
while True:
    user_input = typerinp(f'[{len(files)} items available] [Pick an item by its number]: ', tick=0.01)
    if user_input.isdigit():
        file_id = int(user_input)
        if 1 <= file_id <= len(files):
            break
        else:
            typer("Input is out of range. Please try again.", tick=0.01)
    else:
        typer("Invalid input. Please enter a number.", tick=0.01)

if delete_content_after_loading:
    typer('Delete content after loading was activated. Clearing...', tick=0.01)
    os.system('clear')

file_index = file_id - 1
with open(files[file_index], 'r') as storyfile:
    storylines = storyfile.readlines()
    for line in storylines:
        if line.startswith('>wait>'):
            sleep(float(line.replace('>wait>', '').strip()))
        elif line.startswith('>step>'):
            print(line.replace('>step>', '').strip(), flush=True, end='')
        elif line.startswith('>break>'):
            print('')
        else:
            typer(line.strip(), tick=0.01)

input("")
