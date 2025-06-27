# CSV XLOOKUP Tool

A Python GUI application that performs an Excel-like XLOOKUP operation between two CSV files, adding a column from one file to another based on a common key.

![CSV XLOOKUP Tool Screenshot](screenshot.png) *[Note: Add a screenshot later]*

## Features

- Load two CSV files for comparison
- Select columns for lookup and value matching
- Add a new column to the first file with values from the second file
- Save the modified file with the new column
- Simple and intuitive graphical interface

## Requirements

- Python 3.6+
- pandas
- PyQt5

## Installation

1. Clone this repository or download the script
2. Install required packages:
pip install pandas PyQt5


## Usage

1. Run the application:

python xlookup_app.py

2. Select your files:
- "File A": The file you want to add a column to
- "File B": The file containing the values you want to add
3. Specify:
- Name for the new column
- Lookup column in File A (common key)
- Lookup column in File B (matching key)
- Value column in File B (values to add)
4. Click "Run XLOOKUP"
5. Save the modified file

## How It Works

The application performs the equivalent of Excel's XLOOKUP by:
1. Creating a mapping between the lookup column and value column in File B
2. Adding a new column to File A with values matched from File B
3. Preserving all original data from File A

## Limitations

- Only works with CSV files
- First match is used if there are duplicate keys in File B


