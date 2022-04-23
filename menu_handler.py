import os
from colorama import Fore
from input_reader import InputReader

class MenuHandler:

    def __init__(self):
        self.input_reader = InputReader()

    def process_menu(self, menu):
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

        self.display_menu(menu)

        response = self.parse_menu_response(menu)

        while not response:
            self.display_menu(menu)
            response = self.parse_menu_response(menu)

        return response

    def clear_screen(self):
        os.system('clear')

    def display_menu(self, menu):
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
        self.clear_screen()
        print(Fore.YELLOW + menu.get('prompt') + Fore.WHITE)
        for key in menu.get('options', []).keys():
            print(f'[{key}] {menu.get("options", {}).get(key).get("prompt")}')

    def parse_menu_response(self, menu):
        """
        Parses the input from the user in response to a menu's prompt
        Ensures that the input is of a correct format and appropriate for the type of prompt given

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
        user_input = self.input_reader.read_input(menu.get('multiline'))

        if menu.get('type') == 'choice':
            response = self.handle_choice_response(menu, user_input)
        elif menu.get('type') == 'input':
            response = self.handle_input_response(menu, user_input)

        return response

    def handle_choice_response(self, menu, response):
        """
        Validates a users input to ensure it's appropriate given the choices available

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
        else:
            return False

    def handle_input_response(self, menu, response):
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
