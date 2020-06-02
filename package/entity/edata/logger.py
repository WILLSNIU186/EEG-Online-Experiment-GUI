#!/usr/bin/env python
import datetime
from . import variables, constants


class MyLogger:
    """Class used to write logs into file, console or both."""

    @staticmethod
    def print_log(log_string):
        """
        Returns bandpass filtered data between the frequency ranges specified in the input.
        Args:
            log_string (string): string to be printed as log.
        Returns:
            None
        """
        if variables.Variables.get_current_environment() == constants.CONSTANTS.ENV_DEVELOPMENT:
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(time_stamp, " ", log_string)


    @staticmethod
    def info(log_string):
        """
        Returns bandpass filtered data between the frequency ranges specified in the input.
        Args:
            log_string (string): string to be printed as log.
        Returns:
            None
        """
        if variables.Variables.get_current_environment() == constants.CONSTANTS.ENV_DEVELOPMENT:
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(time_stamp, " ", log_string)
