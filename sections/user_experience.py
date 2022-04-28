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

        self.site_aims = []
        self.target_audience = []
        self.user_stories = []
        self.flowchart = None

        super().__init__(readme, {}, header="User Experience")

    def display_menu(self):
        """
        Displays the menu for the user experience section to the user
        and calls the appropriate function based on user response
        """
        menu = menu_helpers.CHOICE_MENU_PROMPT
        menu['options'] = {
            "1": {
                "prompt": "Manage Site Aims",
                "action": self.set_site_aims
            },
            "2": {
                "prompt": "Manage Target Audience",
                "action": self.set_target_audience
            },
            "3": {
                "prompt": "Manage User Stories",
                "action": self.set_user_stories
            },
            "4": {
                "prompt": "Manage Flowchart Image Path",
                "action": self.set_flowchart
            },
            "5": {
                "prompt": "Return",
                "action": "break"
            }
        }

        response = menu_helpers.process_menu(menu)

        if menu['options'].get(response, {})['action'] == 'break':
            return

        menu['options'].get(response, {})['action']()

    def set_site_aims(self):
        """
        Shows a menu to allow a user to manage the site aims of the section
        """

        menu = menu_helpers.CHOICE_MENU_PROMPT
        menu['options'] = {
            "1": {
                "prompt": "Add Site Aim",
                "action": self.add_site_aim
            },
            "2": {
                "prompt": "Edit Site Aim",
                "action": self.edit_site_aim
            },
            "3": {
                "prompt": "View Site Aims",
                "action": self.view_all_site_aims
            },
            "4": {
                "prompt": "Delete Site Aim",
                "action": self.delete_site_aim
            },
            "5": {
                "prompt": "Return",
                "action": "break"
            }
        }

        while True:
            response = menu_helpers.process_menu(menu)

            if response == "5":
                break

            menu['options'].get(response)['action']()

    def view_all_site_aims(self, pause=True):
        """
        Displays all site aims to the terminal and if set,
        awaits user input before continuing
        """

        if len(self.site_aims) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no site aims. Please add some!"
                + Fore.WHITE
            )

            input(
                Fore.YELLOW +
                "Press enter to continue.."
                + Fore.WHITE
            )
            return

        menu_helpers.clear_screen()
        for i, item in enumerate(self.site_aims):
            print('-------------------------\n')
            print(Fore.BLUE + f'[{i+1}]: ' + item + Fore.WHITE)

            # dont add a seperator if on the last story
            if i == len(self.site_aims) - 1:
                print('-------------------------\n\n')

        if pause:
            input(Fore.YELLOW + 'Press enter to continue' + Fore.WHITE)

    def add_site_aim(self, write_to_sheet=True):
        """
        Prompts the user for the site aim and sets it
        """

        menu_helpers.clear_screen()
        print(Fore.YELLOW + "Please enter the site aim to add: " + Fore.WHITE)
        aim = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

        self.site_aims.append(aim)

        if write_to_sheet:
            aims_string = ""
            for count, aim in enumerate(self.site_aims):
                if count == len(self.site_aims) - 1:
                    aims_string += aim
                else:
                    aims_string += aim + '\n'

            self.write_section_item_to_sheet(
                'site_aims',
                aims_string
            )

    def edit_site_aim(self, write_to_sheet=True):
        """
        Prompts the user to choose an aim to edit, and once chosen
        allows the user to re-enter aim info
        """

        if len(self.site_aims) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no site aims. Please add some!"
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
            self.view_all_site_aims(pause=False)

            print(
                Fore.YELLOW +
                '\nWhich aim would you like to edit?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.site_aims)):

                while True:
                    menu_helpers.clear_screen()
                    aim_to_edit = self.site_aims[int(response)-1]

                    print(
                        Fore.BLUE + aim_to_edit + Fore.WHITE
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the aim you wish to edit? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    menu_helpers.clear_screen()
                    print(
                        Fore.YELLOW +
                        "Please enter the new aim value:" +
                        Fore.WHITE
                    )
                    aim = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

                    self.site_aims[int(response)-1] = aim

                    if write_to_sheet:
                        aims_string = ""
                        for count, aim in enumerate(self.site_aims):
                            if count == len(self.site_aims) - 1:
                                aims_string += aim
                            else:
                                aims_string += aim + '\n'

                        self.write_section_item_to_sheet(
                            'aims',
                            aims_string
                        )

                    return

    def delete_site_aim(self, write_to_sheet=True):
        """
        Prompts the user to choose an aim to delete, and once chosen
        deletes the entry
        """

        if len(self.site_aims) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no site aims. Please add some!"
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
            self.view_all_site_aims(pause=False)

            print(
                Fore.YELLOW +
                '\nWhich aim would you like to delete?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.site_aims)):

                while True:
                    menu_helpers.clear_screen()
                    aim_to_delete = self.site_aims[int(response)-1]

                    print(
                        Fore.BLUE + aim_to_delete + Fore.WHITE
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the aim you wish to delete? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    del self.site_aims[int(response)-1]

                    if write_to_sheet:
                        aims_string = ""
                        for count, aim in enumerate(self.site_aims):
                            if count == len(self.site_aims) - 1:
                                aims_string += aim
                            else:
                                aims_string += aim + '\n'

                        self.write_section_item_to_sheet(
                            'aims',
                            aims_string
                        )

                    return

    def load_site_aims(self, site_aims):
        """
        Loads the site aims for the class from worksheet data
        """
        if site_aims:
            aims_split = site_aims.split('\n')
            for aim in aims_split:
                if aim:
                    self.site_aims.append(aim)

    def load_user_stories(self, user_stories):
        """
        Loads the user stories for the class from worksheet data
        """
        for story in user_stories.split('\n'):
            goal = story.split('|')[0]
            action = story.split('|')[1]

            self.user_stories.append({
                "goal": goal,
                "action": action
            })

    def load_flowchart(self, flowchart):
        """
        Sets the flowchart attribute from worksheet data
        """
        self.flowchart = flowchart

    def output_site_aims(self):
        """
        Outputs the site_aims attribute in GitHub Markdown format
        """

        output = "### Site Aims\n\n"

        for aim in self.site_aims:

            output += f" * {aim.capitalize()}\n"

        return output

    def set_target_audience(self):
        """
        Shows a menu to the user allowing them to manage the target audience of the section
        """

        menu = menu_helpers.CHOICE_MENU_PROMPT
        menu['options'] = {
            "1": {
                "prompt": "Add Target Audience",
                "action": self.add_target_audience
            },
            "2": {
                "prompt": "Edit Target Audience",
                "action": self.edit_target_audience
            },
            "3": {
                "prompt": "View Target Audiences",
                "action": self.view_all_target_audiences
            },
            "4": {
                "prompt": "Delete Target Audience",
                "action": self.delete_target_audience
            },
            "5": {
                "prompt": "Return",
                "action": "break"
            }
        }

        while True:
            response = menu_helpers.process_menu(menu)

            if response == "5":
                break

            menu['options'].get(response)['action']()

    def view_all_target_audiences(self, pause=True):
        """
        Displays the target audiences to the screen and if set
        awaits user input before returning
        """

        if len(self.target_audience) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no target audience. " +
                "Please add some!" +
                + Fore.WHITE
            )

            input(
                Fore.YELLOW +
                "Press enter to continue.."
                + Fore.WHITE
            )
            return

        menu_helpers.clear_screen()
        for i, item in enumerate(self.target_audience):
            print('-------------------------\n')
            print(Fore.BLUE + f'[{i+1}]: ' + item + Fore.WHITE)

            # dont add a seperator if on the last story
            if i == len(self.target_audience) - 1:
                print('-------------------------\n\n')

        if pause:
            input(Fore.YELLOW + 'Press enter to continue' + Fore.WHITE)

    def add_target_audience(self, write_to_sheet=True):
        """
        Prompts the user for a target audience entry
        """

        menu_helpers.clear_screen()
        print(Fore.YELLOW + "Please enter the target audience to add: " + Fore.WHITE)
        target_audience = input(Fore.YELLOW + ' -> ' + Fore.WHITE)

        self.target_audience.append(target_audience)

        if write_to_sheet:
            target_audience_string = ""
            for count, target_audience in enumerate(self.target_audience):
                if count == len(self.target_audience) - 1:
                    target_audience_string += target_audience
                else:
                    target_audience_string += target_audience + '\n'

            self.write_section_item_to_sheet(
                'target_audience',
                target_audience_string
            )

    def edit_target_audience(self, write_to_sheet=True):
        """
        Prompts the user to choose a target audience to edit, and once chosen
        allows the user to re-enter target_audience info
        """

        if len(self.target_audience) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no target audience." +
                " Please add some!" +
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
            self.view_all_target_audiences(pause=False)

            print(
                Fore.YELLOW +
                '\nWhich target audience would you like to edit?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.target_audience)):

                while True:
                    menu_helpers.clear_screen()
                    target_audience_to_edit = self.target_audience[
                        int(response)-1
                    ]

                    print(
                        Fore.BLUE + target_audience_to_edit + Fore.WHITE
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the target audience you wish to edit?' +
                        '[Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    menu_helpers.clear_screen()
                    print(
                        Fore.YELLOW +
                        "Please enter the new target audience value:" +
                        Fore.WHITE
                    )
                    target_audience = input(
                        Fore.YELLOW +
                        ' -> ' +
                        Fore.WHITE
                    )

                    self.target_audience[int(response)-1] = target_audience

                    if write_to_sheet:
                        target_audience_string = ""
                        for count, target_audience in enumerate(
                            self.target_audience
                        ):
                            if count == len(self.target_audience) - 1:
                                target_audience_string += target_audience
                            else:
                                target_audience_string += target_audience + '\n'

                        self.write_section_item_to_sheet(
                            'target_audience',
                            target_audience_string
                        )

                    return

    def delete_target_audience(self, write_to_sheet=True):
        """
        Prompts the user to choose a target audience to delete, and once chosen
        deletes the entry
        """

        if len(self.target_audience) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no target audience. " +
                "Please add some!" +
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
            self.view_all_target_audiences(pause=False)

            print(
                Fore.YELLOW +
                '\nWhich target audience would you like to delete?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.target_audience)):

                while True:
                    menu_helpers.clear_screen()
                    target_audience_to_edit = self.target_audience[
                        int(response)-1
                    ]

                    print(
                        Fore.BLUE + target_audience_to_edit + Fore.WHITE
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the target audience you wish to delete? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    del self.target_audience[int(response)-1]

                    if write_to_sheet:
                        target_audience_string = ""
                        for count, target_audience in enumerate(
                            self.target_audience
                        ):
                            if count == len(self.target_audience) - 1:
                                target_audience_string += target_audience
                            else:
                                target_audience_string += target_audience + '\n'

                        self.write_section_item_to_sheet(
                            'target_audience',
                            target_audience_string
                        )

                    return

    def load_target_audience(self, target_audience):
        """
        Sets the target_audience attribute. Each newline entered by the
        user is treated as an individual target audience entry
        """

        if target_audience:
            audience_split = target_audience.split('\n')
            for target in audience_split:
                if target:
                    self.target_audience.append(target)

    def output_target_audience(self):
        """
        Outputs the target_audience attribute in GitHub Markdown format
        """

        output = "### Target Audience\n\n"

        for target in self.target_audience:

            output += f" * {target.capitalize()}\n"

        return output

    def set_user_stories(self):
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
                "prompt": "Delete story",
                "action": self.delete_story
            },
            "5": {
                "prompt": "Return",
                "action": "break"
            }
        }

        while True:
            response = menu_helpers.process_menu(menu)

            if response == "5":
                break

            menu['options'].get(response)['action']()

    def view_all_stories(self, pause=True):
        """
        Displays all stories to the user and if set,
        awaits user input before returning
        """

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

    def edit_story(self, write_to_sheet=True):
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
                        "\n" + story_to_edit['action'] + '\n' +
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

                    if confirmed == 'N':
                        break

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

                    return

    def delete_story(self, write_to_sheet=True):
        """
        Prompts the user to choose a story to edit, and once chosen
        deletes the entry
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
                '\nWhich story would you like to delete?' +
                Fore.WHITE
            )

            response = input()

            if int(response)-1 in range(len(self.user_stories)):

                while True:
                    menu_helpers.clear_screen()
                    story_to_edit = self.user_stories[int(response)-1]

                    print(
                        Fore.GREEN + "Action: " + Fore.WHITE +
                        "\n" + story_to_edit['action'] + '\n' +
                        Fore.GREEN + "Goal: " + Fore.WHITE +
                        "\n" + story_to_edit['goal']
                    )

                    print(
                        Fore.YELLOW +
                        '\nIs this the story you wish to delete? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    del self.user_stories[int(response)-1]

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

    def set_flowchart(self, write_to_sheet=True):
        """
        Sets the flowchart attribute.
        """
        menu_helpers.clear_screen()
        print(
            Fore.YELLOW +
            "Please enter the path to your flowchart image:" +
            Fore.WHITE
        )

        flowchart_path = input(
            Fore.YELLOW +
            " -> " +
            Fore.WHITE
        )

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
                self.load_site_aims(site_aims)
            elif row.get('Data Type') == 'target_audience':
                target_audience = row.get('Value')
                self.load_target_audience(target_audience)
            elif row.get('Data Type') == 'user_stories':
                stories = row.get('Value')
                self.load_user_stories(stories)
            elif row.get('Data Type') == 'flowchart':
                self.load_flowchart(row.get('Value'))
