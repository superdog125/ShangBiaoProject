from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time

class commmpyCraw(object):

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/opt/google/chrome/chromedriver')
    def log_in(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.driver.get("https://www.qichacha.com/user_login")
        time.sleep(3)
        self.driver.find_element_by_id("nameNormal").send_keys("17816124708")
        self.driver.find_element_by_id("pwdNormal").send_keys("qiaoye55")
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block m-t-md login-btn']").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[@class='close']").click()
        time.sleep(2)
    def parse(self, content):
        self.driver.find_element_by_xpath("//li[@data-index='10']").click()
        self.driver.find_element_by_xpath("//input[@class='form-control input-lg']").send_keys(content)
        self.driver.find_element_by_xpath("//input[@id='V3_Search_bt']").click()
        self.driver.save_screenshot("chrome.png")



if __name__ == "__main__":

    c_crawl = commmpyCraw()
    c_crawl.log_in("17816124708", "qiaoye55")
    c_crawl.parse("上海")

