#We learn something new in this module.
# To use pickle 
from selenium import webdriver
import time
import datastore
import json

def start():
	url = "http://cbseresults.nic.in/class12npy/Class12th17.htm"
	roll = 6627915
	a = 1
	count = 0
	old_roll = roll
	data = {}
	browser = webdriver.Firefox()
	try:

		while True:
			browser.get(url)
			time.sleep(2)
			browser.find_element_by_name("regno").clear()
			browser.find_element_by_name("regno").send_keys(str(roll))
			browser.find_element_by_name("sch").send_keys('56014')
			browser.find_element_by_name("cno").send_keys('6229')
			browser.find_element_by_name("B2").click()
			time.sleep(5)
			pagesource = browser.page_source
			if "Result Not" in pagesource:
				print "Not found"
				count += 1
				roll = old_roll
				a = -1
			elif count == 2:
				break
			else:
				#/html/body/div/div/center/table/tbody/tr[11]/td[2]/font
				#/html/body/div/div/center/table/tbody/tr[11]/td[5]/font
				#/html/body/div/div/center/table/tbody/tr[11]/td[2]/font
				#store in dict
				subname_1 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[2]/td[2]/font")
				subname_2 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[3]/td[2]/font")
				subname_3 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[4]/td[2]/font")
				subname_4 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[5]/td[2]/font")
				subname_5 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[6]/td[2]/font")
				
				subname_1 = str(subname_1.text).strip()
				subname_2 = str(subname_2.text).strip()
				subname_3 = str(subname_3.text).strip()
				subname_4 = str(subname_4.text).strip()
				subname_5 = str(subname_5.text).strip()

				subname_1_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[2]/td[5]/font")
				subname_2_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[3]/td[5]/font")
				subname_3_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[4]/td[5]/font")
				subname_4_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[5]/td[5]/font")
				subname_5_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[6]/td[5]/font")
				
				subname_1_mark = str(subname_1_mark.text).strip()
				subname_2_mark = str(subname_2_mark.text).strip()
				subname_3_mark = str(subname_3_mark.text).strip()
				subname_4_mark = str(subname_4_mark.text).strip()
				subname_5_mark = str(subname_5_mark.text).strip()
				
				if "Additional Subject" in pagesource:
					subname_6 = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[11]/td[2]/font")
					subname_6 = str(subname_6.text).strip()
					subname_6_mark = browser.find_element_by_xpath("/html/body/div/div/center/table/tbody/tr[11]/td[5]/font")
					subname_6_mark = str(subname_6_mark.text).strip()
					
				else:
					subname_6 = ""
					subname_6_mark = ""
				
				data[str(roll)] = {
						str(subname_1) : subname_1_mark, 
						str(subname_2) : subname_2_mark, 
						str(subname_3) : subname_3_mark,
						str(subname_4) : subname_4_mark,
						str(subname_5) : subname_5_mark,
						str(subname_6) : subname_6_mark,
						}

				#print data
				print json.dumps(data, indent=4)
				time.sleep(2)
				print "Here"
			roll += a
	except Exception as e:
		print "Exception", e
	finally:
		print "Here"
		with open("student_data", "w") as fh:
			json.dump(data, fh)

start()