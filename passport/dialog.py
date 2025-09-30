import sys

INDENT = ' ' * 4

def get_input(pool):
    """ Prompt a user to select a number from a list of numbers representing
        available Git IDs. Optionally the user can choose `q` to quit the
        selection process.

        Args:
            pool (list): A list of numbers representing available Git IDs

        Returns:
            None (NoneType): If the user quits the selection dialog
            selection (int): A number representing a Git ID chosen by a user
    """
    while True:
        # Redirect sys.stdin to an open filehandle from which input()
        # is able to read
        sys.stdin = open("/dev/tty")
        selection = input("» Select an [ID] or enter «(q)uit» to exit: ")

        try:
            selection = int(selection)

            if selection in pool:
                return selection
        except ValueError:
            if selection == "q" or selection == "quit":
                return None
            continue
        finally:
            # Reset sys.stdin to its default value, even if we return early when
            # an exception occurs.
            sys.stdin = sys.__stdin__


def print_choices(choices):
    """ Prints a list of available Git IDs containing properties ID, «scope»,
        name, email and service.

        Args:
            choices (dict): git ID candidates
    """
    for choice_key, choice in choices.items():
        id_type = "Global" if choice.get("flag") == "global" else "Passport"
        lines = [
            f"~:{id_type} ID: {choice_key}",
            f"{INDENT}. User:   {choice['name']}",
            f"{INDENT}. E-Mail: {choice['email']}",
        ]

        service = choice.get("service")
        if service:
            lines.append(f"{INDENT}. Service: {service}")

        signingkey = choice.get("signingkey")
        if signingkey:
            lines.append(f"{INDENT}. Signing Key: {signingkey}")

        msg = '\n'.join(lines) + '\n'
        print(msg)
