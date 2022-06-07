# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csv_path_name):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csv_path_name, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data


def save_csv(csv_path_name, loan_data):
    """Writes the CSV file to the path provided.

    Args:
        csv_path_name (Path): The csv file path.
        loan_data (list): The loan data to save.

    Returns:
        Nothing

    """

    header = "Lender,Max Loan Amount,Max LTV,Max DTI,Min Credit Score,Interest Rate"

    with open(csv_path_name, 'w', newline='') as csv_file:

        # creating a DictWriter because inexpensive_loans is a dictionary
        writer = csv.writer(csv_file)

        # writing the header, if specified
        if header != None:
            print(f"Writing the header {header}")
            writer.writerow(header)

        # writing each loan to the file
        print("Writing each loan")
        # iterating through the inexpensive loan list
        for loan in loan_data:
            print(f"Writing this line: {loan}")
            # since our writer is a DictWriter it handles things for us
            writer.writerow(loan)

    return None
