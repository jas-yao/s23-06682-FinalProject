"""Bibtex test package"""
import click
from s23finalproject import Works


# main method
@click.command(help="OpenAlex Works Class Command Line")
@click.argument("query", nargs=1)
@click.option("--ris", default=True, help="Generates the RIS for a DOI")
@click.option("--bibtex", default=False, help="Generates the bibtex for a DOI")
def main(query, ris, bibtex):
    """main method"""
    work = Works(str(query))
    if bibtex:
        print(work.bibtex())
    if ris:
        print(work.ris())


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
