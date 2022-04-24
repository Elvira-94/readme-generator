"""
This module is the parent class for all sections. It contains methods
common to each section and is inherited by them.
"""

from colorama import Fore
import menu_helpers


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
        """
        Each individual section needs to prompt the user to fill out the
        required data needed for the section.

        This function handles the output and input processing of this data.
        """

        for question_index in self.questions_dict:
            menu_helpers.clear_screen()

            # If a particular prompt requires handling that requires anything
            # custom, we call the setter function, and allow that to handle the
            # input.

            # E.g. If building a table, we may have multiple prompts for a user
            # for a particular item.

            # User Stories:
            # 1. Goal
            # 2. Action
            if self.questions_dict[question_index].get('custom_handling'):
                self.questions_dict[question_index]['setter_function']()
            else:
                print(
                    Fore.YELLOW +
                    self.questions_dict[question_index]['question'] +
                    Fore.WHITE
                )

                # A preview function is a function that shows to the user the
                # current value set for a particular piece of data. So that
                # they can see what they would potentially be overwriting when
                # updating a section.
                if self.questions_dict[question_index].get('preview_function'):

                    preview = self.questions_dict[question_index]\
                        .get('preview_function')()

                    # If preview has data, it means there was a previous value
                    # set for this data point
                    if preview:
                        print(
                            '\n' +
                            Fore.MAGENTA +
                            'Current Value: ' +
                            Fore.LIGHTMAGENTA_EX +
                            preview +
                            Fore.WHITE
                        )

                        print(
                            Fore.MAGENTA +
                            'Leave input blank to not modify current value.' +
                            Fore.WHITE
                        )

                answer = menu_helpers.read_input(
                    self.questions_dict[question_index]['multiline']
                )

                self.questions_dict[question_index]['setter_function'](answer)
