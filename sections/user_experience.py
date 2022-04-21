from colorama import Fore
from tabulate import tabulate
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
            }
        }

        self.site_aims = []
        self.target_audience = []
        self.user_stories = []

        super().__init__(readme, questions_dict, header="User Experience")

    def set_site_aims(self, site_aims):

        aims_split = site_aims.split('\n')
        for aim in aims_split:
            if aim:
                self.site_aims.append(aim)

    def output_site_aims(self):
        output = "### Site Aims\n\n"

        for aim in self.site_aims:

            output += f" * {aim.capitalize()}\n"

        return output

    def set_target_audience(self, target_audience):

        audience_split = target_audience.split('\n')
        for target in audience_split:
            if target:
                self.target_audience.append(target)

    def output_target_audience(self):

        output = "### Target Audience\n\n"

        for target in self.target_audience:

            output += f" * {target.capitalize()}\n"

        return output

    def set_user_stories(self):

        while True:
            print(Fore.YELLOW + "Action:" + Fore.WHITE)
            action = input()
            print(Fore.YELLOW + "Goal:" + Fore.WHITE)
            goal = input()

            confirmed = input('Confirm Story [Y/N]: \n').upper()
            while confirmed != 'Y' and confirmed != 'N':
                print('Please try again...')
                confirmed = input('Confirm Story [Y/N]: \n')

            if confirmed == 'Y':
                self.user_stories.append({
                    'action': action,
                    'goal': goal
                })

            again = input('Add another story [Y/N]: \n').upper()
            while again != 'Y' and again != 'N':
                print('Please try again...')
                again = input('Add another story [Y/N]:  \n')

            if again == 'N':
                break
        
    def output_user_stories(self):
        headers = ["ID", "GOAL", "ACTION"]
        rows = []

        for i in range(len(self.user_stories)):
            rows.append([i+1, self.user_stories[i]['goal'], self.user_stories[i]['action']])

        return tabulate(rows, headers=headers, tablefmt="github")

    def output_raw(self):

        header_raw = f"## {self.header}"

        output = header_raw + "\n\n" \
            + self.output_site_aims() + "\n\n"\
            + self.output_target_audience() + "\n\n"\
            + self.output_user_stories() + "\n\n"

        return output

