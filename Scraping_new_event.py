

# Importing the librairies

import pandas as pd
from requests import get
from bs4 import BeautifulSoup 

namefile = input('Nom du fichier en inluant .txt ')
# Importing the dataset from COINDESK

coindesk_url ='https://www.coindesk.com/bitcoin-events'
response = get(coindesk_url)

html_soup = BeautifulSoup(response.text,'html.parser')

containers = html_soup.find('table', class_="table")

body = containers.find_all("tr")

urls = []
dates = []
names = []
names_lower = []
places = []
for element in body:
    link = element.find('a')['href']
    link = link.split("coindesk")[0]
    final_url = link.split("?utm")[0]+"?utm_source=chaineum"
    
    urls.append(final_url)
  
    
    elements = element.find_all('td')
    date=elements[0].text
    if ('June,') in date:
        date="June"+ date.split('June,')[1]
        
    if('October,') in date:
        date= "October 1, "+date.split(', ')[1]
    dates.append(date)
    names.append(elements[1].text)
    names_lower.append(elements[1].text.lower())
    places.append(elements[2].text)
    
# Importing the dataset from ICOHOLDER
  
url1 ='https://icoholder.com/en/events?type=next&page='
url2 ='&hype=&df=&dt=&discount=&city=&country=&region='
k=1
exist= True



links1 = []

while(exist):  # Boucle pour récupérer les liens sur toutes les pages de ICOHOLDER
    url = url1+str(k)+url2
    print(k)
    k+=1
    response = get(url)

    html_soup = BeautifulSoup(response.text,'html.parser')
    try:
        containers = html_soup.find('div', class_="items near-items")
    
        
    
        body= containers.find_all('a')


        for itm in body:
    
            places.append(itm.find('div', class_="event-loc").text.split('\n')[2]+itm.find('div', class_="event-loc").text.split('\n')[3])
            names.append(itm.find('h2').text)
            names_lower.append(itm.find('h2').text.lower())
            date = itm.find('p').text
            day = date.split('\n')[0]
            month = date.split('\n')[1]
    
            if 'Jan'in month:
                month='January'
            elif 'Feb'in month:
                month='February'
            elif 'Mar'in month:
                month='March'
            elif 'Apr'in month:
                month='April'
            elif 'Jun'in month:
                month='June'
            elif 'Jul'in month:
                month='July'
            elif 'Aug'in month:
                month='August'
            elif 'Sep'in month:
                month='September'
            elif 'Oct'in month:
                month='October'
            elif 'Nov'in month:
                month='November'
            elif 'Dec' in month:
                month='December'
    
            year = date.split('\n')[2]
            if ' ' in year:
                year=year.split(' ')[1]
    
            final_date = month +' '+ day+', '+year
            dates.append(final_date)
    
    
            link='https://icoholder.com'
            link+=itm['data-direct']
            links1.append(link)
    except:
        exist=False
        
print('end of while boucle')        

j=0
for itm in links1: # Boucle permettant de récupérer les liens des events
    j+=1
    print('link: '+str(j))
    new_response=get(itm)
    new_soup=BeautifulSoup(new_response.text,'html.parser')
    
    new_containers = new_soup.find_all('div', class_="text-align-center")
    redirect_link=new_containers[1].find('a')['href']
    try:
        event_page=get(redirect_link)
        
        event_url=event_page.url
        event_url = event_url.split("icoholder")[0]
        final_url = event_url.split("?utm")[0]+"?utm_source=chaineum"
        
        urls.append(final_url)
    except:
        urls.append(' Error ')  
        
# Mise au bon format pour créer une Dataframe Pandas       

# Mise en format pour la dataframe panda        
date_df=[]
for itm in dates:
    if ('January') in itm:
        month = '01'
    if ('February') in itm:
        month = '02'
    if ('March') in itm:
        month = '03'
    if ('April') in itm:
        month = '04'
    if ('May') in itm:
        month = '05'
    if ('June') in itm:
        month = '06'
    if ('July') in itm:
        month = '07'
    if ('August') in itm:
        month = '08'
    if ('September') in itm:
        month = '09'
    if ('October') in itm:
        month = '10'
    if ('November') in itm:
        month = '11'
    if ('December') in itm:
        month = '12'
        
    day = itm.split(' ')[1].split(',')[0].split('-')[0] 
    year = itm.split(', ')[1]
    
    date_df.append(month+('/')+day+('/')+year)
    
names_compare=[]
name_compare=''
for name in names:
    if 'The' in name.split(' ')[0]:
        name = name[4:]
    name_compare = name.split(' ')[0]
    try:
        name_end=name.split(' ')[1]
    except:
        name_end=''
    name_compare +=name_end    
    name_compare = name_compare.split(' ')[0]
    name_compare = name_compare.split(':')[0]
    name_compare = name_compare.split(',')[0]
    name_compare = name_compare.lower()
    names_compare.append(name_compare)
