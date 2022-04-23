from colorama import Fore

class InputReader:
    """
    Class to handle reading of user input from the CLI
    The class will allow multi line input from users for attributes like
    descriptions and will parse users responses accordingly
    ...

    Attributes
    ----------
    NA

    Methods
    -------
    read_input(multiline):
        Reads input from the user in a multiline or single line format 
    """

    def __init__(self):
        pass

    def read_input(self, multiline):
        """
        Adds a section of a given type to the readme object

            Parameters:
                    multiline (bool): Boolean determining if user input can
                    contain multiple newlines

            Returns:
                    input_text (String): The user's input
        """
        input_text = ""

        if multiline:
            print(
                Fore.RED + "[Multi Line] " + Fore.LIGHTYELLOW_EX + 
                "Enter/Paste your content. Ctrl + D or Ctrl + Z (Windows) to submit. " +
                Fore.WHITE
            )

            while True:
                try:
                    line = input()
                except EOFError:
                    break

                input_text += '\n' + line

        else:
            input_text = input()

        return input_text
