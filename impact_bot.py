from __future__ import print_function
import time

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

        # Get basic profile info (and convert to Python data
        # structure)
        info = scholar.get_profile(google_id)
        info = dict(zip(info.names, list(info)))

        # Extract number of total citations for given person
        print("Measuring impact of %s" % info["name"][0])
        try:
            num_cites = int(info["total_cites"][0])
        except:
            num_cites = 0
            
        # Compute simple impact measure (total sum of citations)
        impact += num_cites
        
    return impact
        
if __name__ == "__main__":

    # Import input data
    from people import persons

    # Compute impact
    total_impact = compute_impact(persons)
    
    print("Your impact today is %d. Well done!" % total_impact)

    

    
