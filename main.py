
"""
Chifa Daniel Kewin Homework 1: Library Usage and Security Analysis

This script downloads a Python project from GitHub, identifies all used libraries, and checks for known security issues.
The script performs the following actions:
- Clones a GitHub repository based on the URL provided via command-line.
- Outputs the used libraries, ensuring they are only displayed once
- Runs a security check for each library to identify any known vulnerabilities using 'safety'

Requirements:
- The script needs to be run in a Python 3 environment with necessary libraries like `pipreqs`, `safety`.
- Check requirements.txt for the exact versions used.

Usage from command-line:
    cd <project path>
    python main.py <github_url>

"""

import argparse
import os
import shutil
import stat
import subprocess
import sys



#Taking the input link from the command line using the argparse module due to its automatic type conversion
#and also built-in help commands, whereas input() is much more flimsy
def main():

    """
        The main function is the entry point of the script. It's used for controlling the flow of the script:
        1. Parsing the command-line argument to retrieve the GitHub URL.
        2. Cloning the repository from GitHub.
        3. Generating a `requirements.txt` file for the cloned repository.
        4. Displaying all libraries used in the project.
        5. Performing a security check for known vulnerabilities in the libraries.

        This function ensures that all those steps above are executed in the correct order.
        The main() function exists to ensure the fact that the script doesn't run if it's imported as a module
        and only run if called explicitly.

        Args:
            None: This function does not take any parameters as it retrieves the URL directly from the command-line.

        Returns:
            None: This function doesn't return anything. It calls other functions for a more modular script.
        """

    parser = argparse.ArgumentParser(description="Please enter the URL to the Github Project: ")
    parser.add_argument('url', type=str, help='URL to process')
    args = parser.parse_args()
    print("Processing URL: " + args.url)
    link = args.url #Storing the url attribute as 'link' for simplicity


    clone_repository(link)
    create_requirements_file("./ProjectsFromGithub")
    display_imported_libraries_from_project(link)
    security_check()

def handle_remove_readonly(func, path, exc_info):
    """
       A helper function to handle read-only files when deleting them.

       This function is called by `shutil.rmtree` if a directory cannot be removed
       It changes the files' permissions to make it writable
       and then retries the removal operation.

       Args:
           func : The function that needs to be retried after permission change
           path : The path of the file or directory to be removed.
           exc_info : Exception information passed when the error occurs.
       """

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)  #Change the permission to writable
        func(path)  #Retry the function after the event handling



def clone_repository(github_url):
    """
    Clones a GitHub repository to a local directory called ProjectsFromGithub

    This function attempts 3 times to clone the repository from the given URL.
    If it still fails after 3 times, the program will exit.

    Args:
        github_url : The GitHub repository URL to clone.

    Raises:
        sys.exit(): If the cloning operation fails after 3 attempts.
    """
    i = 0
    if i < 3:  #After 3 attempts of cloning the repository the program will stop
        destination_path = "./ProjectsFromGithub"
        git_link = github_url

        try:
            print(f"Cloning repository from {github_url} into {destination_path}...")
            subprocess.run(["git", "clone", github_url, destination_path], check=True)
            print("Repository cloned successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}. Failed to clone repository.")
            if os.path.exists(destination_path):  #Check if the directory exists
                shutil.rmtree(destination_path,
                              onerror=handle_remove_readonly)  #Handle permission errors to remove the files
                print("Directory deleted successfully.")
                clone_repository(git_link)  #Retry cloning
        i += 1
    if i >= 3:
        print("Cloning failed. Number of attempts: " + str(i))
        sys.exit()


def create_requirements_file(project_path):
    """
    Generates a `requirements.txt` file for the downloaded project.

    This function runs `pipreqs` to create the `requirements.txt`.
    It captures any output or error messages and prints them to the console.

    Args:
        project_path : The path to the project directory where the `requirements.txt` will be created
        and its given by the main function

    Raises:
        subprocess.CalledProcessError : If the `pipreqs` command fails.
        Exception : For any other unexpected errors during the process.
    """
    try:
        print(f"Generating requirements.txt for project at {project_path}...")

        #Run the pipreqs command to make a requirements text file that will be outputted later for the user
        result = subprocess.run(
            ["pipreqs", project_path, "--force"],  #The subprocess command
            check=True,  #Will raise an error if the command fails
            capture_output=True,  #Captures stdout and stderr
            text=True  #Decodes the output to a string (instead of bytes)
        )
        print(result.stdout)
        print("requirements.txt generated successfully!")

    except subprocess.CalledProcessError as e:
        #If pipreqs fails, this will print the error and stderr
        print(f"Error during pipreqs execution: {e}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        #For any other unexpected errors as a safety net
        print(f"Unexpected error: {e}")


def display_imported_libraries_from_project(link) :
    """
        Displays the libraries imported in the project from the `requirements.txt` file created.

        This function reads the `requirements.txt` file generated for the project and outputs
        the list of libraries that the project depends on ensuring that each library is displayed once.

        Args:
            link : The URL of the GitHub repository
        """

    #Getting the name of the project for a nicer reading from the user
    project_name = link.split("/")[-1]

    print(f'\n\tThe imported libraries used in {project_name}\n')
    with open("./ProjectsFromGithub/requirements.txt", "r") as file:
        #Using a set we store the libraries and remove copies
        libraries = set(line.strip() for line in file if line.strip())  #Strip spaces and ignore empty lines

        #Print each library once
        for library in libraries:
            print(library)



def security_check():
    """
      Performs a security check on the project's dependencies.

      This function uses the `safety` package to check the `requirements.txt` file for known
      security vulnerabilities in the libraries used by the project. It outputs any detected
      issues to the console.

      The script uses 'check' instead of 'scan' so the user doesn't have to log in

      Raises:
          Exception : If an error occurs during the security check process.
      """

    try:
        result = subprocess.run(
            ["safety", "check", "-r", "requirements.txt"],
            cwd="./ProjectsFromGithub",
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("No security issues found in the project.")
        else:
            print("Security issues detected:")
            print(result.stdout)  #Print the detected issues
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":  #Condition so the script doesn't run if imported as a module only if the main function is called explicitly
    main()