# Dataframe pandas    
data = pd.DataFrame({
        'Names' : names,
        'Dates' : dates,
        'Dates_df' : date_df,
        'Links' : urls,
        'Places' : places,
        'Names_compare' : names_compare,
        'Names_lower' :names_lower,
       
        })
# Classement par dates   
data2 = pd.read_csv('last_data.csv')   

result = pd.concat([data,data2], ignore_index=True)   
all_result = result.drop_duplicates(subset='Names')  
data = result.drop_duplicates(subset='Names',keep=False)    
    
all_result['Dates_df'] = pd.to_datetime(all_result['Dates_df'])
all_result = all_result.sort_values(by=['Dates_df'])    
    
    
data['Dates_df'] = pd.to_datetime(data['Dates_df'])
data = data.sort_values(by=['Dates_df']) 
# Suppression des doublons
data = data.drop_duplicates(subset='Names_lower',keep='first')  
data = data.drop_duplicates(subset='Links',keep='first')  
duplicate_series = data.duplicated(subset='Names_compare',keep='first')

#Compare avec les anciens events



duplicate_list =duplicate_series.tolist()
all_result.to_csv('last_data.csv',index=False)
dates = []  
names = []
final_links = []
places = []
dates = data['Dates'].tolist()
names = data['Names'].tolist()
final_links = data['Links'].tolist()
places = data['Places'].tolist()
places_uni=[]
contact_adress = []
# Uniformatisation des noms de pays
import unidecode
for place in places:
    place= unidecode.unidecode(place)
    if 'United Kingdom' in place:
        place= place.split(' ')[0]+(' UK')
    if 'United States'in place or 'NV'in place or'New York'in place or'Colorado'in place:
        place= place.split(',')[0]+(', USA')
        
    if 'NY' in place:
        place='New York, USA'
    places_uni.append(place)
    
    
#Recherche adresse de contact
for url in final_links:
  #  if not 'Error' in url and not'cryptovalleyconference'in url:
    print('k')
    try:
        response=get(url)
        html_soup = BeautifulSoup(response.text,'html.parser')
    
        containers = html_soup.find_all('a')
        containers=str(containers)
        try:
            containers2= containers.split('mailto:')[1].split('"')[0]
            containers2= containers2.split('?')[0]
            
            contact_adress.append(containers2)
            print(containers2)
        except:
            contact_adress.append('')
    except:
        contact_adress.append('')
            
    #elif 'Error' in url or 'cryptovalleyconference'in url:
        #contact_adress.append('')
        

# classement par mois
results= []
event19 = []
event20 = []
jan_events19 = []
feb_events19 = []
mar_events19 = []
apr_events19 = []
may_events19 = []
jun_events19 = []
jul_events19 = []
aug_events19 = []
sep_events19 = []
oct_events19 = []
nov_events19 = []
dec_events19 = []
jan_events20 = []
feb_events20 = []
mar_events20 = []
apr_events20 = []
may_events20 = []
jun_events20 = []
jul_events20 = []
aug_events20 = []
sep_events20 = []
oct_events20 = []
nov_events20 = []
dec_events20 = []
event_verif=[]
for i in range(len(dates)):
    result=""
    result+=dates[i]
    result+=': ['
    result+=names[i]
    result+=']url:'
    result+=final_links[i]
    result+=' - '
    result+=places_uni[i]
    result+='\n'
    if duplicate_list[i]==True:
        event_verif.append(result)
        result=''
    
    if not "Error" in result:
        if "2019" in result:
           
            if "January" in result:
                jan_events19.append(result)
            elif "February" in result:
                feb_events19.append(result)
            elif "March" in result:
                mar_events19.append(result)
            elif "April" in result:
                apr_events19.append(result)
            elif "May" in result:
                may_events19.append(result)
            elif "June" in result:
                jun_events19.append(result)
            elif "July" in result:
                jul_events19.append(result)
            elif "August" in result:
                aug_events19.append(result)
            elif "September" in result:
                sep_events19.append(result)
            elif "October" in result:
                oct_events19.append(result)
            elif "November" in result:
                nov_events19.append(result)
            elif "December" in result:
                dec_events19.append(result)
                
                
        if "2020" in result:
           
            if "January" in result:
                jan_events20.append(result)
            elif "February" in result:
                feb_events20.append(result)
            elif "March" in result:
                mar_events20.append(result)
            elif "April" in result:
                apr_events20.append(result)
            elif "May" in result:
                may_events20.append(result)
            elif "June" in result:
                jun_events20.append(result)
            elif "July" in result:
                jul_events20.append(result)
            elif "August" in result:
                aug_events20.append(result)
            elif "September" in result:
                sep_events20.append(result)
            elif "October" in result:
                oct_events20.append(result)
            elif "November" in result:
                nov_events19.append(result)
            elif "December" in result:
                dec_events20.append(result)
    
    results.append(result)
