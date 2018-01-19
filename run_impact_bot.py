from post_slack import post_to_slack
from impact_bot import *

def compute_todays_impact():

    # Import input data
    from people import persons

    # Help with R to Python (Pandas) data conversion
    pandas2ri.activate()

    # Load database 
    database = "history.pickle"
    # Set this to False when running, set to True when starting from
    # scratch
    if False:
        history = [] 
        pickle.dump(history, open(database, "wb"))
        exit()
    else:
        history = pickle.load(open(database, "rb"))

    # Extract information from scholar
    # Set this to False when testing, otherwise set this to True
    filename = "publications.pickle"
    if True:
        publications = extract_scholar_publications(persons)
        pickle.dump(publications, open(filename, "wb"))
    else:
        publications = pickle.load(open(filename, "rb"))

    # Compute impact and h-index
    num_cites = impact(publications)
    h = h_index(publications)
    
    # Find shooting star papers
    N = 5
    stars = shooting_stars(publications, N=N)

    # Add new input to history and dump to database
    history.append((num_cites, h, stars))
    pickle.dump(history, open(database, "wb"))

    # Create output mesage
    message = []
    message += ["Your impact today is %d. Well done!" % num_cites]
    message += ["Your h-index today is %d. Awesome!" % h]
    message += ["The shooting stars (most cited-per-year papers) are:"]
    for (title, cites) in stars:
        message += ["%d: %s (%2.1f)" % (N, title, cites)]
        N = N-1
    return "\n".join(message)

if __name__ == "__main__":
    message = compute_todays_impact()
    print(message)
    post_to_slack(message, ["scan_department",])
    print("Success!")
