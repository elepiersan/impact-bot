from __future__ import print_function

# Import common modules
import pickle
import datetime
import math

# Import rpy2 for working with r package scholar
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

# Import pandas for easier working with r data tables in Python
import pandas
from rpy2.robjects import r, pandas2ri

# Note the following output format from get_publications:
# info[0]: Publication titles
# info[1]: Publication authors
# info[2]: Journal titles
# info[3]: Page numbers
# info[4]: Citations
# info[5]: Year
# info[6]: ? 
# info[7]: ?

def extract_scholar_publications(persons):
    "Extract and return publication and citation information."

    # Import the scholar package
    scholar = importr("scholar")

    # Extract scholar publication information for each person, store
    # as standard Python dictionary
    publications = {}
    for (name, id) in persons.items():
        print("Extracting publication information for %s" % name)
        
        # Get basic profile info
        pubs = scholar.get_publications(id)

        # Convert to pandas dataframe
        try:
            df = pandas2ri.ri2py_dataframe(pubs)
            publications[id] = df
            print("Success")
        except:
            print("Extraction failed for %s. Ignoring data." % name)
            pass
            
    return publications
    
def unique_titles_vs_citations(publications):
    "Extract unique titles and corresponding number of citations."
    titles = {}
    for (id, pubs) in publications.items():
        for index, title in pubs["title"].iteritems(): 
            titles[title] = pubs["cites"][index]
    return titles

def impact(publications):
    """Compute the impact (total number of unique citations) from
    publications."""
    
    # Extract unique titles with corresponding number of citations
    titles = unique_titles_vs_citations(publications)

    # Compute total number of citations
    num_cites = sum(titles.values())
    return num_cites

def h_index(publications):
    "Compute the h_index of the combined lists of publications."

    # Extract unique titles with corresponding number of citations
    titles = unique_titles_vs_citations(publications)

    # Sort list of num of citations in descending order
    cites = titles.values()
    cites.sort(reverse=True)

    # Compute the h-index
    for (i, num_cites) in enumerate(cites):
        if (i+1) > num_cites:
            break
    h_index = i

    return h_index

def shooting_stars(publications, N=5):
    "Compute the N papers with most citations per year."

    # Find the current year
    year = datetime.date.today().year

    # Iterate through all papers and compute number of citations per year
    titles = {}
    for (id, pubs) in publications.items():
        for index, title in pubs["title"].iteritems(): 
            years = (year - pubs["year"][index]) + 1
            if math.isnan(years):
                #print("Year does not make sense for %s, ignoring." % title)
                continue
            titles[title] = pubs["cites"][index]/years

    # Print top N paper (cited most per year):
    stars = sorted(titles.iteritems(), key=lambda (k,v): (v,k))[-N:]
    return stars
