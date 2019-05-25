import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
def buildURL(character="",player="",tournament=""):
    """
        Args:
            character(string):The character that is going to be queried
            player(string):The player name who is going to be queried
            tournament(string):The tournament name who is going to be querieed
        Returns:
            query_url(string):This function returns the url for the query
        This function takes in a character a player and a tournament and
        returns the url to query the vod website 
    """
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
    """
        Args:
            url(string):The url to query the vod website
        Returns:
            video_url(string):The url to the embeded youtube video
        This function takes in a query url returns the embedded YouTube 
        url for the first game that appears on the website
    """
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text,"lxml")   
    if(len(parsed_html.find_all("tr")) < 2):
        return None 
    view_link = parsed_html.find_all("tr")[1].find("a")["href"]
    view_response = requests.get(view_link)
    view_html = BeautifulSoup(view_response.text,"lxml")
    return  view_html.find("iframe")["src"]
def getVideoID(url):
    """
        Args:
            url(string):The url for the embedded YouTube video
        Returns:
            videoID(string): The id for the video that matches
            the embedded youtube video
        This function takes in a url for an embedded YoutTube video
        and returns the id for that video
    """
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
    """
        Args:
            character(string):The character that is going to be queried
            player(string):The player name who is going to be queried
            tournament(string):The tournament name who is going to be querieed
        Returns:
            videoID(string): The id for the video that matches
            the embedded youtube video
        This function takes in a character a player and a tournament
        queries the vods.co website and then returns the first video
        which matches the query
    """
    if(character == "" and player == "" and tournament == ""):
        return None
    full_url = buildURL(character,player,tournament)
    link = getVideoUrl(full_url)
    return getVideoID(link) 
