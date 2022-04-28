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
        Sets the site_aims attribute. Each newline entered by the
        user is treated as an individual site aim
        """

        menu = menu_helpers.CHOICE_MENU_PROMPT
        menu['options'] = {
            "1": {
                "prompt": "Add story",
                "action": self.add_story
            },
            "2": {
                "prompt": "Edit story",
                "action": self.edit_story
            },
            "3": {
                "prompt": "View stories",
                "action": self.view_all_stories
            },
            "4": {
                "prompt": "Return",
                "action": "break"
            }
        }

        while True:
            response = menu_helpers.process_menu(menu)

            if response == "4":
                break

            menu['options'].get(response)['action']()

    def view_all_stories(self, pause=True):

        if len(self.user_stories) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no user stories. Please add some!"
                + Fore.WHITE
            )

            input(
                Fore.YELLOW +
                "Press enter to continue.."
                + Fore.WHITE
            )
            return

        menu_helpers.clear_screen()
        for i, item in enumerate(self.user_stories):
            print('-------------------------')
            print(Fore.BLUE + f'[{i+1}]: ' + Fore.WHITE)
            print('-------------------------')

            print(
                Fore.GREEN + "Action: " + Fore.WHITE +
                "\n" + item['action'] + '\n'
            )

            print(
                Fore.GREEN + "Goal: " + Fore.WHITE +
                "\n" + item['goal']
            )

            # dont add a seperator if on the last story
            if i == len(self.user_stories) - 1:
                print('-------------------------\n\n')
            else:
                print('\n\n')

        if pause:
            input(Fore.YELLOW + 'Press enter to continue' + Fore.WHITE)

    def add_story(self, write_to_sheet=True):
        """
        Prompts the user for the goal and action of a user story
        """

        menu_helpers.clear_screen()
        print(Fore.YELLOW + "What is the action of this story? " + Fore.WHITE)
        action = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

        menu_helpers.clear_screen()
        print(Fore.YELLOW + "What is the goal of this story? " + Fore.WHITE)
        goal = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

        self.user_stories.append({
            "goal": goal,
            "action": action
        })

        if write_to_sheet:
            stories_string = ""
            for count, story in enumerate(self.user_stories):
                if count == len(self.user_stories) - 1:
                    stories_string += story['goal'] + '|' + story['action']
                else:
                    stories_string += story['goal'] + '|' + story['action'] + '\n'

            self.write_section_item_to_sheet(
                'user_stories',
                stories_string
            )

    def edit_story(self):
        """
        Prompts the user to choose a story to edit, and once chosen
        allows the user to re-enter story info
        """

        if len(self.user_stories) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no stories. Please add some!"
                + Fore.WHITE
            )
            input(
                Fore.YELLOW +
                "Press enter to continue.."
                + Fore.WHITE
            )
            return

        while True:

            menu_helpers.clear_screen()
            self.view_all_stories(pause=False)

            print(
                Fore.YELLOW +
                '\nWhich story would you like to edit?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.user_stories)):

                while True:
                    menu_helpers.clear_screen()
                    story_to_edit = self.user_stories[int(response)-1]

                    print(
                        Fore.GREEN + "Action: " + Fore.WHITE +
                        "\n" + story_to_edit['action'] +
                        Fore.GREEN + "Goal: " + Fore.WHITE +
                        "\n" + story_to_edit['goal']
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the story you wish to edit? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue
                    elif confirmed == 'N':
                        break
                    else:
                        menu_helpers.clear_screen()
                        print(Fore.YELLOW + "What is the action of this story? " + Fore.WHITE)
                        action = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

                        menu_helpers.clear_screen()
                        print(Fore.YELLOW + "What is the goal of this story? " + Fore.WHITE)
                        goal = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

                        self.user_stories[int(response)-1] = {
                            "goal": goal,
                            "action": action
                        }

                        return

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
