"""
This module represents the User Experience section of the README

It contains information related to how the app caters to its user,
such as who the intended users are, the purpose of the app for the
users, things the users can do with the app, and the flow of the
app
"""

from colorama import Fore

import menu_helpers
from .section import Section


class FeaturesSection(Section):
    """
    A class to represent the Features Section of the readme.
    """

    def __init__(self, readme):
        questions_dict = {
            1: {
                "question": "Please provide app feaures:",
                "setter_function": self.set_features,
                "custom_handling": True
            }
        }

        self.features = []

        super().__init__(readme, questions_dict, header="Features")

    def set_features(self):
        """
        Sets the site_aims attribute. Each newline entered by the
        user is treated as an individual site aim
        """

        menu = menu_helpers.CHOICE_MENU_PROMPT
        menu['options'] = {
            "1": {
                "prompt": "Add feature",
                "action": self.add_feature
            },
            "2": {
                "prompt": "Edit feature",
                "action": self.edit_feature
            },
            "3": {
                "prompt": "View features",
                "action": self.view_all_features
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

    def add_feature(self):
        """
        Prompts the user for the name of a feature, creates the feature object
        and assigns to the features class
        """

        menu_helpers.clear_screen()
        feature_name = input(Fore.YELLOW + "Feature Name: " + Fore.WHITE)
        feature = Feature(self, feature_name, len(self.features)+1)
        feature.display_menu()

        self.features.append(feature)

    def edit_feature(self):
        """
        Prompts the user to choose a feature to edit, and once chosen
        allows the user to re-enter feature info
        """

        if len(self.features) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no features. Please add some!"
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
            self.view_all_features(pause=False, detailed=False)

            print(
                Fore.YELLOW +
                '\nWhich feature would you like to edit?' +
                Fore.WHITE
            )
            response = input()

            if int(response)-1 in range(len(self.features)):

                while True:
                    menu_helpers.clear_screen()
                    feature_to_edit = self.get_feature(int(response)-1)

                    print(feature_to_edit.output_raw())

                    print(
                        Fore.YELLOW +
                        'Is this the feature you wish to edit? [Y/N]' +
                        Fore.WHITE
                    )

                    confirmed = input().upper()

                    if confirmed not in ('Y', 'N'):
                        input('Please try again! Press enter to continue..')
                        continue

                    if confirmed == 'N':
                        break

                    feature_to_edit.edit_feature()
                    return

    def get_feature(self, feature_index):
        """
        Returns a feature object at the given index
        """
        try:
            return self.features[feature_index]
        except ValueError as err:
            raise err

    def view_all_features(self, pause=True, detailed=True):
        """
        Displays all features to the terminal and awaits user confirmation 
        before returning
        """

        if len(self.features) == 0:
            menu_helpers.clear_screen()
            print(
                Fore.RED +
                "This readme currently has no features. Please add some!"
                + Fore.WHITE
            )

            input(
                Fore.YELLOW +
                "Press enter to continue.."
                + Fore.WHITE
            )
            return

        menu_helpers.clear_screen()
        for i, item in enumerate(self.features):
            print(
                Fore.GREEN +
                f"[{i+1}] {item.feature_name}" +
                Fore.WHITE
            )

            if detailed:
                print(item.output_raw())

        if pause:
            input(Fore.YELLOW + 'Press enter to continue' + Fore.WHITE)

    def output_raw(self):
        """
        Outputs the content of the section in GitHub markdown format
        as expected for the README document structure
        """

        header_raw = f"## {self.header}"

        output = header_raw + "\n\n"

        for feature in self.features:
            output += feature.output_raw()

        return output

    def load_section(self, sheet_data):
        """
        Given data from a google spreadsheet readme, this
        function reads the data for its attributes and populates
        them
        """

        # Combine data for individual features where Data Type shows
        # the relation between features
        #
        # E.g.
        #
        # Section Type |    Data Type   | Value
        #    Feature   | 1 | image_path | image.png
        #
        features = {}
        for row in sheet_data:
            feature_split = row.get('Data Type').split('|')

            if not features.get(feature_split[0]):
                features[feature_split[0]] = {}

            if feature_split[1] == 'point_of_note':
                if features[feature_split[0]].get(feature_split[1]):
                    features[feature_split[0]][feature_split[1]].append(row.get('Value'))
                else:
                    features[feature_split[0]][feature_split[1]] = [row.get('Value')]
            else:
                features[feature_split[0]][feature_split[1]] = row.get('Value')

        for key, item in features.items():
            feature = Feature(self, item.get('feature_name'), key, False)
            feature.load_feature(item)
            self.features.append(feature)


class Feature(Section):
    """
    This class represents a single feature of the features section.
    """

    def __init__(self, feature, feature_name, feature_number, write_to_file=True):
        self.set_feature_name(feature_name, write_to_file)
        self.feature_number = str(feature_number)
        self.points_of_note = []
        self.image_path = ""
        self.image_alt = ""

        questions_dict = {
            1: {
                "question": "Points of Note:",
                "setter_function": self.add_points_of_note,
                "custom_handling": True
            },
            2: {
                "question": "Image path for this feature:",
                "setter_function": self.add_image_path,
                "multiline": False,
                "preview_function": self.get_image_path
            }
        }

        super().__init__(feature.readme, questions_dict, header=feature.header)

    def edit_feature(self):
        """
        Allows a user to edit a feature by calling specific functions to modify
        class attributes
        """
        self.questions_dict = {
            1: {
                "question": "Feature Title:",
                "setter_function": self.set_feature_name,
                "multiline": False,
                "preview_function": self.get_feature_name
            },
            2: {
                "question": "Points of Note:",
                "setter_function": self.edit_point_of_note,
                "custom_handling": True
            },
            3: {
                "question": "Image path for this feature:",
                "setter_function": self.add_image_path,
                "multiline": False,
                "preview_function": self.get_image_path
            }
        }
        self.display_menu()

    def set_feature_name(self, name, write_to_file=True):
        """
        Sets the feature_name attribute
        """
        if name:
            self.feature_name = name

            if write_to_file:

                self.write_section_item_to_sheet(
                    self.feature_number + '|feature_name',
                    self.feature_name
                )

    def get_feature_name(self):
        """
        Returns the feature_name attribute
        """
        return self.feature_name

    def view_points_of_note(self, pause=False, detailed=False):
        """
        Displays the features points of note to the terminal and if set
        awaits user confirmation before returning
        """
        menu_helpers.clear_screen()
        for i, item in enumerate(self.points_of_note):
            print(
                Fore.GREEN +
                f"[{i+1}] {item}" +
                Fore.WHITE
            )

            if detailed:
                print(item.output_raw())

        if pause:
            input(Fore.YELLOW + 'Press enter to continue' + Fore.WHITE)

    def edit_point_of_note(self):
        """
        Displays points of notes and when selected, allows a user to edit
        a specific point
        """
        while True:

            menu_helpers.clear_screen()
            if self.points_of_note:
                self.view_points_of_note()

                print(
                    Fore.YELLOW +
                    '\nWhich point would you like to edit? ' +
                    '(Simply press enter to skip)' +
                    Fore.WHITE
                )
                response = input()

                if not response:
                    return

            else:
                self.add_points_of_note()
                return

            if int(response)-1 in range(len(self.points_of_note)):

                while True:
                    menu_helpers.clear_screen()
                    point_to_edit = self.points_of_note[int(response)-1]

                    print(point_to_edit)

                    print(
                        Fore.YELLOW +
                        '\n\nIs this the point you wish to edit? [Y/N]' +
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
                        '\n' +
                        Fore.MAGENTA +
                        'Current Value: ' +
                        Fore.LIGHTMAGENTA_EX +
                        self.points_of_note[int(response)-1] +
                        Fore.WHITE
                    )

                    print(
                        Fore.YELLOW +
                        '\n\nPlease enter a new value:' +
                        Fore.WHITE
                    )
                    self.points_of_note[int(response)-1] = input(' -> ')

                    points_string = ""
                    for count, point in enumerate(self.points_of_note):
                        if count == len(self.points_of_note) - 1:
                            points_string += point
                        else:
                            points_string += point + '\n'

                    self.write_section_item_to_sheet(
                        self.feature_number + '|point',
                        points_string
                    )
                    return

    def add_point_of_note(self, point):
        """
        Adds an additional point to the feature
        """
        if point:
            self.points_of_note.append(point)

    def output_points_of_note(self):
        """
        Returns points of note for the feature
        """

        output = ""
        for point in self.points_of_note:
            output += f" * {point}\n"

        return output

    def delete_point_of_note(self, index_to_delete):
        """
        Removes a point of note from the points_of_note at the
        given index
        """

        del self.points_of_note[index_to_delete]

    def add_image_path(self, image_path, write_to_file=True):
        """
        Sets the image path for the feature
        """

        if image_path:

            self.image_path = image_path

            if write_to_file:
                self.write_section_item_to_sheet(
                    self.feature_number + '|image_path',
                    self.image_path
                )

    def get_image_path(self):
        """
        Returns the image path for the feature
        """

        return self.image_path

    def set_image_alt(self, alt):
        """
        Sets the image alt text for the feature
        """

        self.image_alt = alt

    def get_image_alt(self):
        """
        Returns the image alt text for the feature
        """

        return self.image_alt

    def output_image_path(self):
        """
        Outputs the image path for the feature in GitHub markdown format
        as expected for the README document structure
        """

        output = f'<p align="center"><img src="{self.get_image_path()} ' +\
            f'width="50%" height="50%" alt="{self.get_image_alt()}"></p>' +\
            '<br />\n'

        return output

    def add_points_of_note(self, write_to_file=True):
        """
        Asks the user for the points of note for the feature
        """

        while True:
            print(Fore.YELLOW + "- Feature points of note -\n\n" + Fore.WHITE)

            point = input(Fore.YELLOW + " -> " + Fore.WHITE)

            self.add_point_of_note(point)

            again = input(
                Fore.GREEN +
                'Add another point [Y/N]: \n' +
                Fore.WHITE
            ).upper()

            while again not in ('Y', 'N'):
                print('Please try again...')
                again = input(
                    Fore.GREEN +
                    'Add another point [Y/N]: \n' +
                    Fore.WHITE
                ).upper()
            if again == 'N':
                break

            points_string = ""

            menu_helpers.clear_screen()

        if write_to_file:
            points_string = ""
            for count, point in enumerate(self.points_of_note):
                if count == len(self.points_of_note) - 1:
                    points_string += point
                else:
                    points_string += point + '\n'

            self.write_section_item_to_sheet(
                self.feature_number + '|point',
                points_string
            )
        return

    def output_raw(self):
        """
        Outputs the content of the feature in GitHub markdown format
        as expected for the README document structure
        """

        output = ""

        output += f"### {self.feature_name}:\n\n"
        output += self.output_points_of_note()
        output += f"\n{self.output_image_path()}\n\n"

        return output

    def load_feature(self, feature_json):
        """
        Loads feature attributes from worksheet data
        """
        if feature_json.get('feature_name'):
            self.set_feature_name(feature_json['feature_name'], write_to_file=False)

        if feature_json.get('point_of_note'):
            for point in feature_json.get('point_of_note'):
                self.add_point_of_note(point)

        if feature_json.get('image_path'):
            self.add_image_path(feature_json['image_path'], write_to_file=False)
