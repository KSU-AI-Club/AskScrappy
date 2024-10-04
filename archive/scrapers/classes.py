from bs4 import BeautifulSoup
import requests
import re
import json

def soupify(url:str) -> BeautifulSoup:
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
    temp_page = requests.get(url, headers=headers)
    return BeautifulSoup(temp_page.text,features='html.parser')

def main() -> dict:
    #32 pages of classes, at the time of making this
    courses = {}
    for page in range(1,32):
        
        url = "https://catalog.kennesaw.edu/content.php?catoid=68&catoid=68&navoid=5469&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={0}#acalog_template_course_filter".format(page)

        page = soupify(url).find_all(class_="block_content")
        for p in page:
            #Key is always re-set first thing on each page so I clear it just to be safe.
            key = ""
            print(len(p.find_all("table")))

            for i in [3,2,1]:
                try:
                    course_list = p.find_all("table")[i]
                    
                    #Usually table 3 is the search box, so looking for this chunk of text makes sure we skip that.
                    if "Filter this list of courses" in course_list.text:
                        continue

                except IndexError as e:
                    if i == 1:
                        print(f"Couldn't find a proper main body tag on page {page}")
                        return

            #Finding all table rows and chopping off some blank ones
            tr_list = course_list.find_all("tr")[1:]
            tr_list = tr_list[:len(tr_list)-1]

            for row in tr_list:
                #Course Categories are only marked by a strong tag, so this makes them the key for the dict
                if len(row.find_all("strong")) > 0:

                    key = re.sub(r'[^A-Za-z0-9 /\':()-]', '', row.text)
                    courses[key] = []

                #Had some issues with the nav bar at the bottom, checking for a colon fixed it, but it could be skipping courses. Not sure.
                elif ":" in row.text:

                    txt = re.sub(r'[^A-Za-z0-9 /\':()-]', '', row.text).split(":")
                    courses[key].append((txt[0],txt[1]))

    return courses


            

if __name__ == "__main__":
    #Creates a json file using class category as the keys for a list of class entries
    #Each entry is a tuple, containing class number (ex: ACCT 2101) as the first entry, and the class name (ex: Internal Auditing) as the second entry.
    classes = main()
    with open("classes.json", "w") as f:
        json.dump(classes, f, indent=4)
