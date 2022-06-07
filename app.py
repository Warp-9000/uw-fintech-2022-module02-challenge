# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


# Global variables
default_bank_loan_data = "./data/daily_rate_sheet.csv"
default_output_data = "./my_bank_loans.csv"


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    # Ask the user to enter loan data
    csv_file_path = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    
    # If the file path is blank set the path to the default, otherwise crea a path object with what they provided.
    if csv_file_path == "":
        csv_file_path = Path(default_bank_loan_data)
    else:
        csv_file_path = Path(csv_file_path)

    # Check if the file path exists, if not exit the application
    if not csv_file_path.exists():
        print("Oops! Can't find this path: {csv_file_path}")
        exit_application()

    return load_csv(csv_file_path)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

def exit_application():
    sys.exit("Thank you for using the Loan Qualifier Application.")


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    print(f"\n---------- DEBUG ----------")
    print(f"qualifying_loans: {qualifying_loans}")
    print(f"number of loans: {len(qualifying_loans)}")
    print("---------- DEBUG ----------\n")

    # ----- Acceptance Criteria -----
    # Given that I’m using the loan qualifier CLI, when I run the qualifier, then the tool should prompt the user to save the results as a CSV file.
    # -------------------------------
    # Prompt the user to save their loans
    save_loan_input = questionary.confirm("Do you want to save your qualifying loans results?").ask()

    print(f"\n---------- DEBUG ----------")
    print(f"save_loan_input: {save_loan_input}")
    print("---------- DEBUG ----------\n")

    # ----- Acceptance Criteria -----
    # Given that I have a list of qualifying loans, when I’m prompted to save the results, then I should be able to opt out of saving the file.
    # -------------------------------
    
    # If the user does not want to save, then exit
    if not save_loan_input:
        exit_application()
    
    # ----- Acceptance Criteria -----
    # Given that no qualifying loans exist, when prompting a user to save a file, then the program should notify the user and exit.
    # -------------------------------

    # If there are no qualifying loans, then notify the user and exit
    if not (len(qualifying_loans) > 1):
        print("There are no qualifying loans to save.")
        exit_application()
    
    # If we get here we know the user wants to save, and there are qualifying loans

    # ----- Acceptance Criteria -----
    # Given that I have a list of qualifying loans, when I choose to save the loans, the tool should prompt for a file path to save the file.
    # -------------------------------

    # Prompt the user to provide a file path
    csv_file_path = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()

    # If the file path is blank set the path to the default, otherwise crea a path object with what they provided.
    if csv_file_path == "":
        csv_file_path = Path(default_output_data)
    else:
        csv_file_path = Path(csv_file_path)

    # ----- Acceptance Criteria -----
    # Given that I’m using the loan qualifier CLI, when I choose to save the loans, then the tool should save the results as a CSV file.
    # -------------------------------
    
    # Save the filtered loan data to the file path specified
    save_csv(csv_file_path, qualifying_loans)


def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)

    # Exit the application
    exit_application()

if __name__ == "__main__":
    fire.Fire(run)
