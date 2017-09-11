#We learn something new in this module.
# To use pickle 
from selenium import webdriver
import time
import datastore

def start():
	url = "http://cbseresults.nic.in/class12npy/Class12th17.htm"
	roll = 6627915
	a = 1
	old_roll = roll
	data = {}
	browser = webdriver.Firefox()
	subjects = {
			'Phy'  : [], 
			'Chem' : [],
			'Bio'  : [],
			'Maths': [],
			'English' : []
			'Phy Ed' : []
		}
	try:

		while True:

			browser.get(url)
			browser.find_element_by_name("regno").clear()
			browser.find_element_by_name("regno").send_keys(str(roll))
			browser.find_element_by_name("sch").send_keys('56014')
			browser.find_element_by_name("cno").send_keys('6229')
			browser.find_element_by_name("B2").click()
			time.sleep(2)
			pagesource = browser.page_source
			#print pagesource
			time.sleep(2)
			if "Result Not" in pagesource:
				print "Not found"
				count += 1
				roll = old_roll
				a = -1
			roll += a
			if count == 2:
				break
/html/body/div/div/center/table/tbody/tr[10]/td[2]/b[1]/font			
			#store in dict
			roll_elem = browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[1]/td[2]/font")
			phy_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[4]/td[5]/font")
			eng_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[2]/td[5]/font")
			chem_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[5]/td[5]/font")
			comp_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[6]/td[5]/font")
			maths_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[3]/td[5]/font")
			phy_ed_elem = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[8]/td[5]/font")
			
			roll = str(roll_elem.text).strip()
			phy_mark = str(phy_elem.text).strip()
			eng_mark = str(eng_elem.text).strip()
			chem_mark = str(chem_elem.text).strip()
			comp_mark = str(comp_elem.text).strip()
			maths_mark = str(maths_elem.text).strip()
			phy_ed_mark = str(phy_ed_elem.text).strip()

			data[roll] = []
			data[roll].append(phy_mark, eng_mark, chem_mark\
							comp_mark, maths_mark, phy_ed_mark)

			print data
			break
			time.sleep(2)
	except Exception as e:
		print e
	finally:
		pickle_it(subjects, "SUBJECT_DICT")

start()