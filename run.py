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
            'Intro':IntroSection
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
    
    """

    def __init__(self, readme):
        self.readme = readme

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
        super().__init__(readme)