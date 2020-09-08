import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
ua = UserAgent()
header = {'user-agent':ua.chrome}
URL='http://codingbat.com'
LANG='python' # you can specify java also

# Find all section links and store them in urls list
try:
    data = requests.get(URL+'/'+LANG,headers=header)
except requests.exceptions.ConnectionError:
    print("Error establishing connection")
    exit()
soup=BeautifulSoup(data.content,'lxml')
links=[div.a['href'] for div in soup.find_all('div',class_='summ')]
urls=[URL+'/'+LANG+"/"+link.split('/')[-1] for link in links]

#Traversing all the section urls and store all the questions url in questions list
question_urls=[]
for url in urls:
	data = requests.get(url,headers=header)
	soup=BeautifulSoup(data.content,'lxml')
	questions=[question.td.a['href']for question in soup.find('div',class_='tabin').find('table').find_all('tr')]
	for question in questions:
		question_urls.append(URL+question)
		
#Traversing all the question urls and store the questions in problem_list
questions=[]
for url in question_urls:
	data = requests.get(url,headers=header)
	soup=BeautifulSoup(data.content,'lxml')
	a=soup.find('div',class_='minh')
	questions.append(a.text)

for question in questions:
	print question
					   
	
	



		
		
    
	
	
	

	



