#Chifa Daniel Kewin Homework 1: Library Usage and Security Analysis
import argparse
import shutil
import stat
import subprocess
import os


#Taking the input link from the command line using the argparse module due to its automatic type conversion
#and also built-in help commands, whereas input() is much more flimsy
def main():
    parser = argparse.ArgumentParser(description="Please enter the URL to the Github Project: ")
    parser.add_argument('url', type=str, help='URL to process')
    args = parser.parse_args()
    print("Processing URL: " + args.url)
    link = args.url #Storing the url attribute as 'link' for simplicity


    clone_repository(link)
    create_requirements_file("./ProjectsFromGithub")

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


if __name__ == "__main__":  #Condition so the script doesn't run if imported as a module only if the main function is called explicitly
    main()



