#!/usr/bin/python3

import os
import sys
from os.path import isfile, join
import shlex
from parser import get_parser
from pathlib import Path
from Options import Options

GREEN_C = '\033[92m'
END_C = '\033[0m'
shell_prompt = GREEN_C + 'cbshell % ' + END_C
parser = get_parser()


def warning(message):
    return message


def error(message):
    return "Error: " + message


def parse_arguments(shell_input):
    # Parsing arguments
    args = shlex.split(shell_input)
    return args


def is_executable(file_path):
    """Returns if file at file_path is executable
    """
    return os.access(file_path, os.X_OK)


def get_execfiles(path):
    items = os.listdir(path)
    filter_execfiles = lambda item: isfile(join(path, item)) and is_executable(join(path, item))
    execfiles = list(filter(filter_execfiles, items))
    return execfiles


def selection_system_calls():
    current_path = os.getcwd()
    execfiles = get_execfiles(current_path)
    args = create_and_handle_options(current_path, execfiles)
    return args


def create_and_handle_options(path, execfiles):

    if execfiles == []:
        message = warning("No executables files available.")
        raise Exception(message)

    options = Options(path, execfiles)
    print(options)
    args = input("Please select an option (with arguments if needed): ")

    args = parse_arguments(args)
    options_number = 0
    try:
        option_number = int(args[0])
    except Exception as e:
        message = error("Option should be a number.")
        raise Exception(message)
    
    exec_path, filename  = options.get(option_number)
    args[0] = exec_path
    return args


def selection_using_bash(search_path, maxdepth):
    pipein, pipeout = os.pipe() # Allows retrieval of find command output
    pid = os.fork()

    execfiles = []
    # If path is making reference to home
    search_path = search_path.replace('~', str(Path.home()))
    # Getting rid of ending / if needed be
    search_path = search_path.rstrip('/')
    if pid < 0:
        print("Could not fork a process.")
    elif pid == 0:
        try:
            shell_input = "find {} -maxdepth {} -executable -type f".format(search_path, maxdepth)
            args = parse_arguments(shell_input)

            # Pipes' read and write are mutually exclusive
            # we must close the read before writting and vice-versa
            os.close(pipein)
            os.dup2(pipeout, 1) # Substituting stdout for pipeout

            os.execvp(args[0], args)
        except Exception as e:
            print(e)
            os._exit(127) # To force exit if something went wrong
    elif pid > 0:
        os.waitpid(pid, 0)

        os.close(pipeout)
        # fdopen() works similar to open but its input is a file descriptor
        with os.fdopen(pipein, "r") as f:
            # eliminating a trailing new line character
            # and getting rid of ./ part of the filename
            remove_endlines = lambda word: word.rstrip('\n').replace(search_path+'/', '')
            execfiles = sorted(list(map(remove_endlines, f.readlines())))
    
    args = create_and_handle_options(search_path, execfiles)
    return args


def get_max_depth(args):
    global parser
    args = [] if len(args) < 2 else args[1:]
    try:
        args = parser.parse_args(args)
        maxdepth = args.maxdepth
        search_path = args.path
        return (search_path, maxdepth)
    except SystemExit as e:
        # Argparse tries to exit the interpreter if problem parsing arguments
        # we DO NOT want that
        raise Exception('')

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

        if args[0] == 'selection':
            try:
               search_path,  maxdepth = get_max_depth(args)
               args = selection_using_bash(search_path, maxdepth)
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
                os._exit(127) # Forcing exit if could not run execvp
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