# fichier adresses contact

saveFilead = open('contact_adress.txt','w')
saveFilead.write("Contact adress:\n")
for i in range (len(result)):
        if contact_adress[i] != '':
            saveFilead.write("\n")
            saveFilead.write(results[i])
            saveFilead.write("\n")
            saveFilead.write(contact_adress[i])
            saveFilead.write("\n")
            saveFilead.write("\n")
            
saveFilead.close()

 # Ecriture ua bon foramt dans un fichier .txt   
saveFile = open(namefile,'w')

if (len(jan_events19)!=0):
    saveFile.write("\n")
    saveFile.write("cb[January, 2019]cb\n")
    saveFile.write("\n")
    for event in jan_events19:
        saveFile.write(event)
 
if (len(feb_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[February, 2019]cb\n")
    saveFile.write("\n")
    for event in feb_events19:
        saveFile.write(event)

if (len(mar_events19)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[March, 2019]cb\n")
    saveFile.write("\n")
    for event in mar_events19:
        saveFile.write(event)

if (len(apr_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[April, 2019]cb\n")
    saveFile.write("\n")
    for event in apr_events19:
        saveFile.write(event)

if (len(may_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[May, 2019]cb\n")
    saveFile.write("\n")
    for event in may_events19:
        saveFile.write(event)

if (len(jun_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[June, 2019]cb\n")
    saveFile.write("\n")
    for event in jun_events19:
        saveFile.write(event)

if (len(jul_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[July, 2019]cb\n")
    saveFile.write("\n")
    for event in jul_events19:
        saveFile.write(event)

if (len(aug_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[August, 2019]cb\n")
    saveFile.write("\n")
    for event in aug_events19:
        saveFile.write(event)

if (len(sep_events19)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[September, 2019]cb\n")
    saveFile.write("\n")
    for event in sep_events19:
        saveFile.write(event)
   
if (len(oct_events19)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[October, 2019]cb\n")
    saveFile.write("\n")
    for event in oct_events19:
        saveFile.write(event)

if (len(nov_events19)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[November, 2019]cb\n")
    saveFile.write("\n")
    for event in nov_events19:
        saveFile.write(event)

if (len(dec_events19)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[December, 2019]cb\n")
    saveFile.write("\n")
    for event in dec_events19:
        saveFile.write(event)
   
if (len(jan_events20)!=0):
    saveFile.write("\n")
    saveFile.write("cb[January, 2020]cb\n")
    saveFile.write("\n")
    for event in jan_events20:
        saveFile.write(event)
 
if (len(feb_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[February, 2020]cb\n")
    saveFile.write("\n")
    for event in feb_events20:
        saveFile.write(event)

if (len(mar_events20)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[March, 2020]cb\n")
    saveFile.write("\n")
    for event in mar_events20:
        saveFile.write(event)

if (len(apr_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[April, 2020]cb\n")
    saveFile.write("\n")
    for event in apr_events20:
        saveFile.write(event)

if (len(may_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[May, 2020]cb\n")
    saveFile.write("\n")
    for event in may_events20:
        saveFile.write(event)

if (len(jun_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[June, 2020]cb\n")
    saveFile.write("\n")
    for event in jun_events20:
        saveFile.write(event)

if (len(jul_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[July, 2020]cb\n")
    saveFile.write("\n")
    for event in jul_events20:
        saveFile.write(event)

if (len(aug_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[August, 2020]cb\n")
    saveFile.write("\n")
    for event in aug_events20:
        saveFile.write(event)

if (len(sep_events20)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[September, 2020]cb\n")
    saveFile.write("\n")
    for event in sep_events20:
        saveFile.write(event)
   
if (len(oct_events20)!=0):
    saveFile.write("\n")    
    saveFile.write("cb[October, 2020]cb\n")
    saveFile.write("\n")
    for event in oct_events20:
        saveFile.write(event)

if (len(nov_events20)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[November, 2020]cb\n")
    saveFile.write("\n")
    for event in nov_events20:
        saveFile.write(event)

if (len(dec_events20)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[December, 2020]cb\n")
    saveFile.write("\n")
    for event in dec_events20:
        saveFile.write(event)
        
if (len(event_verif)!=0):    
    saveFile.write("\n")    
    saveFile.write("cb[Event à verifier]cb\n")
    saveFile.write("\n")
    for event in event_verif:
        saveFile.write(event)
saveFile.close()    

 
