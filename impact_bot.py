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

        # Get basic profile info
        pubs = scholar.get_publications(id)

        # Convert to pandas dataframe
        try:
            df = pandas2ri.ri2py_dataframe(pubs)
            publications[id] = df
        except:
            pass
            
    return publications

def extract_scholar_profile_info(persons):

    # Import the scholar package
    scholar = importr("scholar")

    # Extract scholar information for each person
    infos = {}
    for (name, id) in persons.items():

        # Get basic profile info
        info = scholar.get_profile(id)

        # Convert info to standard Python format
        info = dict(zip(info.names, list(info)))
        infos[id] = info

    return infos
    
def compute_impact(infos):

    # Compute total number of citatons (ignoring duplicates)
    impact = 0
    for (id, info) in infos.items():

        # Extract number of total citations for given person
        print("Measuring impact of %s" % info["name"][0])
        try:
            num_cites = int(info["total_cites"][0])
        except:
            num_cites = 0
            
        # Compute simple impact measure (total sum of citations)
        impact += num_cites
        
    return impact

def h_index(persons):

    # Extract information from scholar
    publications = extract_scholar_publications(persons)
    #pickle.dump(publications, open("publications.pickle", "wb"))
    #exit()
    #publications = pickle.load(open("publications.pickle", "rb"))

    titles = {}

    # Extract unique titles and corresponding number of citations
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
    
def impact(persons):

    # Extract basic profile from scholar
    infos = extract_scholar_profile_info(persons)
    
    # Compute impact
    total_impact = compute_impact(infos)
    return total_impact
    
if __name__ == "__main__":

    # Import input data
    from people import persons

    pandas2ri.activate()
    
    print("Your impact today is %d. Well done!" % impact(persons))
    print("Your h-index today is %d. Well done!" % h_index(persons))


    
