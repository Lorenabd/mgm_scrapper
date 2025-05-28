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
        # Crear la aplicación y la ventana
        app = QApplication(sys.argv)
        ventana = QWidget()
        ventana.setWindowTitle('Ventana de Ejecución')

        # Crear los widgets
        mensaje = QLabel("Navega a la categoría donde quieres empezar a escrapear\n y presiona CONTINUAR para continuar")
        boton_continuar = QPushButton('Continuar')

        # Conectar el botón a la función de continuar
        boton_continuar.clicked.connect(lambda: self.close_pop_up_info(ventana,main_driver))

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(mensaje)
        layout.addWidget(boton_continuar)

        # Configurar la ventana
        ventana.setLayout(layout)
        ventana.setGeometry(400, 400, 300, 150)  # Establecer tamaño de la ventana

        # Mostrar la ventana
        ventana.show()

        # Ejecutar la aplicación
        app.exec_() 
        
    def close_pop_up_info(self,ventana,main_driver):
        ventana.close()
        print("Comenzando a scrapear...")
        ScrapingMarket(main_driver)
 
if __name__ == "__main__":
    market = AccessMarket()
