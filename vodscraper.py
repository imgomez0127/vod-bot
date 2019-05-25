import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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
def getVod(character="",player="",tournament=""):
    if(character == "" and player == "" and tournament == ""):
        return None
    full_url = buildURL(character,player,tournament)
    link = getVideoUrl(full_url)
    return link 
print(getVod(character="Pichu"))
