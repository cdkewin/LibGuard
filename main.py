#Chifa Daniel Kewin Homework 1: Library Usage and Security Analysis
import argparse
import subprocess



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



def clone_repository(github_url):
    destination_path = "./ProjectsFromGithub"
    try:
        print(f"Cloning repository from {github_url} into {destination_path}...")
        subprocess.run(["git", "clone", github_url, destination_path], check=True)
        print("Repository cloned successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}. Failed to clone repository.")






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



