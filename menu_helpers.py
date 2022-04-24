"""
This module is responsible for handling the main menus of the readme
generator app.

When provided with a menu with the correct structure, the MenuHandler
class will show the output to the user in a readable format, and parse
the users response to the menu prompts.
"""

import os
from colorama import Fore
from input_reader import InputReader


input_reader = InputReader()


def clear_screen():
    """
    Uses the OS 'clear' command to clear the terminal window.

    Note: This command is a linux command and will not work on Windows
    Operating Systems. As this app is meant to be ran on a Linux Heroku
    app, the clear command has been chosen.

    If you wish to run this locally on a windows machine, please use the
    'cls' command
    """
    os.system('clear')


def process_menu(menu):
    """
    Processes a given menu dictionary by:
    1. Displaying the menu on screen
    2. Parsing and returning the users response to the menu prompts

        Parameters:
            menu (dict): Dictionary outlining the structure of the menu

                E.g. {
                    "prompt": "Which section type would you like to add?",
                    "type": "choice",
                    "options": {
                        "1": {
                            "prompt": "Introduction",
                            "mapping": "Intro"
                        },
                        "2": {
                            "prompt": "Intended Audience",
                            "mapping": "IntendedAudience"
                        },
                        "3": {
                            "prompt": "Testing",
                            "mapping": "Testing"
                        }
                    }
                }

        Returns:
                response (str): The users response to the menu prompt
    """

    display_menu(menu)

    response = parse_menu_response(menu)

    while not response:
        display_menu(menu)
        response = parse_menu_response(menu)

    return response


def display_menu(menu):
    """
    Displays menu prompts in the terminal in standardised format

    Parameters:
        menu (dict): Dictionary outlining the structure of the menu

            E.g. {
                "prompt": "Which section type would you like to add?",
                "type": "choice",
                "options": {
                    "1": {
                        "prompt": "Introduction",
                        "mapping": "Intro"
                    },
                    "2": {
                        "prompt": "Intended Audience",
                        "mapping": "IntendedAudience"
                    },
                    "3": {
                        "prompt": "Testing",
                        "mapping": "Testing"
                    }
                }
            }

    Returns:
        NA

    """
    clear_screen()
    print(Fore.YELLOW + menu.get('prompt') + Fore.WHITE)
    for key in menu.get('options', []).keys():
        print(f'[{key}] {menu.get("options", {}).get(key).get("prompt")}')


def parse_menu_response(menu):
    """
    Parses the input from the user in response to a menu's prompt
    Ensures that the input is of a correct format and appropriate for the type
    of prompt given

    Parameters:
        menu (dict): Dictionary outlining the structure of the menu

            E.g. {
                "prompt": "Which section type would you like to add?",
                "type": "choice",
                "options": {
                    "1": {
                        "prompt": "Introduction",
                        "mapping": "Intro"
                    },
                    "2": {
                        "prompt": "Intended Audience",
                        "mapping": "IntendedAudience"
                    },
                    "3": {
                        "prompt": "Testing",
                        "mapping": "Testing"
                    }
                }
            }

    Returns:
        response (str): The validated input that the user has provided

    """
    print(Fore.YELLOW + "\n\nEnter Your Input Below:" + Fore.WHITE)
    user_input = input_reader.read_input(menu.get('multiline'))

    if menu.get('type') == 'choice':
        response = handle_choice_response(menu, user_input)
    elif menu.get('type') == 'input':
        response = handle_input_response(user_input)

    return response


def handle_choice_response(menu, response):
    """
    Validates a users input to ensure it's appropriate given the choices
    available

    Parameters:
        menu (dict): Dictionary outlining the structure of the menu

            E.g. {
                "prompt": "Which section type would you like to add?",
                "type": "choice",
                "options": {
                    "1": {
                        "prompt": "Introduction",
                        "mapping": "Intro"
                    },
                    "2": {
                        "prompt": "Intended Audience",
                        "mapping": "IntendedAudience"
                    },
                    "3": {
                        "prompt": "Testing",
                        "mapping": "Testing"
                    }
                }
            }

        response (str): The input provided by the user

    Returns:
        response (str): If valid the response is returned
        False: If invalid, a False boolean is returned to the caller

    """
    if response in menu.get('options').keys():
        return response

    return False


def handle_input_response(response):
    """
    Validates a users input to ensure it's appropriate

    Parameters:
        menu (dict): Dictionary outlining the structure of the menu

            E.g. {
                "prompt": "Which section type would you like to add?",
                "type": "choice",
                "options": {
                    "1": {
                        "prompt": "Introduction",
                        "mapping": "Intro"
                    },
                    "2": {
                        "prompt": "Intended Audience",
                        "mapping": "IntendedAudience"
                    },
                    "3": {
                        "prompt": "Testing",
                        "mapping": "Testing"
                    }
                }
            }

        response (str): The input provided by the user

    Returns:
        response (str): If valid the response is returned
        False: If invalid, a False boolean is returned to the caller

    """
    return response


def read_input(multiline):
    """
    Adds a section of a given type to the readme object

        Parameters:
                multiline (bool): Boolean determining if user input can
                contain multiple newlines

        Returns:
                input_text (String): The user's input
    """
    input_text = ""

    if multiline:
        print(
            Fore.RED + "[Multi Line] " +
            Fore.LIGHTYELLOW_EX +
            "Enter/Paste your content." +
            " Ctrl + D or Ctrl + Z (Windows) to submit. " +
            Fore.WHITE
        )

        while True:
            try:
                line = input()
            except EOFError:
                break

            input_text += '\n' + line

    else:
        input_text = input()

    return input_text
