from colorama import Fore
from tabulate import tabulate
from readme import Readme
from menu_handler import MenuHandler

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('readme_generator')


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
        self.menu_handler = MenuHandler()

    def start(self):
        """
        Handles main logic of the tool once a session starts.

        1. Show main menu loop
        """
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
            menu = {
                "prompt": "What would you like to do:",
                "type": "choice",
                "options": {
                    "1": {
                        "prompt": "Create New README File",
                        "action": self.create_new_readme
                    },
                    "2": {
                        "prompt": "Load Previous README File",
                        "action": self.list_readmes_to_load
                    }
                }
            }

            response = self.menu_handler.process_menu(menu)

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

        readme_object = Readme(project_name, self.menu_handler)
        self.set_current_readme(readme_object)

    def load_readme(self):
        pass
        
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

        response = self.menu_handler.process_menu(menu)

        menu.get('options').get(response).get('action')()
        



def main():
    session = Session()
    session.start()


if __name__ == "__main__":

    main()
