"""Bibtex test package"""
from s23finalproject import Works


REF_BIBTEX = """@article{W2288114809,
 author = {John R. Kitchin},
 doi = {10.1021/acscatal.5b00538},
 journal = {ACS Catalysis},
 number = {6},
 pages = {3894-3899},
 title = {Examples of Effective Data Sharing in Scientific Publishing},
 url = {https://doi.org/10.1021/acscatal.5b00538},
 volume = {5},
 year = {2015}
}
"""


def test_bibtex():
    """Test for Bibtex method"""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert REF_BIBTEX == work.bibtex()
