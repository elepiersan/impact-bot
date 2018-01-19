from impact_bot import *

def compute_todays_impact():

    # Import input data
    from people import persons

    # Help with R to Python (Pandas) data conversion
    pandas2ri.activate()

    # Extract information from scholar
    # Set this to False when testing, otherwise set this to True
    filename = "publications.pickle"
    if False:
        publications = extract_scholar_publications(persons)
        pickle.dump(publications, open(filename, "wb"))
    else:
        publications = pickle.load(open(filename, "rb"))

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
        print(history)
        
    # Compute impact and h-index
    num_cites = impact(publications)
    h = h_index(publications)
    
    # Find shooting star papers
    N = 5
    stars = shooting_stars(publications, N=N)

    # Add new input to history and dump to database
    history.append((num_cites, h, stars))
    pickle.dump(history, open(database, "wb"))
        
    print("Your impact today is %d. Well done!" % num_cites)
    print("Your h-index today is %d. Awesome!" % h_index(publications))

    print("%d most cited-per-year papers:" % N)
    for (title, cites) in stars:
        print("%d: %s (%s)" % (N, title, cites))
        N = N-1

if __name__ == "__main__":
    compute_todays_impact()
