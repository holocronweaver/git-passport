import subprocess


def is_infected():
    """ Checks if the current directory is under Git version control.

        Returns:
            True (bool): If the current directory is a Git repository
            False (bool): If the current directory is not a Git repository

        Raises:
            Exception: If subprocess.Popen() fails
    """
    git_process = subprocess.run([
        "git",
        "rev-parse",
        "--is-inside-work-tree"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if git_process.returncode == 0:
        return True
    else:
        msg = "The current directory does not seem to be a Git repository."
        print(msg)
        return False


def get_config(scope, property):
    """ Get the email address, username of the global or local Git ID.
        Also gets the local remote.origin.url of a Git repository.

        Args:
            scope (str): Search inside a `global` or `local` scope
            property (str): Type of `email` or `name` or `url`

        Returns:
            value (str): A name, email address or url

        Raises:
            Exception: If subprocess.Popen() fails
    """
    git_args = "remote.origin.url" if property == "url" else "user." + property

    git_process = subprocess.run([
        "git",
        "config",
        "--get",
        "--" + scope,
        git_args
    ], capture_output=True)

    value = git_process.stdout.decode("utf-8")
    return value.replace("\n", "")


def set_config(value, property):
    """ Set local user properties for a local Git repository.

        Args:
            value (str): A name or email address
            property (str): Type of `email` or `name`

        Raises:
            Exception: If subprocess.Popen() fails
    """
    subprocess.run([
        "git",
        "config",
        "--local",
        "user." + property,
        value
    ])


def remove_config(verbose=True):
    """ Remove an existing Git identity.

        Raises:
            Exception: If subprocess.Popen() fails
    """
    git_process = subprocess.run([
        "git",
        "config",
        "--local",
        "--remove-section",
        "user"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if verbose:
        if git_process.returncode == 0:
            print("Passport removed.")
        elif git_process.returncode == 128:
            print("No passport set.")
