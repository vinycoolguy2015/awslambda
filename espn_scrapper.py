from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re


class App:
	def __init__(self,player_name=input("Enter the player name you want to search ")):
		self.player_name=player_name
		if self.player_name == '':
			print("Player name not given")
			exit()
		self.driver=webdriver.Chrome('/usr/local/bin/chromedriver')
		self.url=self.search_profile()
		if not self.url is None:
			personal_data,bowling_record,batting_record=self.parse_profile()
			print ("Personal Data\n")
			print (personal_data)
			print ("\nBatting Record\n")
			print (batting_record)
			print ("\nBowling Record\n")
			print (bowling_record)
		else:
			print("Player profile not found")
			exit()
		self.driver.close()
		
	def search_profile(self):
		
		profile_found=False
		url=None
		self.driver.get('https://www.google.com')
		try:
			input_box = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@title="Search"]')));
		except TimeoutException:
			print("Connection timeout during googling")
			self.driver.close()
			exit()
		input_box.send_keys(self.player_name)
		input_box.send_keys(Keys.ENTER)
		try:
			#results = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="med"]'))).find_elements_by_tag_name('a')
                        results = self.driver.find_elements_by_xpath("//div[@class='r']/a[@href]")
		except TimeoutException:
			print("Connection timeout fetching results")
			self.driver.close()
			exit()
		for result in results:
			espn=re.search('^http://www.espncricinfo.com', result.get_attribute("href"))
			if espn and 'player' in result.get_attribute("href"):
				profile_found=True
				url=result.get_attribute("href")
				break
		return url
	
	def parse_profile(self):
		data={}
		bowling_record={}
		batting_record={}
		self.driver.get(self.url)
		urls=self.driver.find_elements_by_class_name('ciPlayerinformationtxt')
		for url in urls:
			b=url.find_element_by_tag_name('b')
			span=url.find_element_by_tag_name('span')
			data[b.text]=span.text
			personal_data=dict((key,value) for key, value in data.items() if key in ['Playing role','Major teams','Current age','Height','Born','Batting style','Bowling style','Full name'] )
		data_rows=self.driver.find_elements_by_xpath("//tr[@class='data1']")
		
		
		if len(data_rows)<20:
			format_played=4
		elif len(data_rows) < 28:
			format_played=5
		else:
			format_played=6
			
		batting_rows=data_rows[0:format_played]
		
		for row in batting_rows:
			columns=row.find_elements_by_tag_name('td')
			data_format={}
			data_format['Matches']=columns[1].text
			data_format['Innings']=columns[2].text
			data_format['Not Outs']=columns[3].text
			data_format['Runs']=columns[4].text
			data_format['Highest Score']=columns[5].text
			data_format['Average']=columns[6].text
			data_format['Balls Faced']=columns[7].text
			data_format['Strike Rate']=columns[8].text
			data_format['Centuries']=columns[9].text
			data_format['Half Centuries']=columns[10].text
			data_format['Boundries']=columns[11].text
			data_format['Sixers']=columns[12].text
			data_format['Catches']=columns[13].text
			data_format['Stumpings']=columns[14].text
			batting_record[columns[0].text]=data_format
				
		bowling_rows=self.driver.find_elements_by_xpath("//tr[@class='data1']")[format_played:format_played*2]
		for row in bowling_rows:
			columns=row.find_elements_by_tag_name('td')
			data_format={}
			data_format['Matches']=columns[1].text
			data_format['Innings']=columns[2].text
			data_format['Balls']=columns[3].text
			data_format['Runs']=columns[4].text
			data_format['Wickets']=columns[5].text
			data_format['BBI']=columns[6].text
			data_format['BBM']=columns[7].text
			data_format['Average']=columns[8].text
			data_format['Economy']=columns[9].text
			data_format['Strike Rate']=columns[10].text
			data_format['4 Wickets']=columns[11].text
			data_format['5 Wickets']=columns[12].text
			data_format['10 Wickets']=columns[13].text
			bowling_record[columns[0].text]=data_format
		return personal_data,bowling_record,batting_record
			
		
if __name__=='__main__':
	app=App()
	


	
