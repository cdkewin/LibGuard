#Chifa Daniel Kewin Homework 1: Library Usage and Security Analysis
import argparse
import shutil
import stat
import subprocess
import os
import json

class Project :
    def __init__(self, libraries):
        self.libraries = libraries
    def getLibraries(self):
        return self.libraries


#Taking the input link from the command line using the argparse module due to its automatic type conversion
#and also built-in help commands, whereas input() is much more flimsy
def main():
    parser = argparse.ArgumentParser(description="Please enter the URL to the Github Project: ")
    parser.add_argument('url', type=str, help='URL to process')
    args = parser.parse_args()
    print("Processing URL: " + args.url)
    link = args.url #Storing the url attribute as 'link' for simplicity


  #  clone_repository(link)
   # create_requirements_file("./ProjectsFromGithub")
    display_imported_libraries_from_project(link)
    security_check()

def handle_remove_readonly(func, path, exc_info):

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)  # Change the permission to writable
        func(path)  # Retry the function after the event handling (os.rmdir) after gaining permission



def clone_repository(github_url):
    destination_path = "./ProjectsFromGithub"
    git_link = github_url
    try:
        print(f"Cloning repository from {github_url} into {destination_path}...")
        subprocess.run(["git", "clone", github_url, destination_path], check=True)
        print("Repository cloned successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}. Failed to clone repository.")
        if os.path.exists(destination_path):  # Check if the directory exists
            shutil.rmtree(destination_path, onerror=handle_remove_readonly)  # Handle permission errors to remove the files
            print("Directory deleted successfully.")
        clone_repository(git_link)  # Retry cloning


def create_requirements_file(project_path):
    try:
        print(f"Generating requirements.txt for project at {project_path}...")

        #Run the pipreqs command to make a requirements text file that will be read later for the user
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
    # Getting the name of the project for a nicer reading from the user
    project_name = link.split("/")[-1]

    print(f'\n\tThe imported libraries used in {project_name}\n')
    with open("./ProjectsFromGithub/requirements.txt", "r") as file:
        # Using a set we store the libraries and remove copies
        libraries = set(line.strip() for line in file if line.strip())  # Strip spaces and ignore empty lines

        # Print each library once
        for library in libraries:
            print(library)


def turn_project_to_object():    # This function will only be called from the security check function which will be called from main
    with open("./ProjectsFromGithub/requirements.txt", "r") as file:
        libraries = set(line.strip() for line in file if line.strip())
    p = Project(libraries)
    return p


def security_check():
    project = turn_project_to_object()
    libraries = project.getLibraries()

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
            print(result.stdout)  # Print the detected issues
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":  # Condition so the script doesn't run if imported as a module only if the main function is called explicitly
    main()



