import json
import requests
from typing import Union
import csv


# Wroking with CSV data and files
def read_csv_column(filename, column_index):
    column_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > column_index:
                column_data.append(row[column_index])
    return column_data


# Add your list here, either just a filename for root or full path
filename = 'example.csv'
column_index = 0

email_list = read_csv_column(filename, column_index)


# Should be treated like an environment variable and secret.
API_KEY = ""


class Validate(object):
    """
    Class for interacting with the IPQualityScore API.

    Attributes:
        key (str): Your IPQS API key.
        format (str): The format of the response. Default is 'json', but you can also use 'xml'.
        base_url (str): The base URL for the IPQS API.

    Methods:
        email_validation_api(email: str, timeout: int = 1, fast: str = 'false', abuse_strictness: int = 0) -> str:
            Returns the response from the IPQS Email Validation API.
    """

    key = None
    format = None
    base_url = None

    def __init__(self, key, format="json") -> None:
        self.key = key
        self.format = format
        self.base_url = f"https://www.ipqualityscore.com/api/{self.format}/"

    def email_validation_api(self, email: str, timeout: int = 7, fast: str = 'false', abuse_strictness: int = 0) -> str:
        """
        Returns the response from the IPQS Email Validation API.

        Args:
            email (str):
                The email you wish to validate.
            timeout (int):
                Set the maximum number of seconds to wait for a reply from an email service provider.
                If speed is not a concern or you want higher accuracy we recommend setting this in the 20 - 40 second range in some cases.
                Any results which experience a connection timeout will return the "timed_out" variable as true. Default value is 7 seconds.
            fast (str):
                If speed is your major concern set this to true, but results will be less accurate.
            abuse_strictness (int):
                Adjusts abusive email patterns and detection rates higher levels may cause false-positives (0 - 2).

        Returns:
            str: The response from the IPQS Email Validation API.
        """

        url = f"{self.base_url}email/{self.key}/{email}"

        params = {
            "timeout": timeout,
            "fast": fast,
            "abuse_strictness": abuse_strictness
        }

        response = requests.get(url, params=params)
        return response.text


if __name__ == "__main__":
    filename = "output.csv"

    headers = [
        "message", "success", "disposable", "smtp_score", "overall_score", "generic",
        "dns_valid", "honeypot", "deliverability", "frequent_complainer", "spam_trap_score",
        "catch_all", "timed_out", "suspect", "recent_abuse", "fraud_score", "sanitized_email", "original_email"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    for email in email_list[0:3]:
        v = Validate(API_KEY)
        response_json = v.email_validation_api(email)

        data = json.loads(response_json)

        # Extract values
        values = [
            data.get("message"),
            data.get("success"),
            data.get("disposable"),
            data.get("smtp_score"),
            data.get("overall_score"),
            data.get("generic"),
            data.get("dns_valid"),
            data.get("honeypot"),
            data.get("deliverability"),
            data.get("frequent_complainer"),
            data.get("spam_trap_score"),
            data.get("catch_all"),
            data.get("timed_out"),
            data.get("suspect"),
            data.get("recent_abuse"),
            data.get("fraud_score"),
            data.get("sanitized_email"),
            email
        ]

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(values)


print(f"Data saved to {filename}.")
