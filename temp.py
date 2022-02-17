# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from urllib import parse
from urllib.error import HTTPError
import certifi
import ssl



ssl._create_default_https_context=ssl._create_unverified_context
store_person={}
store_links=[]
def url_open(url):
    try:
        
        
        with urlopen(url,context=ssl._create_default_https_context(cafile=certifi.where())) as url:
           
            soup = BeautifulSoup (url,'lxml')
            
            return soup
    except ValueError:
        with urlopen(parse.unquote(url),context=ssl._create_default_https_context(cafile=certifi.where())) as url:
           
            soup = BeautifulSoup (url,'lxml')
            
            return soup
    except HTTPError:
        return
def getPage(soup):
    return soup.prettify()

def getName(soup):
    try:
        return soup.body.h1.string
    except:
        return None
def getYOB(soup):
    try:
        first=soup.body.find("div",id="bodyContent").find("table",class_="infobox")
        return first.find("span",class_="bday").string.split("-")[0]
    except:
        return None
'''
def getYOD(soup):
    try:
        first=soup.find("div",id="bodyContent").find("table",class_="infobox")
        second= first.find_all("th",class_="infobox-label")[1].string
        
        if(second=="Died"):
            third=first.find_all("td",class_="infobox-data")
            
            return(third[1].contents[0].split(" ")[-1])
    except:
        return None
'''

def getYOD(soup):
    try:
        first=soup.find("div",id="bodyContent").find("table",class_="infobox")
        second=first.find("span",class_="bday")
        third=second.parent.parent.parent.find_next_sibling("tr")
        fourth = third.find("th",class_="infobox-label").string
        
        if(fourth=="Died"):
            fifth=third.find("td",class_="infobox-data").contents[0].split(" ")[-1]
            return fifth
    except:
        return None
        
    
def getLinks(soup):
    third=[]
    
   
    first = soup.find("div",id="bodyContent").find_all("a")
    for i in range(0,len(first)):
            if(first[i].has_attr('href')):
                second = first[i].get("href")
                
                try:
                    
                    index=second.index("/wiki/")
                    if(index>=0):    
                        third.append(second[index:len(second)])
                except:
                    continue
    return third
def store_1(soup,url):
    tmp_url=url.split("/")[-1]
    if tmp_url in store_person:
        return 0
    name=getName(soup)
    dead_year=getYOD(soup)
    birth_year=getYOB(soup)
    if(name!=None):
        if(dead_year!=None):
            if(birth_year!=None):
                
                store_person[tmp_url]=(name,birth_year,dead_year)
                '''
                limit the links, to make it capable to finish the searching
                however, we want to make the store_person will run the whole store_links,
                so we do not set a check in certain number of links, the ultimate size of store_links will bigger
                than 500 but probably smaller than 1500, but the good new of not setting exact number such as only 500 links is
                the program will at least list all the link in the next page, and the store_person will search all those links even 
                the further links from those new notable person will not be recoreded.
                
                '''
                if(len(store_links)<500):
                    
                    store_2(soup,url)
                    print(len(store_links))
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0
def store_2(soup,url):
    tmp_url=url.split("/")[-1]
    links=getLinks(soup)
    for i in links:
        
        store_links.append((tmp_url,i))
        
def store_person_file():
    try:
        with open('notables.csv','w+') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Linkes(https://en.wikipedia.org) in front','Name','Birthyear','DeadYear'])
            for i in store_person:
                csv_writer.writerow([i,store_person[i][0],store_person[i][1],store_person[i][2]])
            f.close()
    except IOError:
        
        raise IOError('Wrong I/O mechanical action')
def store_links_file():
    try:
        with open('links.csv','w+') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Linkes(https://en.wikipedia.org) in front','connected links'])
            for i in store_links:
                csv_writer.writerow([i[0],i[1]])
            f.close()    
    except IOError:
        raise IOError('Wrong I/O mechanical action')
def main():
    
    seed="https://en.wikipedia.org/wiki/Wu_Wenjun"
    soup=url_open(seed)
    
    if(store_1(soup,seed)<1):
        store_2(soup,seed)
    
    i=0
    while(i<len(store_links)):
        url='https://en.wikipedia.org'+store_links[i][1]
        print(i)
        print(url)
        soup=url_open(url)
        if(soup!=None):
            
            store_1(soup,url)
            
            
        i+=1
    print(store_person)
    print(store_links)
    store_person_file()
    store_links_file()
    
if __name__=="__main__":
    main()

