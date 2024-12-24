import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

import argparse
import warnings
import time


# Professor Table:

# class=TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx
#   class=TeacherCard__NumRatingWrapper-syjs0d-2 joEEbw
#       class=CardNumRating__StyledCardNumRating-sc-17t4b9u-0 eWZmyX
# Quality Stat  class=CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 icXUyq
# Total Rating  class=CardNumRating__CardNumRatingCount-sc-17t4b9u-3 jMRwbg

# class=TeacherCard__CardInfo-syjs0d-1 fkdYMc
#   class=CardName__StyledCardName-sc-1gyrgim-0 cJdVEK <- Name
#    


# Show More Button
# class=SearchResultsPage__AddPromptWrapper-vhbycj-2 dubepU
#   class=Buttons__Button-sc-19xdot-1 PaginationButton__StyledPaginationButton-txi1dr-1 glImpo

# Each Data contains:
# Name, Number of Rating, Quality, Department, percentage would take again, level of difficulty

class RateMyProfessorScrapper:
    def __init__(self):
        self.root_path = "https://www.ratemyprofessors.com/search/professors/481?q=*"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-cache")
        self.options.add_argument("--enable-unsafe-swiftshader")
        self.options.add_argument('log-level=3')
        self.options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.show_more_button = ""
        
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.root_path)
    
    def set_show_more_button(self):
        try:
            Xpath = '//*[@id="root"]/div/div/div[3]/div/div[2]/div[2]/button'
            self.show_more_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, Xpath)))
            self.driver.execute_script(
                            "arguments[0].setAttribute('id', arguments[1]);", self.show_more_button, "RMP_Scrape")
        except Exception as e:
            #print(f"Set Show More Button: Some error occurred \n {e.msg}")
            raise e
            
    def check_show_more_button(self):
        try:
            self.set_show_more_button()
            
            print("Searching for more Professors...")
            self.driver.execute_script(
                "arguments[0].click();", self.show_more_button)

            self.show_more_button = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "RMP_Scrape")))
            
            self.driver.execute_script(
                "arguments[0].click();", self.show_more_button)
            
            return True
        except:
            return False 
    
    def get_professor_data(self):
        
        warnings.filterwarnings("ignore")
        
        while self.check_show_more_button():
            pass
        
        html_page = self.driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        
        quality_table = soup.find_all(class_="CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
        total_rating_table = soup.find_all(class_="CardNumRating__CardNumRatingCount-sc-17t4b9u-3")

        teacher_name_table = soup.find_all(class_="CardName__StyledCardName-sc-1gyrgim-0")
        department_table = soup.find_all(class_="CardSchool__Department-sc-19lmz2k-0 haUIRO")
        retake_difficulty_table = soup.find_all(class_="CardFeedback__CardFeedbackNumber-lq6nix-2 hroXqf")
        
        quality_col = [r.get_text() for r in quality_table]
        total_rating_col = [r.get_text().split(" ")[0] for r in total_rating_table]
        teacher_name_col = [r.get_text() for r in teacher_name_table]
        department_col = [r.get_text() for r in department_table]
        retake_col = [r for r in np.array(retake_difficulty_table)[0::2].reshape(-1)]
        difficulty_col = [r for r in np.array(retake_difficulty_table)[1::2].reshape(-1)]

        professor_df = pd.DataFrame({"teacher_name": teacher_name_col, 
                                    "department": department_col,
                                    "quality": quality_col,
                                    "total_rating": total_rating_col,
                                    "difficulty": difficulty_col,
                                    "retake": retake_col})
        
        professor_df.to_csv("professor_data.csv", index=False)
        print("Data Saved")

def main():
    rmp_scraper = RateMyProfessorScrapper()
    rmp_scraper.get_professor_data()
    
if __name__ == "__main__":
    main()
