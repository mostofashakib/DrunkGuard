import string
import random
import requests, os, sys, tempfile, subprocess, base64, time
import GetAddress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def CallUber_Run():

    # initial parameter

    email_list = "xyz@gmail.com"
    password = "Your_Password"
    location = "Your home location"

    # get the path of ChromeDriverServer

    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options, executable_path= r"chromedriver.exe")
    Request_driver = webdriver.Chrome(options=options, executable_path= r"chromedriver.exe")

    # create a new Chrome session
    driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://auth.uber.com/login/")

    Request_driver.get("https://m.uber.com/looking?_ga=2.72958036.694223225.1583663335-669399475.1583663335")

    # connect to your account

    button1 = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/form/div/div[1]/div/input")
    button1.click()
    button1.send_keys(email_list)
    button2 = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/form/button")
    button2.click()

    button3 = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/input[2]")
    button3.click()
    button3.send_keys(password)
    button4 = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/button")
    button4.click()

    print("Requesting your Uber ride")

    button5 = Request_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[1]/div/input")
    button5.click()
    button5.send_keys(GetAddress.GetAddress_Run())
    button6 = Request_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[1]")
    button6.click()

    button7 = Request_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[1]/div/input")
    button7.click()
    button7.send_keys(location)
    button6 = Request_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]")
    button6.click()

    #infinite loop

    driver.quit()

    result = "John will pick you up in 5 mins with a green Toyota Prius from " + GetAddress.GetAddress_Run()

    return result