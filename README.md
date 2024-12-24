# TSR AminoAcid Package

**TSR AminoAcid Package** is a Python tool for retrieving Protein Data Bank (PDB) files and generating key/triplet files for Amino Acid analysis.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Retrieve PDB Files](#retrieve-pdb-files)
  - [Generate Keys and Triplets](#generate-keys-and-triplets)
  - [Using with CSV Input](#using-with-csv-input)
- [Arguments](#arguments)
- [Examples](#examples)

## Installation

### Cloning the Repository

To get started with the `aminoacid_tsr_package`, clone the repository from GitHub:

```bash
git clone https://github.com/KrishnaRauniyar/TSR_AMINOACID_PACKAGE.git
cd TSR_AMINOACID_PACKAGE/aminoacid_tsr_package
```

### Installing the Package
1. It's recommended to create a virtual environment:

```bash
python3 -m venv tsrenv
source tsrenv/bin/activate  # Mac/Linux
tsrenv\Scripts\activate  # Windows
```

2. Install the package using pip:

```bash
pip install .
```

3. Alternatively, you can install the package from the built wheel:

```bash
python setup.py sdist bdist_wheel
pip install dist/aminoacid_tsr_package-0.1.0-py3-none-any.whl
```

4. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Once installed, you can use the following steps to retrieve PDB files and generate key/triplet files.
### Retrieve PDB Files

```python
from aminoacid_tsr_package.PDB_DL import PDB_DL

# Retrieve PDB files for the specified PDB IDs
pdb_ids = ["1GTA", "1GTB", "1lbe"]
PDB_DL(pdb_ids, 'Dataset')
```
Or you can use a CSV file to download the PDB files:
```python
from aminoacid_tsr_package.PDB_DL import PDB_DL

data_dir = "Dataset"
csv_file = "sample_details.csv"
PDB_DL(csv_file, data_dir)
```

This will download the PDB files into the specified `Dataset` directory. If the directory is not specified, the default directory for storing the PDB files would also be `Dataset`.
Protein IDs are not case-sensitive, so you may use lowercase and uppercase letters to address the proteins.

### Generate Keys and Triplets
To generate keys or triplet files for the proteins:

```python
from aminoacid_tsr_package.generate_keys_and_triplets import AminoAcidProteinTSR

# Define the directory where PDB files are stored
data_dir = "Dataset"
# Define the list of PDB files and corresponding chains
input_files = ["1GTA", "1GTB", "1LBE"]
chain = ["A", "A", "A"]  # specify chains for each PDB file
output_option = "keys"  # choose 'keys', 'triplets', or 'both'. If none, the function will generate both.
# mirror_image is an optional argument. Set to True if you want the TSR to address for the mirror image triangles.

# Process protein data to generate key files
AminoAcidProteinTSR(data_dir, input_files, chain=chain, output_option=output_option mirror_image=True)
```
Protein's chains are case-sensitive since there are chains with both lower and uppercase letters.

### Using a CSV file as Input
You can pass a CSV file as input to process multiple PDB files with chain information. The CSV file should have the following format:

|protein         |chain        |
|----------------|-------------|
|1GTA            |A            |
|1GTB            |A            |
|1LBE            |A            |

To process the CSV file:

```python
from aminoacid_tsr_package.generate_keys_and_triplets import AminoAcidProteinTSR

# Define the directory and CSV file path
data_dir = "Dataset"
csv_file = "sample_details.csv"
# mirror_image is an optional argument. Set to True if you want the TSR to address for the mirror image triangles.

# Process the CSV input
AminoAcidProteinTSR(data_dir, csv_file, output_option="keys", mirror_image=True)
```

## Arguments
- `data_dir`: Directory where the PDB files are located or where they will be downloaded.
- `input_files`: A list of PDB IDs or the path to a CSV file containing protein IDs and chains.
- `chain`: A list of chains corresponding to each PDB file (optional if using a CSV file).
- `output_option`: Either "keys" to generate key files or "triplets" to generate triplet files.
- `mirror_image` : Optional argument. Set to True if you want the TSR to address for the mirror image triangles.

## Examples
### Example 1: Retrieving PDB Files and Generating Keys

```python
from aminoacid_tsr_package.PDB_DL import PDB_DL
from aminoacid_tsr_package.generate_keys_and_triplets import AminoAcidProteinTSR

# Step 1: Retrieve PDB files
data_dir = "Dataset" # It is also the default directory if not declared
pdb_ids = ["1GTA", "1gtb", "1lbe"] # Not case-sensitive
chain = ["A", "A", "A"] # Case-sensitive
PDB_DL(pdb_ids, data_dir)

# Step 2: Generate key files for the proteins
AminoAcidProteinTSR(data_dir, pdb_ids, chain=chain, output_option="keys", mirror_image=True) # Modify the output option as desired
```
### Example 2: Using CSV File for Input

```python
from aminoacid_tsr_package.PDB_DL import PDB_DL
from aminoacid_tsr_package.generate_keys_and_triplets import AminoAcidProteinTSR

# Use CSV input for batch processing
data_dir = "Dataset"
csv_file = "sample_details.csv"
PDB_DL(csv_file, data_dir)
AminoAcidProteinTSR(data_dir, csv_file, output_option="triplets", mirror_image=True)
```
