from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time

class App:
	def __init__(self,email='abc@abc.com',password='abc'):
		self.email=email
		self.password=password
		self.driver=webdriver.Chrome('C:\\Users\\vinayak\\Desktop\\Python\\Selenium\\chromedriver')
		self.login()
		print(self.course_search())
		self.driver.close()
		
		
	def login(self):
		self.driver.get('https://university.mongodb.com/')
		sign_in=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Sign in")]')))
		sign_in.click()
		try:
			email=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
			password=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
			submit=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="submit"]')))
		except TimeoutException:
			print("Connection timeout")
			self.driver.close()
			exit()
		email.send_keys(self.email)
		password.send_keys(self.password)
		submit.click()
		
	def course_search(self):
		content={}
		courses=WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "My Courses")]')))
		courses.click()
		completed_courses=WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Completed Courses")]')))
		completed_courses.click()
		course=WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "M102")]')))
		course.click()
		table=WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-striped"]/tbody')))
		links=table.find_elements_by_tag_name('tr')[0:7]
		urls=[link.find_element_by_tag_name('a').get_attribute('href') for link in links]
		for url in urls:
			self.driver.get(url)
			list=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="lesson-list"]')))
			lessons=list.find_elements_by_tag_name('li')
			for lesson in lessons:
				homework=re.search('^Homework', lesson.text)
				if not homework:
					lesson.click()
					time.sleep(5)
					youtube_link=self.driver.find_element_by_tag_name('iframe').get_attribute('src').split('?')[0]
					content[lesson.text]=youtube_link
		return content
					
					
			
if __name__=='__main__':
	app=App()
