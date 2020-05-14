from requests import get
from bs4 import BeautifulSoup
import pandas as pd 

dates =[]
links = []    
titles = []
contents = []

images = []
url ='https://www.cbinsights.com/research/bitcoin-blockchain/'
response = get(url)

html_soup = BeautifulSoup(response.text,'html.parser')

containers = html_soup.find_all('h1', class_="article-title")


for itm in containers:
    link = 'https://www.cbinsights.com'
    
    endlink= itm.find('a')['href']
    links.append(link + endlink)
    titles.append(itm.text)
    
for link in links:
    response = get(link)
    html_soup = BeautifulSoup(response.text,'html.parser')
    # Récupérer la date
    containers = html_soup.find('li', class_="publish-date")
    try:
        dates.append(containers.text)
    except:
        dates.append('')
     # Récupérer le contenu   
    containers = html_soup.find_all('p')
    content=''
    for itm in containers:
        if 'Start your free trial today'not in itm.text and 'Download the free report' not in itm.text and 'newsletter' not in itm.text:
            content += itm.text +"\n"
    contents.append(content)   
    #Récupérer les images
    containers = html_soup.find_all('img')
    img = []
    for itm in containers:
        image = itm['src']
        img.append(image)
    images.append(img)
    
data = pd.DataFrame({
        'Titles' : titles,
        'Dates' : dates,
        'Links' : links,
        'Contenu' : contents,
        'Images' : images,
                 })     
data.to_csv('out5.csv', sep='\t', encoding='utf-8-sig')

saveFilead = open('article_cbinsight.txt','w', encoding='utf-16')
saveFilead.write("Article CBInsight\n")
for i in range (len(titles)):
        if contents[i] != '':
            saveFilead.write("\n")
            saveFilead.write(links[i]+ '  ')
            saveFilead.write("\n")
            saveFilead.write("Images: ")
            saveFilead.write("\n")
            for k in range(len(images[i])):
                saveFilead.write(images[i][k])
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