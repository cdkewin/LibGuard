#Chifa Daniel Kewin Homework 1: Library Usage and Security Analysis
import argparse


#Taking the input link from the command line using the argparse module due to its automatic type conversion
#and also built-in help commands, whereas input() is much more flimsy

parser = argparse.ArgumentParser(description="Please enter the URL to the Github Project: ")
parser.add_argument('url', type=str, help='URL to process')
args = parser.parse_args()
print("Processing URL: " + args.url)
link = args.url



