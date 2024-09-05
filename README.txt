To run the function contained in “job_list.py”: 
Create a python file (or run the following python commands, after adapting them to your liking) from the same directory as the “job_list.py” file. 

Adapt the code: 
Set up your preference within the website (e.g. Mathematics & Statistics, Oxford, within 20 miles) and copy the URL that should look like this: “https://www.jobs.ac.uk/search/?placeId=ChIJrx_ErYAzcUgRAnRUy6jbIMg&locationCoords%5B%5D=51.7520209%2C-1.2577263&country%5B%5D=United+Kingdom&country%5B%5D=GB&administrativeAreaLevel2%5B%5D=Oxfordshire&administrativeAreaLevel1%5B%5D=England&locality%5B%5D=Oxford&activeFacet=academicDisciplineFacet&resetFacet=&keywords=&location=Oxford%2C+UK&distance=20&academicDisciplineFacet-expander=on&academicDisciplineFacet%5B%5D=mathematics-and-statistics”
The subjects should be written as a list of strings (i.e. ['subject1','subject2']), no capitalisation and no space, only '-' if the subject contains multiple words,
the same way it appears in the URL. 
Keywords should be input as a list of strings. In there, include all keywords that you should not be in job titles (e.g. if looking for a postdoc, add 'PhD', 'phd' and so on in the list)


Commands: 
from job_list import *
job_names(['ocean-sciences','chemistry'], 'https://www.jobs.ac.uk/search/?location=United+Kingdom&country%5B0%5D=United+Kingdom&country%5B1%5D=GB&placeId=ChIJqZHHQhE7WgIReiWIMkOg-MQ&activeFacet=academicDisciplineFacet&sortOrder=1&pageSize=25&startIndex=1&academicDisciplineFacet%5B0%5D=physical-and-environmental-sciences', ['PhD','phd','Phd','Professor','Lecturer'])


Output: 
The output files (job listings and log file) will be created in the same working directory as the “job_list.py” file. 
