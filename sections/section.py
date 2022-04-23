from colorama import Fore

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

            if self.questions_dict[question_index].get('custom_handling'):
                self.questions_dict[question_index]['setter_function']()
            else:
                print(Fore.YELLOW + self.questions_dict[question_index]['question'] + Fore.WHITE)
                answer = self.readme.menu_handler.input_reader.read_input(self.questions_dict[question_index]['multiline'])
                self.questions_dict[question_index]['setter_function'](answer)