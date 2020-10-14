#!/usr/bin/python3

import os
import sys


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
