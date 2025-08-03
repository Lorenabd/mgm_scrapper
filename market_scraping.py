# MGM MARKET
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import regex as re
import csv
from selenium.webdriver.common.by import By
from lxml import html
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from pop_up_continue import WindowContinue


class ScrapingMarket:
    def __init__(self, main_driver, file_output_name):
        self.main_driver = main_driver
        self.file_output_name = file_output_name
        self.config = self.read_json("./variables.json")
        self.window_continue = WindowContinue()
        self.get_data()

    def read_json(self, variables_file):
        with open(variables_file, "r") as file:
            config = json.load(file)
        return config

    def continue_scrapping(self):
        result = self.window_continue.get_result()
        if result is None:
            print("Extraction finished.")
        else:
            print(f"Scraping next category into “{result}”…")
            self.file_output_name = result
            self.get_data()

    def get_data(self):
        last_page = False
        primera_vez = True

        while True:
            old_text = self.main_driver.find_element(
                By.XPATH,
                "/html/body/div/div/main/div[2]/div[2]/div/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]",
            ).text
            print(old_text)
            path_expression = self.main_driver.find_element(
                By.XPATH,
                "html/body/div/div/main/div[2]/div[2]/div/div/div/div[3]/div[2]/div/div",
            )
            childs_elements = path_expression.find_elements(
                By.CLASS_NAME, "product-item"
            )
            primer_scraping = True

            for row in childs_elements:
                matches = row.find_element(By.CLASS_NAME, "name").text
                print(matches)
                matches_user = row.find_element(
                    By.CLASS_NAME, "vendor-name"
                ).text.split()[-1]
                print(matches_user)
                try:
                    self.main_driver.find_element(By.XPATH, "//li[a[@rel='next']]")
                    print("el boton next esta presente")
                except NoSuchElementException:
                    print("se esta procesando la ultima pagina o solo hay una")
                    last_page = True
                print(
                    f"lista de usuarios guardados hasta ahora: {self.config['user_info']['user']}"
                )

                if matches not in self.config["textos"]["not_complete"]:
                    self.config["textos"]["not_complete"].append(matches)
                    boton = row.find_element(By.XPATH, ".//a[@class='thumb']")
                    self.main_driver.execute_script(
                        "arguments[0].scrollIntoView();", boton
                    )
                    ActionChains(self.main_driver).key_down(Keys.CONTROL).click(
                        boton
                    ).key_up(Keys.CONTROL).perform()
                    windows = self.main_driver.window_handles
                    self.main_driver.switch_to.window(windows[-1])
                    try:
                        WebDriverWait(self.main_driver, 60).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[1]/div/main/div[2]/div[2]/div/div[1]/div/div[1]/div/div/figure/a/img",
                                )
                            )
                        )
                        print("pagina actualizada")
                        try:
                            if primer_scraping:
                                print("cogiendo mercado")
                                mercado = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div[1]/div/main/div[2]/div[1]/div/div/a[4]",
                                ).text
                                print(mercado)
                                primer_scraping = False

                            full_product_name = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div[1]/div/main/div[2]/div[2]/div/div[1]/div/div[2]/div/h1",
                            ).text
                            print(full_product_name)

                            price_product = self.main_driver.find_element(
                                By.XPATH, "//div/span[1]/strong"
                            ).text
                            print(price_product)
                            time.sleep(1)
                            product_type = self.main_driver.find_element(
                                By.XPATH,
                                "//span[contains(text(), '- Product Type:')]/following-sibling::span[contains(@class, 'c-badge')]",
                            ).text
                            print(product_type)
                            total_sales_product = self.main_driver.find_element(
                                By.XPATH, "//div[2]/div/span[2]"
                            ).text.split()[0]
                            print(total_sales_product)
                            try:
                                origen = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div[1]/div/main/div[2]/div[2]/div/div[1]/div/div[2]/div/form/div[5]/div/div[1]/ul/li[2]/span[2]",
                                ).text
                                print(origen)
                            except Exception as e:
                                print(f"Error: {e}")
                                origen = "None"
                            time.sleep(1)
                            self.main_driver.close()
                            self.main_driver.switch_to.window(windows[0])
                        except Exception as e:
                            print(f"Error: {e}")
                            self.main_driver.close()
                            self.main_driver.switch_to.window(windows[0])

                        print("vuelta al principal")
                        if not last_page:
                            WebDriverWait(self.main_driver, 60).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//li[a[@rel='next']]")
                                )
                            )

                        if matches_user not in self.config["user_info"]["user"]:
                            print("entrando en perfil usuario")
                            boton_user_profile = row.find_element(
                                By.CLASS_NAME, "vendor-name"
                            )
                            href = row.find_element(
                                By.CLASS_NAME, "vendor-name"
                            ).get_attribute("href")
                            print("Enlace al perfil del usuario:", href)
                            ActionChains(self.main_driver).key_down(Keys.CONTROL).click(
                                boton_user_profile
                            ).key_up(Keys.CONTROL).perform()
                            windows = self.main_driver.window_handles
                            self.main_driver.switch_to.window(windows[-1])
                            time.sleep(4)
                            WebDriverWait(self.main_driver, 200).until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        "/html/body/div/div/main/div[2]/div[1]/div/h1",
                                    )
                                )
                            )

                            try:
                                join_date_user = (
                                    self.main_driver.find_element(
                                        By.XPATH,
                                        "/html/body/div/div/main/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/p[2]",
                                    )
                                    .text.split(":")[-1]
                                    .strip()
                                )
                                print(join_date_user)
                                user_level = (
                                    self.main_driver.find_element(
                                        By.XPATH,
                                        "/html/body/div/div/main/div[2]/div[2]/div/div[1]/div/div[2]/span[1]",
                                    )
                                    .text.split(" ")[-1]
                                    .split(".")[-1]
                                )
                                print(user_level)
                                completed_orders = (
                                    self.main_driver.find_element(
                                        By.XPATH,
                                        "/html/body/div/div/main/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/p[1]",
                                    )
                                    .text.split(":")[-1]
                                    .strip()
                                )
                                print(completed_orders)

                                user_rating = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[1]/div/div[2]/p/span[4]",
                                ).text.split(":")[-1]
                                print(user_rating)

                                total_orders = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[1]/div/div[2]/p/span[3]",
                                ).text.split(":")[-1]
                                print(total_orders)
                                wait = WebDriverWait(self.main_driver, 10)
                                positive_feedback = wait.until(
                                    EC.presence_of_element_located(
                                        (
                                            By.XPATH,
                                            "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[2]/div/div[1]/div",
                                        )
                                    )
                                )
                                self.main_driver.execute_script(
                                    "arguments[0].scrollIntoView();", positive_feedback
                                )
                                positive_feedback = positive_feedback.text.split(" ")[0]
                                print(positive_feedback)

                                neutral_feedback = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[2]/div/div[2]/div",
                                ).text.split(" ")[0]
                                print(neutral_feedback)

                                negative_feedback = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[2]/div/div[3]/div",
                                ).text.split(" ")[0]
                                print(negative_feedback)

                                quality_user = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[1]/div[1]/div[2]/span",
                                ).text.split(" ")[0]
                                print(quality_user)

                                shipping_user_rating = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[1]/div[3]/div[2]/span",
                                ).text.split(" ")[0]
                                print(shipping_user_rating)

                                communication_user_rating = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div/main/div[2]/div[2]/div/div[5]/div/div[1]/div[2]/div[2]/span",
                                ).text.split(
                                    " "
                                )[
                                    0
                                ]
                                print(communication_user_rating)

                                print("ha encontrado todo lo de users")
                                time.sleep(1)
                                self.main_driver.close()
                                self.main_driver.switch_to.window(windows[0])
                            except Exception as e:
                                print(f"Error: {e}")
                                self.main_driver.close()
                                self.main_driver.switch_to.window(windows[0])
                                print("FALLO EN USER DATA")
                                break

                            self.config["user_info"]["data_join_year_user"][
                                matches_user
                            ] = join_date_user
                            self.config["user_info"]["data_user_level"][
                                matches_user
                            ] = user_level
                            self.config["user_info"]["orders"]["data_completed_orders"][
                                matches_user
                            ] = completed_orders
                            self.config["user_info"]["rating"]["data_user_rating"][
                                matches_user
                            ] = user_rating
                            self.config["user_info"]["orders"]["data_total_orders"][
                                matches_user
                            ] = total_orders
                            self.config["feedback_info"]["data_positive_feedback"][
                                matches_user
                            ] = positive_feedback
                            self.config["feedback_info"]["data_neutral_feedback"][
                                matches_user
                            ] = neutral_feedback
                            self.config["feedback_info"]["data_negative_feedback"][
                                matches_user
                            ] = negative_feedback
                            self.config["quality_info"]["data_quality_user"][
                                matches_user
                            ] = quality_user
                            self.config["quality_info"]["data_shipping_user_rating"][
                                matches_user
                            ] = shipping_user_rating
                            self.config["quality_info"][
                                "data_communication_user_rating"
                            ][matches_user] = communication_user_rating

                            self.config["user_info"]["join_year_user"].append(
                                join_date_user
                            )
                            self.config["user_info"]["user_level"].append(user_level)
                            self.config["user_info"]["orders"]["completed"].append(
                                completed_orders
                            )
                            self.config["user_info"]["rating"]["user_rating"].append(
                                user_rating
                            )
                            self.config["user_info"]["orders"]["total"].append(
                                total_orders
                            )
                            self.config["feedback_info"][
                                "list_positive_feedback"
                            ].append(positive_feedback)
                            self.config["feedback_info"][
                                "list_neutral_feedback"
                            ].append(neutral_feedback)
                            self.config["feedback_info"][
                                "list_negative_feedback"
                            ].append(negative_feedback)
                            self.config["quality_info"]["quality_user_rating"].append(
                                quality_user
                            )
                            self.config["quality_info"]["shipping_user_rating"].append(
                                shipping_user_rating
                            )
                            self.config["quality_info"][
                                "communication_user_rating"
                            ].append(communication_user_rating)
                        else:
                            self.config["user_info"]["join_year_user"].append(
                                self.config["user_info"]["data_join_year_user"].get(
                                    matches_user
                                )
                            )
                            self.config["user_info"]["user_level"].append(
                                self.config["user_info"]["data_user_level"].get(
                                    matches_user
                                )
                            )
                            self.config["user_info"]["orders"]["completed"].append(
                                self.config["user_info"]["orders"][
                                    "data_completed_orders"
                                ].get(matches_user)
                            )
                            self.config["user_info"]["rating"]["user_rating"].append(
                                self.config["user_info"]["rating"][
                                    "data_user_rating"
                                ].get(matches_user)
                            )
                            self.config["user_info"]["orders"]["total"].append(
                                self.config["user_info"]["orders"][
                                    "data_total_orders"
                                ].get(matches_user)
                            )
                            self.config["feedback_info"][
                                "list_positive_feedback"
                            ].append(
                                self.config["feedback_info"][
                                    "data_positive_feedback"
                                ].get(matches_user)
                            )
                            self.config["feedback_info"][
                                "list_neutral_feedback"
                            ].append(
                                self.config["feedback_info"][
                                    "data_neutral_feedback"
                                ].get(matches_user)
                            )
                            self.config["feedback_info"][
                                "list_negative_feedback"
                            ].append(
                                self.config["feedback_info"][
                                    "data_negative_feedback"
                                ].get(matches_user)
                            )
                            self.config["quality_info"]["quality_user_rating"].append(
                                self.config["quality_info"]["data_quality_user"].get(
                                    matches_user
                                )
                            )
                            self.config["quality_info"]["shipping_user_rating"].append(
                                self.config["quality_info"][
                                    "data_shipping_user_rating"
                                ].get(matches_user)
                            )
                            self.config["quality_info"][
                                "communication_user_rating"
                            ].append(
                                self.config["quality_info"][
                                    "data_communication_user_rating"
                                ].get(matches_user)
                            )

                        self.config["user_info"]["user"].append(matches_user)
                        self.config["textos"]["all"].append(full_product_name)
                        self.config["market_info"]["precio"].append(price_product)
                        self.config["market_info"]["tipo_producto"].append(product_type)
                        self.config["sales_info"]["total_sales_producto"].append(
                            total_sales_product
                        )
                        self.config["place_info"]["lugar"].append(origen)
                        self.config["market_info"]["especializado"].append(mercado)
                    except Exception as e:
                        print(f"Error: {e}")
                        self.main_driver.close()
                        self.main_driver.switch_to.window(windows[0])
                else:
                    print(f"El producto {matches} está duplicado")

            try:

                if primera_vez:
                    primera_vez = False
                    try:
                        next_li = self.main_driver.find_element(
                            By.XPATH, "//li[a[@rel='next']]"
                        )
                        print(
                            "se ha encontrado el boon next comprobando si esta disables"
                        )
                        if "disabled" in next_li.get_attribute("class"):
                            print("se esta procesando la ultima pagina o solo hay una")
                            last_page = True
                    except NoSuchElementException:
                        print("solo hay una pagina")
                        break

                if last_page:
                    print("SE HA FINALIZADO EL SCRAPING")
                    break
                next_page = WebDriverWait(self.main_driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "//li[a[@rel='next']]"))
                )
                next_page = WebDriverWait(self.main_driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[a[@rel='next']]"))
                )
                previous_url = self.main_driver.current_url
                print("Intentando hacer clik en NEXT...")
                next_page.click()
                print("Click en NEXT")
                WebDriverWait(self.main_driver, 200).until(
                    lambda driver: driver.current_url != previous_url
                )
                print("ha cambiado la url")
                print(
                    self.main_driver.find_element(
                        By.XPATH,
                        "/html/body/div/div/main/div[2]/div[2]/div/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]",
                    ).text
                )
                print("ha cambiado el contenido")
                print("Siguiente página cargada correctamente")
                next_page = WebDriverWait(self.main_driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "//li[a[@rel='next']]"))
                )
                print("ha aparecido el siguiente next")
                next_li = self.main_driver.find_element(
                    By.XPATH, "//li[a[@rel='next']]"
                )
                print("se ha encontrado el boon next comprobando si esta disables")
                if "disabled" in next_li.get_attribute("class"):
                    print("se esta procesando la ultima pagina o solo hay una")
                    last_page = True
            except:
                print("No hay mas páginas disponibles")
                break

        df_data_extracted = pd.DataFrame(
            {
                "Name Product": self.config["textos"]["all"],
                "Seller": self.config["user_info"]["user"],
                "Origin": self.config["place_info"]["lugar"],
                "Price": self.config["market_info"]["precio"],
                "Specialized market": self.config["market_info"]["especializado"],
                "Total sales product": self.config["sales_info"][
                    "total_sales_producto"
                ],
                "User Rating": self.config["user_info"]["rating"]["user_rating"],
                "Join date": self.config["user_info"]["join_year_user"],
                "User level": self.config["user_info"]["user_level"],
                "Completed orders user": self.config["user_info"]["orders"][
                    "completed"
                ],
                "Total user orders": self.config["user_info"]["orders"]["total"],
                "Positive feedback": self.config["feedback_info"][
                    "list_positive_feedback"
                ],
                "Neutral feedback": self.config["feedback_info"][
                    "list_neutral_feedback"
                ],
                "Negative feedback": self.config["feedback_info"][
                    "list_negative_feedback"
                ],
                "Quality user rating": self.config["quality_info"][
                    "quality_user_rating"
                ],
                "Shipping user rating": self.config["quality_info"][
                    "shipping_user_rating"
                ],
                "Communication user rating": self.config["quality_info"][
                    "communication_user_rating"
                ],
            }
        ).sort_values(by="Seller")
        os.makedirs("DATA_EXTRACTED", exist_ok=True)
        df_data_extracted.to_csv(
            os.path.join("DATA_EXTRACTED", f"{self.file_output_name}.csv"),
            index=False,
            sep=",",
        )
        self.continue_scrapping()
