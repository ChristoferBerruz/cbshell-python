#!/usr/bin/python3

import os
import sys
from os.path import isfile, join


class Options(object):

    def __init__(self):
        self._dicc = {}
        self._current_n = 1

    def insert(self, parent_path, file_name):
        exec_path = join(parent_path, file_name)
        self._dicc[self._current_n] = (exec_path, file_name)
        self._current_n += 1
    
    def get(self, option_number):
        if 0<= option_number <= self._current_n:
            return self._dicc[option_number]
        else:
            raise Exception("Option is not valid")

    def add_list(self, parent_path, filename_list):
        for filename in filename_list:
            self.insert(parent_path, filename)

    def __str__(self):
        res = ''
        for key, (exec_path, file_name) in self._dicc.items():
            res += '{:3d}    {}\n'.format(key, file_name)
        return res


WARNING_C = '\033[93m'
END_C = '\033[0m'
shell_prompt = WARNING_C + 'cbshell % ' + END_C

def parse_arguments(shell_input):
    
    # Ideally, every argument is separated by a single white space
    words = shell_input.split(' ')
    
    # But not everything is ideal...
    # Cleaning empty strings when there are extra white spaces
    words = [word for word in words if word != '']
    return words


def is_executable(file_path):
    """Returns if file at file_path is executable
    """
    return os.access(file_path, os.X_OK)

def get_execfiles(path):
    items = os.listdir(path)
    filter_execfiles = lambda item: isfile(join(path, item)) and is_executable(join(path, item))
    execfiles = list(filter(filter_execfiles, items))
    return execfiles

def selection():
    current_path = os.getcwd()
    execfiles = get_execfiles(current_path)

    options = Options()
    options.add_list(current_path, execfiles)

    print(options)
    args = input("Please select an option (with arguments if needed): ")

    args = parse_arguments(args)
    options_number = 0
    try:
        option_number = int(args[0])
    except Exception as e:
        raise Exception("Option should be a number.")
    
    exec_path, _ = options.get(option_number)
    args[0] = exec_path
    return args


def main():
    while(True):
        shell_input = input(shell_prompt)
        args = parse_arguments(shell_input)

        # Prompt shell in a new line if user presses enter
        # without any characters or all white spaces
        if args == []:
            continue

        # Return if exit command
        if args[0] == 'exit':
            break

        if args[0] == "selection":
            try:
                args = selection()
            except Exception as e:
                print(e)
                continue

        # Check if background process and modify args accordingly
        background = args[-1] == '&'
        if background and len(args) == 1:
            # The only character is '&'
            print("cbshell: syntax error near unexpected token `&'")
            continue


        args = args[0:len(args)-1] if background else args

        pid = os.fork()

        if pid < 0:
            print("Could not fork a process.")
        elif pid == 0:
            try:
                os.execvp(args[0], args)
            except Exception as e:
                print(e)
        elif pid > 0 and not background:
            os.waitpid(pid, 0)
    
    sys.exit(0)

def driver():
    try:
        main()
    except KeyboardInterrupt as interrupt:
        print()
        driver()

if __name__ == '__main__':
    print("**To exit custom shell just type exit**\n")
    driver()
