from __future__ import print_function

# Import rpy2 for working with r package scholar
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

# Import pandas for easier working with r data tables in Python
#from rpy2.robjects import r, pandas2ri

def compute_impact(persons):
    
    # Import the scholar package
    scholar = importr("scholar")

    impact = 0  
    for (name, google_id) in persons.items():
        info = scholar.get_profile(google_id)

        # Convert to dictionary for easy handling (Bottleneck?)
        info = dict(zip(info.names, list(info)))

        # Extract number of total citations for given person
        num_cites = int(info["total_cites"][0])

        # Compute simple impact measure (total sum of citations)
        impact += num_cites

    return impact

        
if __name__ == "__main__":

    # Import input data
    from people import persons

    # Compute impact
    total_impact = compute_impact(persons)
    
    
    print("Your impact today is %d " % total_impact)

    
    #pubs = scholar.get_publications(google_id)

    
