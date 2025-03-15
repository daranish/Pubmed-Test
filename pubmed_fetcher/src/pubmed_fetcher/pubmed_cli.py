import click
from pubmed_fetcher.pubmed_fetcher import fetch_and_save_pubmed_data

@click.command()
@click.argument("query")
@click.option("-f", "--filename", type=str, help="Specify filename to save results as CSV.")
@click.option("-d", "--debug", is_flag=True, help="Print debug information.")
@click.option("-h", "--help", is_flag=True, help="Display usage instructions.")
def main(query, filename, debug, help):
    """CLI to fetch PubMed research papers based on query."""
    
    if help:
        click.echo("Usage: poetry run get-papers-list QUERY [-f filename.csv] [-d]")
        return

    fetch_and_save_pubmed_data(query, filename, debug)

if __name__ == "__main__":
    main()
