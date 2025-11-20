def listings_names(url_standard, keywords):
    
    """
    This code pulls jobs from jobs.ac.uk
    Set up your preference within the website:
    1. Choose one Academic Job Discipline / Field of Expertise, Professional / Managerial / Support Services Jobs, or Studentships / PhDs
    2. Choose a location and a max distance (Optional)
    3. Choose the subjects of interest (e.g. Chemistry in Physical & Environmental Sciences)
    4. Copy the URL as input
    5. Choose the keywords that you don't want to see in job titles (e.g. "Phd", "PhD","phd", "PHD")
    """
    print('Running')

    #Necessary libraries
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import datetime
    import pandas as pd
    import openpyxl
    import os

    # Function to format text used later
    def format_func(text):
        return "".join(line.strip() for line in text.splitlines())

    # Function to turn months into numbers
    def month_func(text):
        text = text.lower()
        month_mapping = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,}
        return month_mapping[text]
        
    # Getting current work directory
    cwd = os.getcwd()

    #Today's date
    now = datetime.datetime.now()
    today = datetime.date.today()
    daytime = today.strftime("%b-%d-%Y")
    month = daytime.split('-')[0]
    day = daytime.split('-')[1]
    year = daytime.split('-')[2]
        
    # Creating empty lists to store each variable
    Jobs = []
    Links = []
    Location = []
    Dates = []
    Salary = []
    Date_placed = []

    # Loop to go through each page
    for ps in range(1,426,25):
        pos = url_standard.find('startIndex=')+11
        number = str(ps)
        url = url_standard[:pos]+number+url_standard[pos+1:]

        # Extracting the html code
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Extract job names and associated links
        jobs = [str(x.string) for x in soup.find_all('a') if "None" not in str(x.string)]
        links = [x.get('href') for x in soup.find_all('a') if '/job/' in str(x.get('href'))]
    
        # Extract location
        location = [x.string for x in soup.find_all('b')]

        # Extract deadline   
        dates = [y.text.strip() for y in soup.find_all('span', class_=['j-search-result__date--blue', 'j-search-result__date--red']) if y]     
            
        # Extract salary
        salary = [y.text.strip() for y in soup.find_all('div', class_="j-search-result__info") if y]
    
        # Extract date placed
        date_placed = [str(x).split('Date Placed: ')[1].split('</div>')[0].split('</strong>')[1] for x in soup.find_all('div')
                    if 'Date Placed: ' in str(x) and '/job/' not in str(x)]
    
    
        # Only keeping the actual jobs from the website data mining    
        start = jobs.index('Privacy Notice')+4
        end = jobs.index('×')
        jobs = jobs[start:end]
    
    
        # Removing the \n and spaces in the job titles and salary
        jobs = [format_func(jobs[i]) for i in range(0,len(jobs)) if "\n" in jobs[i]] 
        salary = [format_func(salary[i]) for i in range(0,len(salary))]    
        date_placed = [format_func(date_placed[i]) for i in range(0,len(date_placed))] 

        Links.extend(links)
        Jobs.extend(jobs)
        Location.extend(location)
        Dates.extend(dates)
        Salary.extend(salary)
        Date_placed.extend(date_placed)
        
    # Creating final lists of relevant listings
    jobs_n = []
    dates_n = []
    not_relevant = []
    links_n = []
    salary_n = []
    date_placed_n = []
    location_n = []


    # Deleting jobs with given keywords in the title:
    for i in range(0,len(jobs)):
        if any(x in jobs[i] for x in keywords):
            not_relevant.append(Jobs[i])
        else: 
            jobs_n.append(Jobs[i])
            dates_n.append(Dates[i])
            links_n.append(Links[i])
            salary_n.append(Salary[i])
            date_placed_n.append(Date_placed[i])
            location_n.append(Location[i])

    del jobs, Jobs, dates, Dates, not_relevant, salary, Salary, date_placed, Date_placed, location, Location

    dates_d = [x.split(' ')[0] for x in dates_n]
    dates_m = [x.split(' ')[1] for x in dates_n]

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    months_len = [31,28,31,30,31,30,31,31,30,31,30,31]
    time_left = []


    # Checking if the deadline is later than current date
    for i in range(0,len(dates_n)): 
        m = months.index(dates_n[i].split(' ')[1])+1
        if m > months.index(month)+1: 
            time_left.append(int(dates_d[i])+(months_len[months.index(month)]-int(day)))
        elif m == months.index(month)+1:
            if 0 <= int(dates_d[i])-int(day) <= 1:
                time_left.append(0)
            else: 
                time_left.append(int(dates_d[i])-int(day))
        else:
            time_left.append(0)



    # Delete jobs with zero day left until deadline
    indexes = [i for i in range(0,len(time_left)) if time_left[i] == 0]
    for index in sorted(indexes, reverse=True):
        del jobs_n[index], dates_n[index], links_n[index], salary_n[index], time_left[index], date_placed_n[index], location_n[index]                        
    del indexes
    time_left = [elem for elem in time_left if elem != 0] 

    # Format the salary list
    salary_n = [salary_n[i].split('Salary:')[1] for i in range(0,len(salary_n))]
    
    # Creating functioning links
    links_n = ['www.jobs.ac.uk'+links_n[i] for i in range(0,len(links_n))]
     

    # Adding year to date placed
    for i in range(0,len(date_placed_n)): 
        date_placed_n[i] = date_placed_n[i] +' '+ year if month_func(date_placed_n[i].split(' ')[1]) <= month_func(month) else date_placed_n[i] +' '+ str(int(year)-1)
    date_placed_n = pd.to_datetime(date_placed_n, format='%d %b %Y', errors='coerce').date

    # Storing previous version of output in a variable (if it exists)
    name_file = cwd + '/listings.xlsx'
    if os.path.exists(name_file):
        old_r = True
        old_results = pd.read_excel(name_file)
    else:
        old_r = False
    
    
    # Building a dataframe for each category and saving it into an excel file
    final_index = pd.DataFrame({'Name':jobs_n,'Date placed':date_placed_n,'Days left':time_left,'Deadline':dates_n, 'Salary': salary_n, 'Location': location_n, 'Link':links_n})
    final_index = final_index.sort_values('Date placed', ascending= False)
    final_index['Date placed'] = final_index['Date placed'].astype(str)
    final_index = final_index.reset_index(drop = True)
        
    # Comparison with previous output file (if it exists) to know what is new
    if old_r:
        not_in_old = final_index[~final_index['Link'].isin(old_results['Link'])].dropna()
        new_links = not_in_old['Link']; nl = len(new_links)
        indexes = []
        for link in new_links:
            index = final_index[final_index['Link'] == link].index[0]
            indexes.append(int(index))
    else:
        indexes = -1
    
    # Different formatting depending on the presence of new listings or not 
    if indexes == -1:
        print("Creating new results file")
        print(f'{len(final_index.index)} new listings \n')
        with pd.ExcelWriter(name_file, engine='xlsxwriter') as writer:
            final_index.to_excel(writer, sheet_name = 'Sheet1',index = False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            cell_format = workbook.add_format(); cell_format.set_bold(); cell_format.set_text_wrap()
            cell_format.set_align('vcenter'); cell_format.set_font_size(11) ; cell_format.set_align('center')
            
            cell_format2 = workbook.add_format(); cell_format2.set_text_wrap(); cell_format2.set_align('vcenter')
            cell_format2.set_font_size(11); cell_format2.set_align('center')

            worksheet.set_column(0, 0, 55, cell_format)
            widths = [12, 10, 9, 10, 50, 21, 70]         
            for x in range(1, len(widths)):
                worksheet.set_column(x, x, widths[x], cell_format2)

    elif len(indexes) == 0:
        print("Nothing new")
        with pd.ExcelWriter(name_file, engine='xlsxwriter') as writer:
            final_index.to_excel(writer, sheet_name = 'Sheet1',index = False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            cell_format = workbook.add_format(); cell_format.set_bold(); cell_format.set_text_wrap()
            cell_format.set_align('vcenter'); cell_format.set_font_size(11) ; cell_format.set_align('center')
            
            cell_format2 = workbook.add_format(); cell_format2.set_text_wrap(); cell_format2.set_align('vcenter')
            cell_format2.set_font_size(11); cell_format2.set_align('center')

            worksheet.set_column(0, 0, 55, cell_format)
            widths = [12, 10, 9, 10, 50, 21, 70]         
            for x in range(1, len(widths)):
                worksheet.set_column(x, x, widths[x], cell_format2)

    else: 
        if nl > 1:
            print(f'{nl} new listings. \n')
        elif nl == 1: 
            print(f'{nl} new listing. \n')   
        with pd.ExcelWriter(name_file, engine='xlsxwriter', date_format='d/m/yyyy') as writer:
            final_index.to_excel(writer, sheet_name = 'Sheet1', index = False)
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            cell_format = workbook.add_format(); cell_format.set_bold(); cell_format.set_text_wrap()
            cell_format.set_align('vcenter'); cell_format.set_font_size(11); cell_format.set_align('center') 
                    
            cell_format2 = workbook.add_format(); cell_format2.set_text_wrap(); cell_format2.set_align('vcenter')
            cell_format2.set_font_size(11); cell_format2.set_align('center')

            worksheet.set_column(0, 0, 55, cell_format)
            widths = [12, 12, 9, 10, 50, 21, 70]         
            for x in range(1, len(widths)):
                worksheet.set_column(x, x, widths[x], cell_format2)

        # Writing the new listings in red
        workbook = openpyxl.load_workbook(name_file)
        sheet = workbook.active
        cell_format3 = openpyxl.styles.Font(color = "EE4B2B", bold=True)
        cell_format4 = openpyxl.styles.Font(color = "EE4B2B")
        for index in indexes:
            row = sheet[index + 2]  
            for cell in row:
                if cell.column_letter == 'A':
                    cell.font = cell_format3
                else:
                    cell.font = cell_format4
        workbook.save(name_file)  

    # Output the run results in a log file (data, time and new listings)
    f = open(cwd + '/log.txt', 'a')
    if "nl" in locals():
        if nl > 1: 
            f.write(f'Code ran on {daytime} at {str(now.time()).split(".")[0]}, {nl} new listings. \n')
        else:
            f.write(f'Code ran on {daytime} at {str(now.time()).split(".")[0]}, {nl} new listing. \n')
    else:
        f.write(f'Code ran on {daytime} at {str(now.time()).split(".")[0]}. \n')
    f.close()
    print('Finished')
