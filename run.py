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



