# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:04:10 2017

@author: BLK
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import timedelta
from datetime import datetime
import json
import random
import pickle
import requests
import csv
import os


os.chdir("z://Documents/Script/anmeldelsesscraper")
date = datetime.now()
today=str(date.day)+"."+str(date.month)

user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(chrome_options=options)


def scroll(item, x=0, y=0):
       driver.execute_script("window.scrollTo("+str(item.location_once_scrolled_into_view['x']+x)+","+str(item.location_once_scrolled_into_view['y']+y)+");")

gamerlinks = []
try:
       gamerlinks=json.load(open("gamerlinks.txt","r"))
       print("links loaded")
except:
       print("links not loaded")

def gamerhref():
       
       side=1
       driver.get("https://www.gamer.no/anmeldelser?type=products&sortBy=tek_review_published&sortDir=desc&limit=10&timespan=all")
       WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.LINK_TEXT,"Side "+str(side))))
       
       while len(driver.find_elements_by_link_text("Side "+ str(side))) > 0:
              lenker = driver.find_elements_by_link_text("Les hele anmeldelsen")
              for i in lenker:
                     if i.get_attribute("href") not in gamerlinks:
                            gamerlinks.append(i.get_attribute("href"))
              side += 1
              if len(driver.find_elements_by_link_text("Side "+ str(side)))>0:
                    next = driver.find_element_by_link_text("Side "+ str(side))
                    scroll(next)
                    next.click()
gamer = {}
try:
       gamer= json.load(open("gametekst.txt","r"))
       
def getGameTekst(url):
       global driver
       
       try:
              driver.get(url)
       except TimeoutException:
              driver.quit()
              driver = webdriver.Chrome(chrome_options=options)
              driver.get(url)
              
       
       global gamer2
       if len(driver.find_elements_by_link_text("Vis alle"))>0:
              visalle=driver.find_element_by_link_text("Vis alle" )
              scroll(visalle)
              vurl=visalle.get_attribute("href")
              driver.get(vurl)
       
       gameTittel = driver.find_element_by_tag_name("h1").text
#       if gameTittel not in gamer:
       gamer2.setdefault(gameTittel,[])
       try:
              intro= driver.find_element_by_class_name("headline").text
       except:
              intro= driver.find_element_by_tag_name("h2").text
       anmeldtekst =  ""
       for i in driver.find_element_by_xpath("//* [@class='text clearfix']").find_elements_by_tag_name("p"):
              if len(i.find_elements_by_tag_name("em")) > 0:
                     pass
              elif len(i.find_elements_by_tag_name("b")) >0:
                     pass
              else:
                     anmeldtekst += i.text
       try:
              karakter = int(driver.find_element_by_xpath('//*[@itemprop="ratingValue"]').text)
       except:
              try:
                     karakter= int(driver.find_element_by_class_name('score-data').text[0])
              except:
                    karakter = "NA"
       if karakter == "NA":
              score="NA"
       else:
              score= (karakter/10)*100
       gamer2[gameTittel]=[intro+" "+anmeldtekst,karakter,score, "Spill" ]
       


presslinks = []
try:
       presslinks=json.load(open("presslinks.txt","r"))
       print("links loaded")
except:
       print("links not loaded")
def getPressLinks():
       side=1
       driver.get("http://www.pressfire.no/anmeldelser")
       while len(driver.find_elements_by_link_text(str(side))) <= 129:
              for i in driver.find_elements_by_class_name("search_result"):
                     a= i.find_element_by_tag_name("a")
                     if a.get_attribute("href") not in presslinks:
                            presslinks.append(a.get_attribute("href"))
              print(side)
              side+=1
              if len(driver.find_elements_by_link_text(str(side))) > 0:
                     try:
                            neste = driver.find_element_by_link_text(str(side))
                            scroll(neste)
                            neste.click()
                     except:
                            neste = driver.find_element_by_link_text(">")
                            scroll(neste)
                            neste.click()
                            
                            
                     
press= {}

def getPressTekst(url):
       global driver
       try:       
              driver.get(url)
       except TimeoutException:
              driver.quit()
              driver = webdriver.Chrome(chrome_options=options)
              driver.get(url)
       side = "Press Fire"       
       navn = driver.find_element_by_xpath('//*[@id="article"]/h1').text
       
       tekst = ""
       for i in driver.find_element_by_id("article_body").find_elements_by_tag_name("p"):
              tekst += i.text
       try:
             karakter = int(driver.find_element_by_class_name("game-dice").get_attribute("alt")[-1])
       except:
              karakter= "NA"
              
       if karakter == "NA":
              score = "NA"
       else:
              
              score = round((karakter / 6)*100,2)
       press.setdefault(navn,[])
       press[navn]=[tekst,karakter,score,"Spill"]
       
       


def getText(liste, funksjon, index=0):
       a=index
       for i in liste[index:-1]:
              a+=1
              print("scraping ",i,a,"of ", len(liste))
              funksjon(i)