from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4 as bs

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
sauce =driver.page_source
soup = bs.BeautifulSoup(sauce,'lxml')
s = str(soup.find('ul', class_='subnav menu'))
print(s)
