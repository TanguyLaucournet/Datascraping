from requests import get
from bs4 import BeautifulSoup
import pandas as pd 

dates = []
end_links = []
titles = []
links= []
contents= []
img = []

url ='https://www.inwara.com/research'
response = get(url)

html_soup = BeautifulSoup(response.text,'html.parser')
datetime = html_soup.find_all('time')
for date in datetime:
    dates.append(date.text)
containers = html_soup.find_all('div', class_="page-header")


for itm in containers:
    itm = itm.find('a')
    titles.append(itm.text)
    end_links.append(itm['href'])
  

for link in end_links:
    url ='https://www.inwara.com'
    url+=link
    links.append(url)
    response = get(url)

    html_soup = BeautifulSoup(response.text,'html.parser')
    containers = html_soup.find_all('p', class_="graf graf--p")        
    content =''
    for itm in containers:
        if "InWara’s Monthly Report:" not in itm.text and 'Like our data' not in itm.text:
            content +=itm.text
            content +="\n"
    contents.append(content)
    
    containers = html_soup.find_all('figure')
    content=''
    for itm in containers:
        result ='https://www.inwara.com'+ itm.find('img')['src']
        content+= result + ' '
    img.append(content)
        
data = pd.DataFrame({
        'Titles' : titles,
        'Dates' : dates,
        'Links' : links,
        'Contenu' : contents,
        'Images' : img,
                 })     
data.to_csv('out4.csv', sep='\t', encoding='utf-8-sig')

saveFilead = open('article_inwara.txt','w', encoding='utf-16')
saveFilead.write("Article Inwara\n")
for i in range (len(titles)):
        if contents[i] != '':
            saveFilead.write("\n")
            saveFilead.write(links[i]+ '  ')
            saveFilead.write(img[i])
            saveFilead.write("\n")
            saveFilead.write(dates[i])
            saveFilead.write("\n")
            saveFilead.write(titles[i])
            saveFilead.write("\n")
            saveFilead.write(contents[i])
            saveFilead.write("\n")
            saveFilead.write("---------------------------------------------------------------------------------")
            saveFilead.write("\n")
            saveFilead.write("\n")
saveFilead.close()           
       

   