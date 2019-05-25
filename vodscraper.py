import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
def buildURL(character="",player="",tournament=""):
    default_url = "https://vods.co/ultimate"
    path = "/ultimate/"
    if(character):
        path += "character/" + character + "/"
    if(player):
        path += "player/" + player + "/"
    if(tournament):
        path += "tournament/" + tournament + "/"
    return urljoin(default_url,path)
def getVideoUrl(url):
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text,"lxml")   
    if(len(parsed_html.find_all("tr")) < 2):
        return None 
    view_link = parsed_html.find_all("tr")[1].find("a")["href"]
    view_response = requests.get(view_link)
    view_html = BeautifulSoup(view_response.text,"lxml")
    return  view_html.find("iframe")["src"]
def getVideoID(url):
    embedRegex = re.compile("embed/")    
    search_results = embedRegex.search(url)
    if(search_results == None):
        return None
    videoID = ""
    for char in url[search_results.span()[1]:]:
        if char == "?":
            return videoID
        videoID += char
    return videoID
def getVod(character="",player="",tournament=""):
    if(character == "" and player == "" and tournament == ""):
        return None
    full_url = buildURL(character,player,tournament)
    link = getVideoUrl(full_url)
    return getVideoID(link) 
