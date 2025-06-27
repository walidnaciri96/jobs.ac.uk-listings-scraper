This code pulls listings from jobs.ac.uk.
First, you must create the URL used in the function. To do so: 
    1. Go to https://www.jobs.ac.uk
    2. Choose one Academic Job Discipline / Field of Expertise, Professional / Managerial / Support Services Jobs, or Studentships / PhDs
    3. Choose a location and a max distance (optional)
    4. Choose the subjects of interest (e.g. Chemistry in Physical & Environmental Sciences)
    5. Copy the URL as input
    6. Choose the keywords that you don't want to see in job titles (e.g. "Phd", "PhD","phd", "PHD")

To run the function: 
Download the file, create a Python file in the same directory, and run the following: 
	from listings import listings_names
	listings_names(url_standard, keywords)

Where url_standard is the URL created beforehand and keywords 
	   keywords contains the list of keywords structured as the following: ["Phd", "PhD","phd", "PHD”]


Outputs: 
This function creates two output files, in the same directory as the function, a log.txt file where the time and date, as well as the numbers of new listings, will be logged, and a listings.xlsx file where the listings are sorted by publication date.
