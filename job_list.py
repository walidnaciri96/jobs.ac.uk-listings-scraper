def job_names(subjects, url_standard, keywords):
    
    """
    This code looks at jobs from jobs.ac.uk
    Set up your preference within the website (e.g. Mathematics & Statistics, Oxford, within 20 miles) and copy the URL that should look like this:
    "https://www.jobs.ac.uk/search/?placeId=ChIJrx_ErYAzcUgRAnRUy6jbIMg&locationCoords%5B%5D=51.7520209%2C-1.2577263&country%5B%5D=United+Kingdom&country%5B%5D=GB&administrativeAreaLevel2%5B%5D=Oxfordshire&administrativeAreaLevel1%5B%5D=England&locality%5B%5D=Oxford&activeFacet=academicDisciplineFacet&resetFacet=&keywords=&location=Oxford%2C+UK&distance=20&academicDisciplineFacet-expander=on&academicDisciplineFacet%5B%5D=mathematics-and-statistics"
    The subjects should be written as a list of strings (i.e. ['subject1','subject2']), no capitalisation and no space, only '-' if the subject contains multiple words,
    the same way it appears in the URL. 
    Keywords should be input as a list of strings. In there, include all keywords that you should not be in job titles 
    (e.g. if looking for a postdoc, add 'PhD', 'phd' and so on in the list)
    """
    print('Running')

    #Necessary libraries
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import datetime
    import pandas as pd
    import os
    
    def format_func(text):
        return "".join(line.strip() for line in text.splitlines())

    
    cwd = os.path.dirname(os.path.realpath(__file__))
    
    #Making sure the link is correct and making sure all results are displayed in one page
    if '&subDisciplineFacet%5B0%5D=' not in url_standard: url_standard  = url_standard + '&subDisciplineFacet%5B0%5D='
    if 'pageSize' in url_standard: 
        if int(url_standard.split('pageSize=')[1].split('&startIndex=')[0]) < 500:
            url_standard = url_standard.replace('pageSize='+url_standard.split('pageSize=')[1].split('&startIndex=')[0],'pageSize=500')
    
    frames = []

    for p in subjects:
        url = url_standard+p
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')


        jobs = []
        dates = []
        links = []
        salary = []

        #Today's date
        now = datetime.datetime.now()
        today = datetime.date.today()
        daytime = today.strftime("%b-%d-%Y")
        month = daytime.split('-')[0]
        day = daytime.split('-')[1]
        year = daytime.split('-')[2]

        #Extract job names and associated links
        jobs = [str(x.string) for x in soup.find_all('a') if "None" not in str(x.string)]
        links = [x.get('href') for x in soup.find_all('a') if '/job/' in str(x.get('href'))]

        #Extract location
        location = [x.string for x in soup.find_all('b')]

         #Extract deadline   
        dates = [y.text.strip() for y in soup.find_all('span', class_=['j-search-result__date--blue', 'j-search-result__date--red']) if y]     
        
        #Extract salary
        salary = [y.text.strip() for y in soup.find_all('div', class_="j-search-result__info") if y]

        #Extract date placed
        date_placed = [str(x).split('Date Placed: ')[1].split('</div>')[0].split('</strong>')[1] for x in soup.find_all('div')
                    if 'Date Placed: ' in str(x) and '/job/' not in str(x)]


        #Only keeping the actual jobs from the website data mining    
        start = jobs.index('Privacy Notice')+4
        end = jobs.index('×')
        jobs = jobs[start:end]


        #Removing the \n and spaces in the job titles and salary
        jobs = [format_func(jobs[i]) for i in range(0,len(jobs)) if "\n" in jobs[i]] 
        salary = [format_func(salary[i]) for i in range(0,len(salary))]    
        date_placed = [format_func(date_placed[i]) for i in range(0,len(date_placed))]  
        

        jobs_n = []
        dates_n = []
        not_relevant = []
        links_n = []
        salary_n = []
        date_placed_n = []
        location_n = []


        #Deleting jobs with given keywords in the title:

        for i in range(0,len(jobs)):
            if any(x in jobs[i] for x in keywords):
                not_relevant.append(jobs[i])
            else: 
                jobs_n.append(jobs[i])
                dates_n.append(dates[i])
                links_n.append(links[i])
                salary_n.append(salary[i])
                date_placed_n.append(date_placed[i])
                location_n.append(location[i])

        del jobs, dates, not_relevant, salary, date_placed, location

        dates_m = []
        dates_d = []

        dates_d = [x.split(' ')[0] for x in dates_n]
        dates_m = [x.split(' ')[1] for x in dates_n]

        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        months_len = [31,28,31,30,31,30,31,31,30,31,30,31]
        time_left = []


        #Checking if the deadline is later than current date
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



        #Delete jobs with zero day left until deadline
        indexes = [i for i in range(0,len(time_left)) if time_left[i] == 0]

        for index in sorted(indexes, reverse=True):
            del jobs_n[index], dates_n[index], links_n[index], salary_n[index], time_left[index], date_placed_n[index], location_n[index]
                                
        del indexes
        time_left = [elem for elem in time_left if elem != 0] 

         #Format the salary list
        salary_n = [salary_n[i].split('Salary:')[1] for i in range(0,len(salary_n))]
    
        #Creating functioning links
        links_n = ['www.jobs.ac.uk'+links_n[i] for i in range(0,len(links_n))]
     

        #Adding year to date placed
        date_placed_n = [date_placed_n[i] +' '+ year for i in range(0,len(date_placed_n))]
        date_placed_n = pd.to_datetime(date_placed_n, format='%d %b %Y', errors='coerce').date
    
        #Building a dataframe for each category and saving it into an excel file
        final_index = pd.DataFrame({'Name':jobs_n,'Date placed':date_placed_n,'Days left':time_left,'Deadline':dates_n, 'Salary': salary_n, 'Location': location_n, 'Link':links_n})
        final_index = final_index.sort_values('Date placed', ascending= False)
        final_index['Date placed'] = final_index['Date placed'].astype(str)
        
        with pd.ExcelWriter(cwd + '/%s.xlsx' %(p), engine='xlsxwriter', date_format='d/m/yyyy') as writer:
            final_index.to_excel(writer, sheet_name = 'Sheet1',index = False)
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            cell_format = workbook.add_format()
            cell_format.set_bold()
            cell_format.set_text_wrap()
            cell_format.set_align('vcenter')
            cell_format.set_font_size(11) 
            cell_format.set_align('center')
            
            cell_format2 = workbook.add_format()
            cell_format2.set_text_wrap()
            cell_format2.set_align('vcenter')
            cell_format2.set_font_size(11)
            cell_format2.set_align('center')

            worksheet.set_column(0, 0, 55, cell_format)
            widths = [12, 10, 9, 10, 50, 21, 70]         
            for x in range(1, len(widths)):
                worksheet.set_column(x, x, widths[x], cell_format2)


        # Dataframe with all jobs
        frames.append(final_index)
        print(f'{p} finished')

    result = pd.concat(frames).reset_index().drop(['index'], axis=1)
    links_list = list(result['Link']) 
    indexes = [links_list.index(x) for x in set(links_list)]  
    indexes.sort()

    result2 = pd.DataFrame(columns=['Name','Date placed','Days left','Deadline', 'Salary', 'Location', 'Link'], index=range(0))
    result2 = pd.concat([result2, result.loc[indexes]], ignore_index=True)
    result2 = result2.sort_values('Date placed', ascending= False)
    result2['Date placed'] = result2['Date placed'].astype(str)

    name_file = cwd + '/all_jobs.xlsx'
    with pd.ExcelWriter(name_file, engine='xlsxwriter', date_format='d/m/yyyy') as writer:
        result2.to_excel(writer, sheet_name = 'Sheet1',index = False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        cell_format = workbook.add_format()
        cell_format.set_bold()
        cell_format.set_text_wrap()
        cell_format.set_align('vcenter')
        cell_format.set_font_size(11) 
        cell_format.set_align('center') 
            
        cell_format2 = workbook.add_format()
        cell_format2.set_text_wrap()
        cell_format2.set_align('vcenter')
        cell_format2.set_font_size(11)
        cell_format2.set_align('center')

        worksheet.set_column(0, 0, 55, cell_format)
        widths = [12, 12, 9, 10, 50, 21, 70]         
        for x in range(1, len(widths)):
            worksheet.set_column(x, x, widths[x], cell_format2)


    f = open(cwd + '/log.txt', 'a')
    f.write(f'Code ran on {daytime} at {str(now.time()).split(".")[0]}. \n')
    f.close()

    print('Finished')