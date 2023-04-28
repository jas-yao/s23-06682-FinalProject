"""Works class"""
import time
import base64
import requests

import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure

import bibtexparser

# from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class Works:
    """Open Alex Works Class"""

    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(  # pylint: disable=missing-timeout
            f"https://api.openalex.org/works/{oaid}"
        )
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            if len(_authors) == 0:
                authors = "None"
            else:
                authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        # journal = self.data["host_venue"]["display_name"]
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        opal = self.data["id"]
        strs = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), \
        {self.data["doi"]}. cited by: {citedby}. {opal}'
        return strs

    def _repr_markdown_(self):  # pylint: disable=too-many-locals
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]\
        ({self.data['host_venue']['id']})"
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        opal = self.data["id"]

        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]

        fig, axes = plt.subplots()
        axes.bar(years, counts)
        axes.set_xlabel("year")
        axes.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        strs = f'{authors}, *{title}*, **{journal}**, {volume}{issue}{pages}, \
        ({year}), {self.data["doi"]}. cited by: {citedby}. [Open Alex]({opal})'

        strs += "<br>" + citefig
        return strs

    @property
    def _ris(self):
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception(  # pylint: disable=broad-exception-raised
                "Unsupported type {self.data['type']}"
            )

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        # ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        # uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" \
        # download="ris">Download RIS</a>'
        return ris

    def ris(self):
        """gets the ris"""
        return self._ris

    def related_works(self):
        """gets related works"""
        rworks = []
        for rw_url in self.data["related_works"]:
            rws = Works(rw_url)
            rworks += [rws]
            time.sleep(0.101)
        return rworks

    def citing_works(self):
        """
        Makes a request with the cited_by_api_url.
        Goes through each result of the request and puts the work into a Works
        object
        returns a list of related works

        Does not account for cited_by greater than 200
        """
        citedby = []
        res = requests.get(  # pylint: disable=missing-timeout
            self.data["cited_by_api_url"] + "&per-page=200"
        ).json()
        for i in res["results"]:
            cbs = Works(i["id"])
            citedby += [cbs]
            time.sleep(0.5)
        return citedby

    def references(self):
        """
        Exactly the same as related works, insteading accessing references
        returns a list of references
        """
        references = []
        for ref_url in self.data["referenced_works"]:
            ref = Works(ref_url)
            references += [ref]
            time.sleep(0.5)
        return references

    def bibtex(self):
        """
        Extracts relevant data from the works object and exports it as a bibtex
        Generates a file and does not return anything.
        Returns None
        """

        # the authors string generation was taken from above...
        # could improve by make this a class attribute
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            if len(_authors) == 0:
                authors = "None"
            else:
                authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]
        title = self.data["title"]
        journal = self.data["primary_location"]["source"]["display_name"]
        volume = self.data["biblio"]["volume"]
        number = self.data["biblio"]["issue"]
        pages = (
            self.data["biblio"]["first_page"] + "-" + self.data["biblio"]["last_page"]
        )
        year = str(
            self.data["publication_year"]
        )  # this needs to be converted to string
        doi = self.data["doi"].replace("https://doi.org/", "")
        url = self.data["doi"]
        ids = self.data["id"].replace("https://openalex.org/", "")

        # this section on generating a bibtex file is largely based off of the
        # tutorial example
        # https://bibtexparser.readthedocs.io/en/master/tutorial.html
        # with relevant modifications to make the entry similar to what was
        # shown in class.
        # ID generation was defaulted to the Open Alex ID
        dbs = BibDatabase()
        dbs.entries = [
            {
                "author": authors,
                "title": title,
                "journal": journal,
                "volume": volume,
                "number": number,
                "pages": pages,
                "year": year,
                "doi": doi,
                "url": url,
                "ID": ids,
                "ENTRYTYPE": "article",
            }
        ]

        #         writer = BibTexWriter()
        #         with open("bibtex.bib", "w") as bibfile:
        #             bibfile.write(writer.write(dbs))

        bibtex_str = bibtexparser.dumps(dbs)

        return bibtex_str
