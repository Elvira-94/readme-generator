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
        self.sections[section_type] = section

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

            print(self.questions_dict[question_index]['question'])
            answer = input()

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
                "setter_function": self.set_description
            },
            2: {
                "question": "Provide a demo link to your project: ",
                "setter_function": self.set_demo_link
            },
            3: {
                "question": "Path to your intro image: ",
                "setter_function": self.set_intro_image
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
