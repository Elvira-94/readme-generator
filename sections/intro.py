"""
This module represents the Introduction of the README
It contains information about the project allows the reader
to access the project.
"""

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
                "preview_function": self.get_descrption,
                "setter_function": self.set_description,
                "multiline": True
            },
            2: {
                "question": "Provide a demo link to your project: ",
                "preview_function": self.get_demo_link,
                "setter_function": self.set_demo_link,
                "multiline": False
            },
            3: {
                "question": "Path to your intro image: ",
                "preview_function": self.get_intro_image,
                "setter_function": self.set_intro_image,
                "multiline": False
            },
        }

        self.description = ""
        self.demo_link = ""
        self.intro_image = ""

        super().__init__(readme, questions_dict, header="Introduction")

    def set_description(self, description):
        """
        Sets the description attribute
        """

        if description:
            self.description = description
            self.write_section_item_to_sheet('description', self.description)

    def get_descrption(self):
        """
        Returns the description attribute
        """

        return self.description

    def set_demo_link(self, demo_link):
        """
        Sets the demo_link attribute
        """

        if demo_link:
            self.demo_link = demo_link
            self.write_section_item_to_sheet('demo_link', self.demo_link)

    def get_demo_link(self):
        """
        Returns the demo_link attribute
        """

        return self.demo_link

    def set_intro_image(self, intro_image_path):
        """
        Sets the intro_image attribute
        """

        if intro_image_path:
            self.intro_image = intro_image_path
            self.write_section_item_to_sheet(
                'intro_image_path',
                self.intro_image
            )

    def get_intro_image(self):
        """
        Returns the intro_image attribute
        """

        return self.intro_image

    def output_raw(self):
        """
        Outputs the content of the section in GitHub markdown format
        as expected for the README document structure
        """

        header_raw = f"## {self.header}"

        demo_link_raw = "You can view the live project here: " + \
            f"<a href='{self.demo_link}' target='_blank' rel='noopener'>" + \
            f"{self.readme.title}</a>"

        output = header_raw + "\n\n" + \
            self.description + "\n\n" + \
            demo_link_raw + "\n\n"

        return output

    def load_section(self, sheet_data):
        """
        Given data from a google spreadsheet readme, this
        function reads the data for its attributes and populates
        them
        """

        for row in sheet_data:
            if row.get('Data Type') == 'description':
                self.description = row.get('Value')
            elif row.get('Data Type') == 'demo_link':
                self.demo_link = row.get('Value')
            elif row.get('Data Type') == 'intro_image_path':
                self.intro_image = row.get('Value')

    def find_section_sheet_rows(self, item):
        """
        Finds the rows in the spreadsheet that correspond with the section type
        """

        section_matches = self.readme.worksheet.findall(
            self.header,
            in_column=1
        )
        found_row = None
        for cell in section_matches:
            if self.readme.worksheet.cell(cell.row, cell.col+1).value == item:
                found_row = cell.row
                break

        return found_row

    def write_section_item_to_sheet(self, item, value):
        """
        This function takes a given attribute and value and writes them
        to the worksheet.

        If a record for this item exists, it will overwrite it
        or else it will add a row to the bottom of the worksheet
        """

        row = self.find_section_sheet_rows(item)
        if not row:
            row = self.readme.find_next_empty_sheet_row()

        self.readme.worksheet.update_cell(row, 3, value)
