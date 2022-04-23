from .section import Section

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
        demo_link_raw = "You can view the live project here: " + \
            f"<a href='{self.demo_link}' target='_blank' rel='noopener'>" + \
            f"{self.readme.title}</a>"

        output = header_raw + "\n\n" + self.description + \
            "\n\n" + demo_link_raw + "\n\n"

        return output

    def load_section(self, sheet_data):

        print(sheet_data)
        for row in sheet_data:
            if row.get('Data Type') == 'description':
                self.description = row.get('Value')
            elif row.get('Data Type') == 'demo_link':
                self.demo_link = row.get('Value')
            elif row.get('Data Type') == 'intro_image_path':
                self.intro_image = row.get('Value')
        
