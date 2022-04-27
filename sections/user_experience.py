"""
This module represents the User Experience section of the README

It contains information related to how the app caters to its user,
such as who the intended users are, the purpose of the app for the
users, things the users can do with the app, and the flow of the
app
"""

from colorama import Fore
from tabulate import tabulate

import menu_helpers
from .section import Section


class UserExperienceSection(Section):
    """
    A class to represent the User Experience Section of the readme.

    Subsections
    - Site Aims
    - Target Audience
    - User Stories
    - Site Structure
    - Flow Chart
    """

    def __init__(self, readme):
        questions_dict = {
            1: {
                "question": "What are the aims of the site: ",
                "setter_function": self.set_site_aims,
                "multiline": True
            },
            2: {
                "question": "Who is the target audience of the site:",
                "setter_function": self.set_target_audience,
                "multiline": True
            },
            3: {
                "question": "Please Provide User Stories:",
                "setter_function": self.set_user_stories,
                "custom_handling": True
            },
            4: {
                "question": "Please provide the path to your flowchart image:",
                "setter_function": self.set_flowchart,
                "multiline": False
            }
        }

        self.site_aims = []
        self.target_audience = []
        self.user_stories = []
        self.flowchart = None

        super().__init__(readme, questions_dict, header="User Experience")

    def set_site_aims(self, site_aims, write_to_sheet=True):
        """
        Sets the site_aims attribute. Each newline entered by the
        user is treated as an individual site aim
        """
        if site_aims:
            aims_split = site_aims.split('\n')
            for aim in aims_split:
                if aim:
                    self.site_aims.append(aim)

            if write_to_sheet:
                self.write_section_item_to_sheet('aims', site_aims)

    def output_site_aims(self):
        """
        Outputs the site_aims attribute in GitHub Markdown format
        """

        output = "### Site Aims\n\n"

        for aim in self.site_aims:

            output += f" * {aim.capitalize()}\n"

        return output

    def set_target_audience(self, target_audience, write_to_sheet=True):
        """
        Sets the target_audience attribute. Each newline entered by the
        user is treated as an individual target audience entry
        """

        if target_audience:
            audience_split = target_audience.split('\n')
            for target in audience_split:
                if target:
                    self.target_audience.append(target)

            if write_to_sheet:
                self.write_section_item_to_sheet(
                    'target_audience',
                    target_audience
                )

    def output_target_audience(self):
        """
        Outputs the target_audience attribute in GitHub Markdown format
        """

        output = "### Target Audience\n\n"

        for target in self.target_audience:

            output += f" * {target.capitalize()}\n"

        return output

    def set_user_stories(self, write_to_sheet=True):
        """
        Sets the target_audience attribute. Each newline entered by the
        user is treated as an individual target audience entry
        """

        while True:
            print(Fore.YELLOW + "- User Stories -\n\n" + Fore.WHITE)

            print(Fore.YELLOW + "Action:" + Fore.WHITE)
            action = input()
            print(Fore.YELLOW + "Goal:" + Fore.WHITE)
            goal = input()

            confirmed = input(
                Fore.GREEN +
                '\n\nConfirm Story [Y/N]: \n' +
                Fore.WHITE
            ).upper()

            while confirmed not in ('Y', 'N'):
                print('Please try again...')
                confirmed = input('Confirm Story [Y/N]: \n')

            if confirmed == 'Y':
                self.user_stories.append({
                    'action': action,
                    'goal': goal
                })

            again = input(
                Fore.GREEN +
                'Add another story [Y/N]: \n' +
                Fore.WHITE
            ).upper()

            while again not in ('Y', 'N'):
                print('Please try again...')
                again = input('Add another story [Y/N]:  \n')

            if again == 'N':
                break

            menu_helpers.clear_screen()

        stories_string = ""
        for story in self.user_stories:
            stories_string += story['goal'] + '|' + story['action'] + '\n'

        if write_to_sheet:
            self.write_section_item_to_sheet(
                'user_stories',
                stories_string
            )

    def output_user_stories(self):
        """
        Outputs the user_stories attribute in GitHub Markdown format
        using tabulate library to format the table
        """

        headers = ["ID", "GOAL", "ACTION"]
        rows = []

        for count, value in enumerate(self.user_stories):
            rows.append([count + 1, value['goal'], value['action']])

        return tabulate(rows, headers=headers, tablefmt="github")

    def set_flowchart(self, flowchart_path, write_to_sheet=True):
        """
        Sets the flowchart attribute.
        """
        if flowchart_path:
            self.flowchart = flowchart_path
            if write_to_sheet:
                self.write_section_item_to_sheet('flowchart', self.flowchart)

    def output_flowchart(self):
        """
        Outputs the flowchart attribute as an image in GitHub Markdown format
        """

        output = "### Flowchart\n\n"
        output += f"![{self.readme.title} Flowchart](" \
            + self.readme.image_path + '/' + self.flowchart \
            + "})\n\n"
        return output

    def output_raw(self):
        """
        Outputs the content of the section in GitHub markdown format
        as expected for the README document structure
        """

        header_raw = f"## {self.header}"

        output = header_raw + "\n\n" \
            + self.output_site_aims() + "\n\n"\
            + self.output_target_audience() + "\n\n"\
            + self.output_user_stories() + "\n\n"\
            + self.output_flowchart() + "\n\n"

        return output

    def load_section(self, sheet_data):
        """
        Given data from a google spreadsheet readme, this
        function reads the data for its attributes and populates
        them
        """

        for row in sheet_data:
            if row.get('Data Type') == 'aims':
                site_aims = row.get('Value')
                self.set_site_aims(site_aims, write_to_sheet=False)
            elif row.get('Data Type') == 'target_audience':
                target_audience = row.get('Value')
                self.set_target_audience(target_audience, write_to_sheet=False)
            elif row.get('Data Type') == 'user_stories':
                stories = row.get('Value')
                for story in stories.split('\n'):
                    goal = story.split('|')[0]
                    action = story.split('|')[1]

                    self.user_stories.append({
                        "goal": goal,
                        "action": action
                    })
            elif row.get('Data Type') == 'flowchart':
                self.set_flowchart(row.get('Value'))
