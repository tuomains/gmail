# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import SeleniumLibrary

GOOGLE_URL = "https://www.google.fi/"

class Action():

 def make_google_search(self,search_string):
  print(search_string)
  chrome_options = Options()
  chrome_options.add_argument("--disable-infobars")
  chrome_options.add_argument("--lang=fin")
  #chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-features=RendererCodeIntegrity")
  chrome_options.add_argument("test-type")
  driver = webdriver.Chrome(chrome_options=chrome_options)
  driver.get(GOOGLE_URL)
  driver.find_element(By.NAME,"q").send_keys(search_string)
  driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
  driver.find_element(By.XPATH,"//*[@class='LC20lb DKV0Md']").click()
  driver.get_screenshot_as_file("screenshot.jpg")
  page = driver.page_source
  return page

if __name__=="__main__":
 t=Action()
 r = t.make_google_search("asdf")
 print(r)