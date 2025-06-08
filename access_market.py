from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import html
from market_scraping import ScrapingMarket
import os
from PyQt5.QtGui import QIcon, QFont



class AccessMarket():
    def __init__(self):
        options=self.set_options()
        self.execute_browser(options)
        
    def set_options(self):
        options = Options()
        options.binary_location=f"{os.getenv('BROWSER')}/tor-browser/Browser/firefox"
        options.set_preference("network.proxy.type",1)
        options.set_preference("network.proxy.socks","127.0.0.1")
        options.set_preference("network.proxy.socks_port",9051)
        options.set_preference("network.proxy.socks_remote_dns",True)
        options.set_preference("javascript.enabled",False)
        return options
        
    def execute_browser(self,options):
        main_driver = webdriver.Firefox(options=options)
        connect_button = main_driver.find_element(By.XPATH,'//*[@id="connectButton"]')
        connect_button.click()
        print("conect button clicked")
        time.sleep(5)
        url="https://ngemgrlhmdqi3zsgscjgjrbwpietxf3kbwjfzrarb4h6f3nimjsiu7yd.top/signin" #MGM MARKET
        main_driver.get(url)
        WebDriverWait(main_driver,300).until(
                        EC.url_to_be("https://ngemgrlhmdqi3zsgscjgjrbwpietxf3kbwjfzrarb4h6f3nimjsiu7yd.top/") #wait 5 mins for user identification + phising tests
        )

        WebDriverWait(main_driver,300).until(
                        EC.presence_of_element_located((By.XPATH,'/html/body/div/div/main/div[2]/div/div/div/h2')) #wait 5 mins for user identification + phising tests
        )
        self.pop_up_info(main_driver)
        
    def pop_up_info(self,main_driver):
        app = QApplication(sys.argv)
        ventana = QWidget()
        ventana.setWindowTitle('Important Information!')
        ventana.setStyleSheet("QWidget { font-size: 20px; }")

        ventana.setWindowIcon(QIcon("./icon.png"))  

        mensaje = QLabel("Navigate to the category where you want to start\n scrapping and press CONTINUE to start.")
        boton_continuar = QPushButton('Continue')

        mensaje.setFont(QFont("Arial", 14)) 
        boton_continuar.setFont(QFont("Arial", 12))  

        boton_continuar.clicked.connect(lambda: self.close_pop_up_info(ventana, main_driver))

        layout = QVBoxLayout()
        layout.addWidget(mensaje)
        layout.addWidget(boton_continuar)

        ventana.setLayout(layout)


        ventana.resize(400, 200)

        ventana.show()
        app.exec_()
        
    def close_pop_up_info(self,ventana,main_driver):
        ventana.close()
        print("Comenzando a scrapear...")
        ScrapingMarket(main_driver)
 
if __name__ == "__main__":
    market = AccessMarket()
