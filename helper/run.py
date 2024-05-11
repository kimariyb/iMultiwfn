# -*- coding: utf-8 -*-
"""
run.py

This module contains run-related functions for Multiwfn.

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

import os
import subprocess


def _view_bar(current, total, bar_length=20):
    """
    Print a progress bar.

    Parameters
    ----------
    current : int
        current progress
    total : int
        total progress
    bar_length : int, optional
        length of the progress bar, by default 20
    """
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = '' * (bar_length - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, int(round(percent * 100))), end='\r')
    print()


def _run(wave_file, commands) -> str:
    """
    According commands execute Multiwfn for a given wave function file.

    Parameters
    ----------
    wave_file : str
        path to the wave function file
    commands : list
        list of commands to execute

    Returns
    -------
    str
        output file name of the Multiwfn output

    Raises
    ------
    ValueError
        if the command is not found in the wave function file
    """
    if not os.path.isfile(wave_file):
        raise ValueError("Wave function file not found: {}".format(wave_file))

    # write output stream to file
    input_stream = '\n'.join(list(map(str, commands)))

    # The output file name is the same as the wave function file with a.txt extension
    output_file = wave_file.replace('.fchk', '.txt')

    # construct command line arguments
    args = f'Multiwfn {wave_file} << EOF > {output_file}\n{input_stream}\nEOF\n'

    # execute command
    subprocess.run(args, shell=True)

    print('\n')

    return output_file


def batch_run(wave_files, commands):
    """
    Run Multiwfn for a list of wave function files with the same commands.

    Parameters
    ----------
    wave_files : list
        list of paths to the wave function files
    commands : list
        list of commands to execute

    Returns
    -------
    list
        list of output file names of the Multiwfn outputs
    list
        list of CDFT file names of the Multiwfn outputs
    """
    output_files = []
    cdft_files = []
    files_number = len(wave_files)

    # check if there are any wave function files
    assert files_number > 0, "No wave function files provided !"
    print(f'Total {files_number} wave function files to run!\n')
    print(f'Running Multiwfn for {files_number} wave function files...')

    # run Multiwfn for each wave function file
    for i, wave_file in enumerate(wave_files):
        # update progress bar
        print(f'Running Multiwfn for {i + 1} of {files_number} wave function files: {wave_file}...')
        _view_bar(i + 1, files_number)
        output_file = _run(wave_file, commands)
        output_files.append(output_file)

        # CDFT calculation will generate a CDFT.txt file in the current folder
        # rename it to ${name}-CDFT.txt file, ${name} is the name of the wave function file
        cdft_file = os.path.splitext(wave_file)[0] + "-CDFT.txt"
        os.rename("CDFT.txt", cdft_file)
        cdft_files.append(cdft_file)
        
        # print completion message
        print(f'Multiwfn for {wave_file} completed !')

    return output_files, cdft_files


def parse_commands(commands_file):
    """
    Parse a file containing Multiwfn commands.

    Parameters
    ----------
    commands_file : str
        path to the file containing Multiwfn commands

    Returns
    -------
    list
        list of commands
    """
    with open(commands_file, 'r') as f:
        commands = f.readlines()

    # remove leading/trailing white spaces and empty lines
    commands = [line.strip() for line in commands if line.strip()]

    return commands