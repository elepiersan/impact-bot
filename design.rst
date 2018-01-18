*********
ImpactBot
*********

The aim of the ImpactBot is:

  for a list of people (for instance an academic department), compute
  the total number of citations for the corresponding publications.


Algorithm steps:

1. For a list of people (for instance an academic department),
   identify their Google Scholar person pages. 

2. Extract all publications for a Google Scholar person page,
   including title, authors, citation number, year, (duplicates) into
   suitable data structure.

3. Compute a suitable sum of the citations for all publications.
