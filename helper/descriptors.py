# -*- coding: utf-8 -*-
"""
descriptors.py

This module provides functions to read the output files of iMultiwfn and extract the descriptors.

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

import re
import numpy as np

from helper.utils import read_contents


class Molecule:
    """
    A class to store molecule.
    """

    def __init__(self, name, atoms: list, charges: list):
        self.name = name
        self.atoms = atoms
        self.charges = charges

    def __str__(self):
        return f"Molecule(name={self.name}, atoms={self.atoms}, charge={self.charges})"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, key):
        return self.atoms[key], self.charges[key]

    def __iter__(self):
        for atom, charge in zip(self.atoms, self.charges):
            yield atom, charge

    def to_dict(self):
        return {'name': self.name, 'atoms': self.atoms, 'charges': self.charges}

    @classmethod
    def from_dict(cls, d):
        return cls(name=d['name'], atoms=d['atoms'], charges=d['charges'])


def _read_charge(charge_lines, charge_type):
    """
    Read the charge from the output file.

    Parameters
    ----------
    charge_lines : list
        The lines containing the charge information.
    charge_type : str
        The type of charge. Either 'Hirshfeld', 'RESP', 'ADCH' or 'spin'.

    Returns
    -------
    Molecule
        A Molecule object containing the name, atoms, and charge.
    """
    atoms = []
    charges = []
    # RESP charge
    if charge_type == 'RESP':
        for line in charge_lines:
            parts = line.split()
            # 原子名称和电荷值
            atom_name = parts[0] + parts[1]
            charge = float(parts[2])
            atoms.append(atom_name)
            charges.append(charge)

    # Hirshfeld charge
    if charge_type == 'Hirshfeld':
        for line in charge_lines:
            parts = line.split()
            atom_identifier = parts[4] + parts[5]  # 原子名称
            charge = float(parts[7])  # 转换为浮点数
            # 清理原子标识符中的空格
            atom_identifier = atom_identifier.strip()
            atoms.append(atom_identifier)
            charges.append(charge)

    # ADCH charge
    if charge_type == 'ADCH':
        for line in charge_lines:
            parts = line.split()
            atom_name = parts[1] + ')'
            charge = float(parts[3])
            atoms.append(atom_name)
            charges.append(charge)

    # spin population
    if charge_type == 'spin':
        for line in charge_lines:
            parts = line.split()
            atom_name = parts[1] + parts[2]
            population = float(parts[4])
            atoms.append(atom_name)
            charges.append(population)

    return Molecule(name=None, atoms=atoms, charges=charges)


def _read_fuzzy(contents, descriptor_name):
    """
    Read the fuzzy descriptor from the output file.

    Parameters
    ----------
    contents : list
        The contents of the output file.
    descriptor_name : str
        The name of the descriptor. Either 'electron_density', 'Laplacian_electron_density', or 'kinetic_energy_density'

    Returns
    -------
    Molecule
        A Molecule object containing the name, atoms, and charge.
    """
    atoms = []
    values = []

    if descriptor_name == 'electron_density':
        for line in contents:
            parts = line.split()
            atom_name = parts[0] + parts[1]
            value = float(parts[2])
            atoms.append(atom_name)
            values.append(value)

    if descriptor_name == 'Laplacian_electron_density':
        for line in contents:
            parts = line.split()
            atom_name = parts[0] + parts[1]
            value = float(parts[2])
            atoms.append(atom_name)
            values.append(value)

    if descriptor_name == 'kinetic_energy_density':
        for line in contents:
            parts = line.split()
            atom_name = parts[0] + parts[1]
            value = float(parts[2])
            atoms.append(atom_name)
            values.append(value)

    return Molecule(name=None, atoms=atoms, charges=values)


def _get_other_descriptors(contents):
    """
    Get the other descriptors from the output files.

    Parameters
    ----------
    contents : str
        The contents of the output file.

    Returns
    -------
    dict
        A dictionary containing the other descriptors.
    """
    # The Names of descriptors (initially set to None)
    descriptors = {
        'atom_num': None,
        'total_energy': None,
        'HOMO': None,
        'LUMO': None,
        'HOMO_LUMO_gap': None,
        'radius_gyration': None,
        'mass': None,
        'diameter': None,
        'MPP': None,
        'SDP': None,
        'surface_area': None,
        'volume': None,
        'sphericity': None,
        'dipole_moment': None,
        'MPI': None,
        'ESP_min': None,
        'ESP_max': None,
        'ALIE_min': None,
        'ALIE_max': None,
        'ALIE_avg': None,
        'LEAE_min': None,
        'LEAE_max': None,
        'LEA_min': None,
        'LEA_max': None,
        'LEA_avg': None,
        'Hirshfeld_charge': None,
        'ADCH_charge': None,
        'RESP_charge': None,
        'spin_population': None,
        'electron_density': None,
        'Laplacian_electron_density': None,
        'kinetic_energy_density': None,
    }

    # Read other descriptors.
    lines = contents.splitlines()

    # Read Molecular Structure and EnergyDescriptors.
    for line in lines:
        if ' Atoms:  ' in line:
            new_str = line.split(': ')[1]
            new_str = new_str.split(',')[0]
            descriptors['atom_num'] = int(new_str)
        elif ' Molecule weight:      ' in line:
            new_str = line.split(': ')[1]
            new_str = new_str.split(' Da')[0]
            descriptors['mass'] = float(new_str)
        elif ' Total energy:    ' in line:
            new_str = line.split(': ')[1]
            new_str = new_str.split('Hartree')[0]
            descriptors['total_energy'] = float(new_str)
        elif 'Orbital' in line and 'HOMO' in line:
            descriptors['HOMO'] = float(re.search(r'energy:\s+([\d.-]+)', line).group(1))
        elif 'Orbital' in line and 'LUMO' in line:
            descriptors['LUMO'] = float(re.search(r'energy:\s+([\d.-]+)', line).group(1))
        elif 'HOMO-LUMO gap:' in line:
            descriptors['HOMO_LUMO_gap'] = float(re.search(r'gap:\s+([\d.-]+)', line).group(1))
        elif ' Radius of gyration' in line:
            descriptors['radius_gyration'] = float(re.search(r':\s+([\d.]+)', line).group(1))
        elif ' Molecular planarity parameter (MPP) is' in line:
            descriptors['MPP'] = float(re.search(r'is\s+([\d.]+)', line).group(1))
        elif ' Span of deviation from plane (SDP) is' in line:
            descriptors['SDP'] = float(re.search(r'is\s+([\d.]+)', line).group(1))
        elif ' Diameter of the system' in line:
            descriptors['diameter'] = float(re.search(r'system:\s+([\d.]+)', line).group(1))
        elif ' Sphericity' in line:
            descriptors['sphericity'] = float(re.search(r':\s+([\d.]+)', line).group(1))
        elif ' Magnitude of molecular dipole moment (a.u.&Debye)' in line:
            descriptors['dipole_moment'] = float(re.search(r':\s+([\d.]+)', line).group(1))

    # Read Electrostatic Potential Descriptors.
    index = 0
    for idx, line in enumerate(lines):
        if '       ================= Summary of surface analysis =================' in line:
            index += 1
            if index == 1:
                start_idx = idx + 2
                line = lines[start_idx]
                new_str = line.split('Volume: ')[1]
                new_str = new_str.split('Bohr^3')[0]
                descriptors['volume'] = float(new_str) * (0.529177249 ** 3)  # convert to angstrom^3
                line = lines[start_idx + 2]
                new_str = line.split('Overall surface area: ')[1]
                new_str = new_str.split('Bohr^2')[0]
                descriptors['surface_area'] = float(new_str) * (0.529177249 ** 2)  # convert to angstrom^2
            elif index == 2:
                start_idx = idx + 4
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('kcal/mol   Maximal')[0]
                descriptors['ESP_min'] = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('kcal/mol')[0]
                descriptors['ESP_max'] = float(new_str)
                line = lines[start_idx + 13]
                new_str = line.split(':')[1]
                new_str = new_str.split('eV')[0]
                descriptors['MPI'] = float(new_str)
            elif index == 3:
                start_idx = idx + 4
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('eV,  ')[0]
                descriptors['ALIE_min'] = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('eV')[0]
                descriptors['ALIE_max'] = float(new_str)
                line = lines[start_idx + 4]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                descriptors['ALIE_avg'] = float(new_str)
            elif index == 4:
                start_idx = idx + 4
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('eV,  ')[0]
                descriptors['LEA_min'] = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('eV')[0]
                descriptors['LEA_max'] = float(new_str)
                line = lines[start_idx + 4]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                descriptors['LEA_avg'] = float(new_str)
            elif index == 5:
                start_idx = idx + 4
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('eV,  ')[0]
                descriptors['LEAE_min'] = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('eV')[0]
                descriptors['LEAE_max'] = float(new_str)

    # Read Atom Descriptors.
    for line in lines:
        if ' Citation of ADCH: Tian Lu, Feiwu Chen' in line:
            start_idx = lines.index(line) + 8
            end_idx = start_idx + descriptors['atom_num']
            hirshfeld_lines = lines[start_idx: end_idx]
            descriptors['Hirshfeld_charge'] = _read_charge(hirshfeld_lines, 'Hirshfeld')
        elif ' Note: The values shown after "Corrected charge" are ADCH charges' in line:
            start_idx = lines.index(line) + 6
            end_idx = start_idx + descriptors['atom_num']
            adch_lines = lines[start_idx: end_idx]
            descriptors['ADCH_charge'] = _read_charge(adch_lines, 'ADCH')
        elif ' Stage 2 of standard RESP fitting is skipped since no atom needs to be fitted' in line:
            start_idx = lines.index(line) + 3
            end_idx = start_idx + descriptors['atom_num']
            resp_lines = lines[start_idx: end_idx]
            descriptors['RESP_charge'] = _read_charge(resp_lines, 'RESP')
        elif ' Population of atoms' in line:
            start_idx = lines.index(line) + 1
            end_idx = start_idx + descriptors['atom_num']
            spin_lines = lines[start_idx: end_idx]
            descriptors['spin_population'] = _read_charge(spin_lines, 'spin')

    # Reload index
    index = 0
    for idx, line in enumerate(lines):
        if '   Atomic space        Value  ' in line:
            index += 1
            if index == 1:
                start_idx = idx + 1
                end_idx = start_idx + descriptors['atom_num']
                electron_density_lines = lines[start_idx: end_idx]
                descriptors['electron_density'] = _read_fuzzy(electron_density_lines, 'electron_density')
            elif index == 2:
                start_idx = idx + 1
                end_idx = start_idx + descriptors['atom_num']
                laplacian_electron_density_lines = lines[start_idx: end_idx]
                descriptors['Laplacian_electron_density'] = _read_fuzzy(laplacian_electron_density_lines,
                                                                        'Laplacian_electron_density')
            elif index == 3:
                start_idx = idx + 1
                end_idx = start_idx + descriptors['atom_num']
                kinetic_energy_density_lines = lines[start_idx: end_idx]
                descriptors['kinetic_energy_density'] = _read_fuzzy(kinetic_energy_density_lines,
                                                                    'kinetic_energy_density')

    return descriptors


def _get_cdft_descriptors(contents):
    """
    Get the CDFT descriptors from the output files.

    Parameters
    ----------
    contents : str
        The contents of the output file.

    Returns
    -------
    dict
        A dictionary containing the CDFT descriptors.
    """

    # Read CDFT descriptors.
    # Using regex to match the descriptors.
    def _find_descriptor(data, name):
        pattern = re.compile(r"\b" + re.escape(name) + r":\s+([-\d.]+)\s+\w+", re.MULTILINE)
        match = pattern.search(data)

        return match.group(1) if match else None

    # The Names of descriptors for searching (initially set to None)
    search_descriptors = {
        "Mulliken electronegativity": None,
        "Chemical potential": None,
        "Hardness (=fundamental gap)": None,
        "Electrophilicity index": None,
        "Nucleophilicity index": None,
    }

    # The initial descriptors for returning (initially set to None)
    cdft_descriptors = {
        "electronegativity": None,
        "chemical_potential": None,
        "chemical_hardness": None,
        "electrophilicity_index": None,
        "nucleophilicity_index": None,
    }

    # Find the values of the descriptors.
    for descriptor_name in search_descriptors:
        descriptor_value = _find_descriptor(contents, descriptor_name)
        if descriptor_value is not None:
            search_descriptors[descriptor_name] = float(descriptor_value)

    # Update the cdft_descriptors dictionary with the found values.
    cdft_descriptors['electronegativity'] = search_descriptors['Mulliken electronegativity']
    cdft_descriptors['chemical_potential'] = search_descriptors['Chemical potential']
    cdft_descriptors['chemical_hardness'] = search_descriptors['Hardness (=fundamental gap)']
    cdft_descriptors['electrophilicity_index'] = search_descriptors['Electrophilicity index']
    cdft_descriptors['nucleophilicity_index'] = search_descriptors['Nucleophilicity index']

    return cdft_descriptors


def get_descriptors(cdft_file, other_file):
    """
    Get the descriptors from the output files.

    Parameters
    ----------
    cdft_file : str
        The output file of CDFT calculations.
    other_file : str
        The output file of the calculation.

    Returns
    -------
    dict
        A dictionary containing the descriptors.
    """
    # Get contents of the output files.
    contents = read_contents(other_file)
    cdft_contents = read_contents(cdft_file)

    # Get the other descriptors.
    other_descriptors = _get_other_descriptors(contents)

    # Get the CDFT descriptors.
    cdft_descriptors = _get_cdft_descriptors(cdft_contents)

    # Combine the two dictionaries.
    descriptors = {**other_descriptors, **cdft_descriptors}

    return descriptors
