"""
This module contais the ReadMe class definition
"""

from colorama import Fore
import sections
import menu_helpers


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

    def __init__(self, session, title):
        self.session = session
        self.title = title
        self.sections = {}
        self.image_path = ""

        self.section_types = {
            'Introduction': sections.IntroSection,
            'User Experience': sections.UserExperienceSection
        }

        self.intro_section = None

    def display_menu(self):
        """
        Displays the readme menu that is shown when a readme is currently
        attached to the active session
        """

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
                },
                "4": {
                    "prompt": "Return to Main Menu",
                    "action": self.detach_from_session
                }
            }
        }

        response = menu_helpers.process_menu(menu)

        menu.get('options').get(response).get('action')()

    def detach_from_session(self):
        """
        Detach the current readme object from the active session
        Essentially returns the user to the main menu
        """
        self.session.set_current_readme(None)

    def add_section(self):
        """
        Adds a section of a given type to the readme object
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

        response = menu_helpers.process_menu(menu)

        # If a section has already been created before, call that
        # section object rather than creating a new one
        if self.sections.get(menu.get('options').get(response).get('prompt')):
            self.sections.get(menu.get('options').get(response).get('prompt'))\
                .display_menu()
        else:
            section = menu.get('options').get(response).get('mapping')(self)

            section.display_menu()
            self.sections[
                menu.get('options').get(response).get('prompt')
            ] = section

    def load_sections(self, worksheet):
        """
        Given a google worksheet object, build section objects accordingly
        and attach them to the current readme object

            Parameters:
            worksheet (gspread worksheet): The worksheet object returned from
            Google sheets
        """

        worksheet_data = worksheet.get_all_records()

        section_records = {}

        for row in worksheet_data:
            if section_records.get(row.get('Section Type')):
                section_records[row.get('Section Type')].append(row)
            else:
                section_records[row.get('Section Type')] = [row]

        for item in section_records.items():
            section_class = self.section_types.get(item[0])

            if section_class:
                section_object = section_class(self)
                section_object.load_section(item[1])

                self.sections[item[0]] = section_object
                print(self.sections)
            else:
                raise Exception(f"Unknown Class Found in README: {item[0]}")

    def preview_readme(self):
        """
        Calls self.output_raw and prints the contents of the output to
        the teminal.

        Waits for the user to provide any input before moving back to the
        previous menu
        """
        print(Fore.YELLOW + "\n\n\n|||||||||||||||||||||||")
        print("||                   ||")
        print("||       README      ||")
        print("||       BELOW       ||")
        print("||                   ||")
        print("|||||||||||||||||||||||\n\n\n" + Fore.WHITE)

        print(self.output_raw())
        print(
            Fore.RED + "If the readme is longer than the terminal window,\n"
            + "please scroll up to view more content" + Fore.WHITE
        )
        input(Fore.YELLOW + "Press enter to continue.." + Fore.WHITE)

    def output_raw(self):
        """
        Outputs the readme file in raw format includig all added sections

            Parameters:
                    NA

            Returns:
                output (Str): The raw format of the readme file sections
        """

        output = ""
        for section_type in self.sections.items():
            output += section_type[1].output_raw()

        return output

    def output_to_file(self):
        """
        Calls self.output_raw and wries the results to a README file locally.
        This will only be useful if code is being ran loally and not in Heroku
        """
        with open("Generated_README.md", "w", encoding="utf-8") as file:
            file.write(self.output_raw())
