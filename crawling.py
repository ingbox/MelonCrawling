import time
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

login_url = 'https://member.melon.com/muid/web/login/login_informM.htm'

wd = webdriver.Chrome('C:/Users/zzzma/PycharmProjects/blog/webdriver/chromedriver.exe')

wd.get(login_url)
wd.find_element(By.NAME, 'id').send_keys('zzzmankr')
wd.find_element(By.NAME, 'pwd').send_keys('JPSkyn1204!')
wd.find_element(By.ID, 'btnLogin').click()

wait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gnb_menu"]/ul[2]/li/a/span[2]'))).click()
wait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conts"]/div[1]/ul/li[2]/a/span'))).click()

html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
total = int(int(soup.select("#totCnt")[0].string.replace(',','')) / 20)

# 파일 읽기
f = open("C:/Users/zzzma/PycharmProjects/blog/melon.csv", "w", encoding='UTF-8')
f.write("제목, 아티스트, 앨범\n")

for j in range(1, int(total/10)):
	for i in range(1, 11):
		if(i % 10 == 0):
			wait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pageObjNavgation"]/div/a[3]'))).click()
			html = wd.page_source
			soup = BeautifulSoup(html, 'html.parser')

			time.sleep(2)
		else:
			wait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="pageObjNavgation"]/div/span/a[{i}]'))).click()
			html = wd.page_source
			soup = BeautifulSoup(html, 'html.parser')

			for k in range(0, 20):
				# 제목
				title = soup.select("tr > td")[k * 8 + 2]
				try:
					filter_title = title.select('a:last-child')[0].string
				except IndexError:
					filter_title = title.select('.fc_lgray')[0].string

				# 아티스트
				artist = soup.select("tr > td")[k * 8 + 3]
				try:
					filtered_artist = artist.select('.fc_mgray')[0].string
					if (int(len(artist.select('.fc_mgray'))/2) > 1):
						for l in range(1, int(len(artist.select('.fc_mgray'))/2)):
							filtered_artist = filtered_artist + ',' + artist.select('.fc_mgray')[l].string
				except IndexError:
					filtered_artist = artist.select('.checkEllipsis')[0].string

				# 앨범
				album = soup.select("tr > td")[k * 8 + 4]
				filtered_album = album.select('.fc_mgray')[0].string

				f.write(filter_title + "," + filtered_artist + "," + filtered_album + "\n")

				print(filter_title, filtered_artist, filtered_album)

			time.sleep(2)
f.close()

while(True):
    	pass