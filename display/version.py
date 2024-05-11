VERSION = "0.1.0"  # version number
DATE = "2024-05-11"  # release date
AUTHOR = "Kimari Y.B."  # author

import time

from datetime import datetime


def show_version():
    """
    Show version information of SabreML.
    """
    # ASCII art
    ascii_art = f'''
     -----------------------------------------------------------
    |                   =====================                   |
    |                         iMultiwfn                         |
    |                   =====================                   |
    |                        Kimari Y.B.                        |
    |        School of Electronic Science and Engineering       |
    |                     XiaMen University                     |
     -----------------------------------------------------------
        * KYBNMR version {VERSION} on date {DATE}
        * Homepage is https://github.com/kimariyb/iMultiwfn
    '''

    print(ascii_art)
    

def get_current_date():
    """
     Returns the current date in the format "YYYY-MM-DD HH:MM:SS".

    Returns
    -------
    str
        The current date in the format "YYYY-MM-DD HH:MM:SS".
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_time():
    """
    Returns the current time in seconds since the epoch.

    Returns
    -------
    float
        The current time in seconds since the epoch.
    """
    return time.time()


def get_running_time(start_time, end_time):
    """
    Calculates the running time between two times.

    Parameters
    ----------
    start_time : float
        The start time in seconds since the epoch.
    end_time : float
        The end time in seconds since the epoch.

    Returns
    -------
    str
        The running time in hours, minutes and seconds.

    Examples
    --------
    >>> start_time = get_current_time()
    >>> # do something
    >>> end_time = get_current_time()
    >>> print(get_running_time(start_time, end_time))
    01:02:30 is 1 hour, 2 minutes and 30 seconds.
    """

    running_time = end_time - start_time
    hours = int(running_time // 3600)
    minutes = int((running_time % 3600) // 60)
    seconds = int(running_time % 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d} is {hours} hour(s), {minutes} minute(s) and {seconds} second(s)."
