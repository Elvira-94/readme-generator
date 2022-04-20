import colorama
from colorama import Fore

class InputReader:
    """
    Class to handle reading of user input from the CLI
    The class will allow multi line input from users for attributes like descriptions
    and will parse users responses accordingly

    ...

    Attributes
    ----------
    NA

    Methods
    -------
    read_input(multiline):
        Reads input from the user in a multiline or single line format 
    """

    def __init__(self):
        pass

    def read_input(self, multiline):
        """
        Adds a section of a given type to the readme object

            Parameters:
                    multiline (bool): Boolean determining if user input can contain multiple newlines

            Returns:
                    input_text (String): The user's input
        """
        input_text = ""

        if multiline:
            print(Fore.RED + "[Multi Line] " + Fore.LIGHTYELLOW_EX + "Enter/Paste your content. Ctrl + D or Ctrl + Z (Windows) to submit. " + Fore.WHITE)

            while True:
                try:
                    line = input()
                except EOFError:
                    break
                
                input_text += '\n' + line
            
        else:
            input_text = input()

        return input_text


class Readme:
    """
    A class to represent a readme entity

    ...

    Attributes
    ----------
    title : str
        the title of the project

    Methods
    -------
    add_section(section_type):
        Adds a section of a given type to the readme object
    """

    def __init__(self, title, menu_handler):
        self.title = title
        self.sections = {}

        self.menu_handler = menu_handler
        self.intro_section = None

    def display_menu(self):
        menu = {
            "prompt": "What would you like to do:",
            "type": "choice",
            "options": {
                "1": {
                    "prompt": "Add Section",
                    "action": self.add_section
                },
                "2": {
                    "prompt": "View Readme",
                    "action": self.output_raw
                },
                "3": {
                    "prompt": "Create Readme File",
                    "action": self.output_to_file
                }
            }
        }

        response = self.menu_handler.process_menu(menu)

        menu.get('options').get(response).get('action')()

    def add_section(self):
        """
        Adds a section of a given type to the readme object

            Parameters:
                    section_type (str): String outlining the type of section to add. E.g. 'Intro'

            Returns:
                    NA
        """
        menu = {
            "prompt": "Which section type would you like to add?",
            "type": "choice",
            "options": {
                "1": {
                    "prompt": "Introduction",
                    "mapping": IntroSection
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

        response = self.menu_handler.process_menu(menu)
        section = menu.get('options').get(response).get('mapping')(self)

        section.display_menu()
        self.sections[menu.get('options').get(response).get('prompt')] = section

    def output_raw(self):
        """
        Outputs the readme file in raw format includig all added sections

            Parameters:
                    NA

            Returns:
                output (Str): The raw format of the readme file sections
        """

        output = ""
        for section_type in self.sections:
            output += self.sections[section_type].output_raw()

        print(output)

    def output_to_file(self):

        with open("Generated_README.md","w") as f:
            f.write(self.output_raw())


class Section:
    """
    A class to a represent generic document section. 

    ...

    Attributes
    ----------
    readme : Readme
        The readme object that the section belongs to

    Methods
    -------
    populate_section_info()
        Loops through section questions and calls a setter function for the
        section to populate the section attribute with user input
    """

    def __init__(self, readme, questions_dict, header):
        self.readme = readme
        self.header = header
        self.questions_dict = questions_dict

    def display_menu(self):
        
        for question_index in self.questions_dict:


            print(Fore.YELLOW + self.questions_dict[question_index]['question'] + Fore.WHITE)
            answer = input_reader.read_input(self.questions_dict[question_index]['multiline'])
            self.questions_dict[question_index]['setter_function'](answer)


class IntroSection(Section):
    """
    A class to represent the Intro Section of the readme.

    ...

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(self, readme):

        questions_dict = {
            1: {
                "question": "Describe your project: ",
                "setter_function": self.set_description,
                "multiline": True
            },
            2: {
                "question": "Provide a demo link to your project: ",
                "setter_function": self.set_demo_link,
                "multiline": False
            },
            3: {
                "question": "Path to your intro image: ",
                "setter_function": self.set_intro_image,
                "multiline": False
            },
        }

        super().__init__(readme, questions_dict, header="Introduction")

        self.description = ""
        self.demo_link = ""
        self.intro_image = ""

    def set_description(self, description):
        self.description = description

    def set_demo_link(self, demo_link):
        self.demo_link = demo_link
       
    def set_intro_image(self, intro_image_path):
        self.intro_image = intro_image_path

    def output_raw(self):

        header_raw = f"## {self.header}"
        demo_link_raw = f"You can view the live project here: <a href='{self.demo_link}' target='_blank' rel='noopener'>{self.readme.title}</a>"

        output = header_raw + "\n\n" + self.description + "\n\n" + demo_link_raw

        return output


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
                        "action": self.load_readme
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
        """
        Will load a readme from a file
        WIP
        """
        pass


def main():
    session = Session()
    session.start()


if __name__ == "__main__":
    input_reader = InputReader()
    main()