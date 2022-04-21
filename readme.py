import sections

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
        self.image_path = ""

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
                    "action": self.preview_readme
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
                    "mapping": sections.IntroSection
                },
                "2": {
                    "prompt": "User Experience",
                    "mapping": sections.UserExperienceSection
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
        self.sections[
            menu.get('options').get(response).get('prompt')
        ] = section

    def preview_readme(self):
        print(self.output_raw())

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

        return output

    def output_to_file(self):

        with open("Generated_README.md","w") as f:
            f.write(self.output_raw())

