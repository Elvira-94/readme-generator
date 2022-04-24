"""
This module is responsible for the core running of Readme Generator.
It is the first module entered when the program is executed.

The module keeps track of user sessions, and handles main menu functionality
"""

import sys
import time
import gspread
from colorama import Fore
from google.oauth2.service_account import Credentials

import menu_helpers
from readme import Readme

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('readme_generator')


def start_animation():
    """
    Animation shown at the launch of the app. Waits 2 seconds before
    clearing
    """
    menu_helpers.clear_screen()
    print(Fore.GREEN)

    #         _____  ______          _____  __  __ ______
    #         |  __ \|  ____|   /\   |  __ \|  \/  |  ____|
    #         | |__) | |__     /  \  | |  | | \  / | |__
    #         |  _  /|  __|   / /\ \ | |  | | |\/| |  __|
    #         | | \ \| |____ / ____ \| |__| | |  | | |____
    # _____ _|_|__\_\______/_/_ __\_\_____/|_|__|_|______|  _____
    # / ____|  ____| \ | |  ____|  __ \     /\|__   __/ __ \|  __ \
    # | |  __| |__  |  \| | |__  | |__) |  /  \  | | | |  | | |__) |
    # | | |_ |  __| | . ` |  __| |  _  /  / /\ \ | | | |  | |  _  /
    # | |__| | |____| |\  | |____| | \ \ / ____ \| | | |__| | | \ \
    #  \_____|______|_| \_|______|_|  \_\/_/    \_\_|  \____/|_|  \_\

    print("           _____  ______          _____  __  __ ______")
    print("          |  __ \\|  ____|   /\\   |  __ \\|  \\/  |  ____|")
    print("          | |__) | |__     /  \\  | |  | | \\  / | |__")
    print("          |  _  /|  __|   / /\\ \\ | |  | | |\\/| |  __|")
    print("          | | \\ \\| |____ / ____ \\| |__| | |  | | |____")
    print("   _____ _|_|__\\_\\______/_/_ __\\_\\_____/|_|__|_|______|  _____")
    print("  / ____|  ____| \\ | |  ____|  __ \\     /\\|__   __/ __ \\|  __ \\ ")
    print(" | |  __| |__  |  \\| | |__  | |__) |   /  \\  | | | |  | | |__) |")
    print(" | | |_ |  __| | . \\ |  __| |  _  /   / /\\ \\ | | | |  | |  _  / ")
    print(" | |__| | |____| |\\  | |____| | \\ \\  / ____ \\| | | |__| | | \\ \\ ")
    print("  \\_____|______|_| \\_|______|_|  \\_\\/_/    \\_\\_|  \\____/|_|  \\_\\")
    print("                                                                ")
    print("                                                                ")
    print("                           LOADING...                           ")
    print(Fore.WHITE)
    time.sleep(2)
    menu_helpers.clear_screen()


def exit_animation():
    """
    Displays an exit message to the user, waits for 2 seconds
    before clearing
    """

    #  ______                 _ _                _
    # /  ____|               | | |              | |
    # | |  __  ___   ___   __| | |__  _   _  ___| |
    # | | |_ |/ _ \ / _ \ / _` | '_ \| | | |/ _ \ |
    # | |__| | (_) | (_) | (_| | |_) | |_| |  __/_|
    # \______|\___/ \___/ \__,_|_.__/ \__, |\___(_)
    #                                  __/ |
    #                                 |___/

    menu_helpers.clear_screen()
    print(Fore.GREEN)
    print("   _____                 _ _                _ ")
    print("  / ____|               | | |              | |")
    print(" | |  __  ___   ___   __| | |__  _   _  ___| |")
    print(" | | |_ |/ _ \\ / _ \\ / _  | '_ \\| | | |/ _ \\ |")
    print(" | |__| | (_) | (_) | (_| | |_) | |_| |  __/_|")
    print("  \\_____|\\___/ \\___/ \\__,_|_.__/ \\__, |\\___(_)")
    print("                                  __/ |       ")
    print("                                 |___/        ")
    print(Fore.WHITE)
    time.sleep(2)
    menu_helpers.clear_screen()


def exit_app():
    """
    Displays an exit message to the user and exits the app
    once complete
    """

    exit_animation()
    sys.exit()


class Session:
    """
    A class to a represent a user's current session in the tool.

    A session is created when a user runs the tool, and is terminated when
    the tool has exited.

    The session handles the core functionality of the tool.

    ...

    Attributes
    ----------

    Methods
    -------
    start()
        Handles main logic of the tool once a session starts.

    main_menu()
        Shows the main menu of the tool to the user.

    get_current_readme()
        Returns the current readme object for the session

    set_current_readme()
        Sets the current readme object for the session

    create_new_readme()
        Instantiates a new readme object and assigns it to the current session

    load_readme()
        Will load a readme from a file

    """

    def __init__(self):
        self.current_readme = None

    def start(self):
        """
        Handles main logic of the tool once a session starts.

        1. Show main menu loop
        """
        start_animation()

        while True:
            self.main_menu()

    def main_menu(self):
        """
        Shows the main menu of the tool to the user.

        If there is a currently loaded readme, options will be catered towards
        this readme, otherwise they will be catered around loading/creating a
        readme to use
        """

        if self.get_current_readme():

            self.get_current_readme().display_menu()

        else:
            menu = menu_helpers.CHOICE_MENU_PROMPT
            menu['options'] = {
                "1": {
                    "prompt": "Create New README File",
                    "action": self.create_new_readme
                },
                "2": {
                    "prompt": "Load Previous README File",
                    "action": self.list_readmes_to_load
                },
                "3": {
                    "prompt": "Exit",
                    "action": exit_app
                }
            }

            response = menu_helpers.process_menu(menu)

            menu.get('options').get(response).get('action')()

    def get_current_readme(self):
        """
        Returns the current readme object for the session
        """
        return self.current_readme

    def set_current_readme(self, readme_object):
        """
        Sets the current readme object for the session
        """
        self.current_readme = readme_object

    def create_new_readme(self):
        """
        Instantiates a new readme object and assigns it to the current session
        """
        print(Fore.YELLOW + "Project Name: " + Fore.WHITE)
        project_name = input()

        readme_object = Readme(self, project_name)
        self.set_current_readme(readme_object)

    def load_readme(self, readme_name):
        """
        Loads a specified readme file data from google sheets,
        creates a readme object and instructs the readme object
        to create appropriate section objects
        """

        readme = Readme(self, readme_name)

        worksheet = SHEET.worksheet(readme_name)

        readme.load_sections(worksheet)

        self.set_current_readme(readme)

    def list_readmes_to_load(self):
        """
        Lists the current Readmes that have been saved to Google Sheets
        """

        all_readme_sheets = SHEET.worksheets()
        menu = {
            "prompt": "Which README would you like to load:",
            "type": "choice",
            "options": {}
        }

        for count, value in enumerate(all_readme_sheets):
            menu["options"][str(count + 1)] = {
                "prompt": value.title,
                "action": self.load_readme
            }

        response = menu_helpers.process_menu(menu)

        menu.get('options').get(response)\
            .get('action')(menu.get('options').get(response).get('prompt'))


def main():
    """
    Main function for the program.
    Create a user session and starts the session
    """
    session = Session()
    session.start()


if __name__ == "__main__":

    main()
