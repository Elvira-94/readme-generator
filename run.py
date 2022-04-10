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

    def __init__(self, title):
        self.title = title
        self.section_classes = {
            'Intro': IntroSection
        }
        self.sections = {}

    def add_section(self, section_type):
        """
        Adds a section of a given type to the readme object

            Parameters:
                    section_type (str): String outlining the type of section to add. E.g. 'Intro'

            Returns:
                    NA
        """
        section = self.section_classes[section_type](self)
        section.populate_section_info()
        self.sections[section_type] = section

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

    def populate_section_info(self):

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

def main():

    print(Fore.YELLOW + "Project Name: " + Fore.WHITE)
    project_name = input()

    readme_object = Readme(project_name)
    readme_object.add_section('Intro')
    readme_object.output_to_file()


if __name__ == "__main__":
    input_reader = InputReader()
    main()