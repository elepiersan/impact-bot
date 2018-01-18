from __future__ import print_function
import time
import pickle

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
            print("Extraction failed for %s" % name)
            pass
            
    return publications
    
def impact(publications):
    """Compute the impact (total number of unique citations) from
    publications."""
    
    # Extract unique titles and corresponding number of citations
    titles = {}
    for (id, pubs) in publications.items():
        for index, title in pubs["title"].iteritems(): 
            titles[title] = pubs["cites"][index]

    # Compute total number of citations
    num_cites = sum(titles.values())
    return num_cites

def h_index(publications):

    # Extract unique titles and corresponding number of citations
    titles = {}
    for (id, pubs) in publications.items():
        for index, title in pubs["title"].iteritems(): 
            titles[title] = pubs["cites"][index]
    
    # Sort list of num of citations in descending order
    cites = titles.values()
    cites.sort(reverse=True)

    # Compute the h-index
    for (i, num_cites) in enumerate(cites):
        if (i+1) > num_cites:
            break
    h_index = i

    return h_index
    
if __name__ == "__main__":

    # Import input data
    from people import persons

    pandas2ri.activate()

    # Extract publications data
    filename = "publications.pickle"
    if False:
        publications = extract_scholar_publications(persons)
        pickle.dump(publications, open(filename, "wb"))
        exit()

    # Extract information from scholar
    publications = pickle.load(open(filename, "rb"))
    
    print("Your impact today is %d. Well done!" % impact(publications))
    print("Your h-index today is %d. Awesome!" % h_index(publications))


    
