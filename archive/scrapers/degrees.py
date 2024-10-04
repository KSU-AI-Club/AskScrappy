from bs4 import BeautifulSoup
from lxml import etree
import requests
import re
import json
from os import path

#https://stackoverflow.com/questions/46419607/how-to-automatically-install-required-packages-from-a-python-script-as-necessary

class DegreePage:

    def __init__(self, title:str | None = "", description:str | None = None, careers:str | None = None, school:str | None = None):
        #intentionally not using salary, cant really quantify how important money is to someone
        self.title = title
        self.description = description
        self.careers = careers
        self.school = school
    
    def __str__(self):
        return self.title

#End DegreePage

#Takes a url, spits back a BS4 object.
def soupify(url:str) -> BeautifulSoup:
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
    temp_page = requests.get(url, headers=headers, timeout=3)
    return BeautifulSoup(temp_page.text,features='html.parser')

#This nabs all the links within a given BeautifulSoup object and returns them in a list
#Only checks for a tags
def get_links(soup:BeautifulSoup) -> list:
    a_tags = soup.find_all("a")
    links = []
    for a in a_tags:

        if a.has_attr('href'):
            links.append(a['href'])

    return links

#End get_links

#Takes in a degree page as a bs4 object and packages up the info into a dict
def package_page_info(soup:BeautifulSoup) -> DegreePage:
    page = DegreePage()
    page.title = re.sub(r'[^A-Za-z0-9\'/() ]', '',soup.find(class_="banner_message").text)
    print("Degree title detected as {}".format(page.title))
    while page.description == "" or page.description == None:
        page.description = input("Enter a brief description of the course: ")
    
    #Makes it so you can skip json files you've already made.
    if page.description == "skip":
        return page

    while page.careers == "" or page.careers == None:
        page.careers = input("Enter a few possible careers listed: ")

    while page.school == "" or page.school == None:
        page.school = input("Enter the school/department: ")

    return page
    
#End package_page_info

#Writes a json file given a dictionary
#If overwrite is set to true, it will not check if the file exists first.
def write_json(filename:str, data:dict, overwrite=False, indent=4) -> None:
    if not overwrite and path.isfile(filename):
        return

    with open(filename, "w") as f:
        json.dump(data, f, indent=indent)

#End write_json

#Function that is run when the script is executed
#At the moment, it runs through the list of degrees and prompts the user to enter them all.
#Cant be run from inside of vim because of the input() funcs
def main() -> None:
    b_soup = soupify("https://www.kennesaw.edu/degrees-programs/bachelor-degrees/index.php").find(class_="searchable_list")
    m_soup = soupify("https://www.kennesaw.edu/degrees-programs/master-degrees/index.php").find(class_="searchable_list")
    
    b_links = get_links(b_soup)
    m_links = get_links(m_soup)
    
    #=============Bachelors Degree Pages===========
    for link in b_links:
        t_soup = soupify(link)
        page = package_page_info(t_soup)
        json_name = "json/{}.json".format(str(page))
        if path.isfile(json_name):
            continue

        write_json(json_name, page.__dict__)

    #==============Masters Degree Pages=============
    for link in m_links:
        t_soup = soupify(link)
        page = package_page_info(t_soup)
        json_name = "json/{}.json".format(str(page))
        if path.isfile(json_name):
            continue

        write_json(json_name, page.__dict__)
    
#End main

if __name__ == "__main__":
    main()