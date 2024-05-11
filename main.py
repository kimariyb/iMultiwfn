# -*- coding: utf-8 -*-
"""
main.py

This is the main file of the iMultiwfn program.

1. Select the folder containing the output files
2. Define the commands to be run for each output file
3. Run the batch run function to calculate the wave function for each output file using the commands specified in commands.txt
4. Analyze the output files and generate the final results
5. Generate the final report and present the results to the user
6. End the timer and print the elapsed time

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2024-05-11
"""

from display.version import *

from helper.utils import *
from helper.run import *
from helper.descriptors import *

def main():
    # Start the timer
    start_time = get_current_time()
    
    # Show the welcome message
    show_version()
    
    # Run the batch run function
    # Calculate the wave function for each output file using the commands specified in commands.txt
    # Ask the user if they want to run the batch run Mulitwfn or not
    model = input('Do you want to run the batch run Mulitwfn? (y/n): ')
    if model == 'y':
        # Select the folder containing the input files, like '/home/kimariyb/sabreML/data'
        input_folder = input('Please input the folder containing the input files: ')
        input_files = get_input_files(input_folder)
        if not input_files:
            print('No input files found. Please check the folder path.')
            exit()

        # Define the commands to be run for each output file, like 'commands.txt'
        commands_file = input('Please input the file containing the commands: ')
        commands = parse_commands(commands_file)
        if not commands:
            print('No commands found. Please check the file path.')
            exit()
        
        batch_run(wave_files=input_files, commands=commands)
        # move the output files (*.txt) to the output folder
        move_files('./data', './output', 'txt')
        output_files, cdft_files = get_output_files('./output')
        
    elif model == 'n':
        output_folder = input('Please input the folder containing the output and CDFT files: ')
        output_files, cdft_files = get_output_files(output_folder)
        
    else:
        print('Invalid input. Please input "y" or "n".')
        exit()
    
        
    # Analyze the output files and generate the final results
    results_list = []
    for output_file, cdft_file in zip(output_files, cdft_files):
        result = get_descriptors(cdft_file=cdft_file, other_file=output_file)
        results_list.append(result)
        
    # remove rubbish files
    remove_files('./', 'wfn')
    
    # Generate the final report and present the results to the user
    exports_data(results_list)

    # End the timer
    end_time = get_current_time()

    # Print the elapsed time
    print("Thanks for your use !!!")
    print("SabreML running time: ", get_running_time(start_time, end_time))
    print(f"SabreML finished at: {get_current_date()}. Copyright (c) 2024-2025 Kimariyb.")

    
    
if __name__ == '__main__':
    main()