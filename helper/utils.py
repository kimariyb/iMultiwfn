# -*- coding: utf-8 -*-
"""
utils.py

This module contains some utility functions for iMultiwfn.

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
import glob

import pandas as pd


def exports_data(datas: pd.DataFrame):
    """
    Save the data to a csv file.

    Parameters
    ----------
    datas : pd.DataFrame
        A DataFrame containing the name, atoms, and charges of the molecules.
    """
    # Export descriptors data
    datas.to_excel("results.xlsx", index=False)

    print(datas)
    
    # Export charge data
    charge_names = [
        'Hirshfeld_charge',
        'ADCH_charge',
        'spin_population',
        'electron_density',
        'Laplacian_electron_density',
        'kinetic_energy_density'
    ]

    for i in range(datas.shape[0]):
        charge_list = [datas.iloc[i][charge_names[0]].atoms, datas.iloc[i][charge_names[0]].charges,
                        datas.iloc[i][charge_names[1]].charges, datas.iloc[i][charge_names[2]].charges,
                        datas.iloc[i][charge_names[3]].charges, datas.iloc[i][charge_names[4]].charges,
                        datas.iloc[i][charge_names[5]].charges]

        charge_data = pd.DataFrame(charge_list)

        # convert x axis with y axis
        charge_data = charge_data.T

        charge_data.to_excel(f"charges_{i + 1}.xlsx")


def move_files(source_dir, target_dir, extension='txt'):
    """
    Moves all files with the specified extension from the source directory to the target directory.
    If a file with the same name already exists in the target directory, it will be overwritten.

    source directory: /home/kimariyb/sabreML/data/
    target directory: /home/kimariyb/sabreML/output/

    Parameter
    ---------
    source_dir : str
        The directory containing the files to be moved.
    target_dir : str
        The directory to which the files will be moved.
    extension : str, optional
        The extension of the files to be moved. The default is 'txt'.
    """
    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Move all files with the specified extension to the target directory
    for file in files:
        if file.endswith('.' + extension):
            os.rename(os.path.join(source_dir, file), os.path.join(target_dir, file))


def remove_files(working_dir, extension='wfn'):
    """
    Removes all files with the specified extension from the current directory.

    Parameter
    ---------
    working_dir : str
        The directory containing the files to be removed.
    extension : str, optional
        The extension of the files to be removed. The default is 'wfn'.
    """
    # Get a list of all files in the working directory
    files = os.listdir(working_dir)

    # Remove all files with the specified extension
    for file in files:
        if file.endswith('.' + extension):
            os.remove(os.path.join(working_dir, file))


def get_input_files(input_dir, extension='fchk'):
    """
    Returns a list of all output files in the output directory.

    Parameter
    ---------
    input_dir : str
        The directory containing the output files.
    extension : str, optional
        The extension of the output files to be included in the list. The default is 'fchk'.

    Returns
    -------
    list
        A list of all output files in the output directory.
    """

    input_files = []
    for file in os.listdir(input_dir):
        if file.endswith('.' + extension):
            input_files.append(os.path.join(input_dir, file))
    return input_files


def read_contents(file_path):
    """
    Reads the contents of a file.

    Parameter
    ---------
    file_path : str
        The path to the file to be read.

    Returns
    -------
    str
        The contents of the file.
    """
    with open(file_path, 'r') as f:
        contents = f.read()

    return contents


def get_output_files(output_dir):
    """
    Returns a list of all output files in the output directory.

    Parameter
    ---------
    output_dir : str
        The directory containing the output files.

    Returns
    -------
    list
        A list of cdft txt output files in the output directory.
    list
        A list of other output files in the output directory.
    """
    # split the output files into cdft txt and other output files
    # 首先获取所有的 CDFT txt 文件
    cdft_txt_files = glob.glob(os.path.join(output_dir, '*-CDFT.txt'))

    # 接着获取所有的 txt 文件
    all_txt_files = glob.glob(os.path.join(output_dir, '*.txt'))

    # 然后将 CDFT txt 文件和其他 txt 文件分开
    other_txt_files = list(set(all_txt_files) - set(cdft_txt_files))
    # 其他 txt 文件必须也按照文件名排好顺序，1, 2, 3, 4, 5, 6, 7, 8...
    # 这样才能保证后续的处理顺序正确
    other_txt_files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))

    return cdft_txt_files, other_txt_files
