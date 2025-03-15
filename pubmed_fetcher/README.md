PubMed Fetcher

Overview

PubMed Fetcher is a command-line tool that allows users to search for PubMed research papers based on a query and extract relevant details such as article title, publication date, authors, affiliations, and emails (if available). The results can be displayed in the console or saved as a CSV file.

Project Structure

The project is structured as follows:

├── pubmed_fetcher/
│   ├── __init__.py
│   ├── pubmed_fetcher.py  # Core logic to fetch PubMed data
│   ├── pubmed_cli.py      # CLI implementation using Click
├── pyproject.toml         # Poetry configuration file
├── README.md              # Project documentation
├── poetry.lock
Installation

This project uses Poetry for dependency management. To install the necessary dependencies, follow these steps:

Clone the repository:

git clone https://github.com/daranish/Pubmed-Test.git
cd pubmed-fetcher

Install dependencies using Poetry:

poetry install

Usage

You can run the tool using the command-line interface.

Fetch PubMed Papers

To search for PubMed papers, run the following command:

poetry run get-papers-list "cancer drug discovery"

This will display the results in the console.

Save Results to CSV

To save the results as a CSV file, use the -f option:

poetry run get-papers-list "cancer drug discovery" -f papers.csv

Debug Mode

To enable debug output, use the -d option:

poetry run get-papers-list "cancer drug discovery" -d

Tools and Libraries Used

Python 3.10+: The project is built using Python.

Poetry: Dependency management and package building.

Requests: Used for making API calls to the PubMed API.

Click: A Python package for building command-line interfaces.

PubMed API: Used to fetch research articles from PubMed. PubMed API Docs
