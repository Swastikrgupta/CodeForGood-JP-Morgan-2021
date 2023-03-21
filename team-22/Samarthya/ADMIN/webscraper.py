import requests
import bs4
import sys
from bs4 import BeautifulSoup

def ndmc():
    resp=requests.get("https://www.ndmc.gov.in/departments/education.aspx")
    soup=bs4.BeautifulSoup(resp.content)
    titles=soup.find_all("a",attrs={"class":""})

    announcementName=[]
    announcementLink=[]

    for i in titles:
        if(i["href"][:11]=="Departments"):
            print(i.get_text())
            print(("https://www.ndmc.gov.in/departments/"+i["href"]).replace(" ","%20"),end="\n\n")
            
            announcementName.append(i.get_text())
            announcementLink.append(("https://www.ndmc.gov.in/departments/"+i["href"]).replace(" ","%20"))
    NDMC=zip(announcementName,announcementLink)
    return NDMC



def sims():
    resp=requests.get("https://www.sims-online.org/circular")
    soup=bs4.BeautifulSoup(resp.content)
    titles=soup.find_all("a")

    announcementName=[]
    announcementLink=[]

    for i in titles:
        if(i.get('href')):
            if(i.get('href')[:5]=="https"):
                print(i.get_text())
                print(i["href"],end="\n\n")

                announcementName.append(i.get_text())
                announcementLink.append(i["href"])
    SIMS=zip(announcementName,announcementLink)
    return SIMS
