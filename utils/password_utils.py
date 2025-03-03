"""
Utility functions for handling password input in a cross-platform manner.
"""

import sys
import logging
import os
import traceback

# Platform-specific implementations
if sys.platform == "win32":
    import msvcrt

    def secure_password_input(prompt):
        print(prompt, end="", flush=True)
        password = []
        while True:
            char = msvcrt.getwch()
            if char == "\r":  # enter
                print()
                break
            elif char == "\b":  # backspace
                if password:
                    password.pop()
                    print("\b \b", end="", flush=True)
            elif char == "\x03":  # ctrl+c
                raise KeyboardInterrupt
            else:
                password.append(char)
                print("*", end="", flush=True)
        return "".join(password)

else:
    import tty
    import termios

    def secure_password_input(prompt):
        password = []
        sys.stdout.write(prompt)
        sys.stdout.flush()

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char in ("\x7f", "\x08"):  # backspace/delete
                    if password:
                        password.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                elif char in ("\r", "\n"):  # enter
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                elif char == "\x03":  # ctrl+c
                    raise KeyboardInterrupt
                else:
                    password.append(char)
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return "".join(password)


def get_pdf_password(pdf_path):
    """
    Check if a PDF is password-protected and get the password if needed.
    Returns None if no password is required.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str or None: The password if required, None otherwise
    """
    import pdfplumber
    from pdfminer.pdfdocument import PDFPasswordIncorrect

    # First try without any password
    try:
        with pdfplumber.open(pdf_path, password="") as pdf:
            return None
    except PDFPasswordIncorrect:
        # If we get here, the PDF is password-protected
        filename = os.path.basename(pdf_path)
        logging.info(f"{filename} is password-protected.")
        while True:
            password = secure_password_input(f"Enter password for {filename}: ")
            try:
                # Test if the password works
                with pdfplumber.open(pdf_path, password=password):
                    return password
            except PDFPasswordIncorrect:
                print("\nIncorrect password. Please try again.")
    except Exception as e:
        # Handle other exceptions
        logging.error(f"Error in get_pdf_password: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise
