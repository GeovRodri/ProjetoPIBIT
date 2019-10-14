import csv
import json
from pprint import pprint
from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from utils import Utils


class PricesDriver(object):

    driver = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

    def get_price(self, url):
        titles, data = [], {}
        instances, instances_keys = [], []

        self.driver.get(url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        tables = self.driver.find_elements_by_xpath("//table//th[contains(text(),'Machine type')]/../../..")

        """ Pegando o select de seleção de localização """
        localizations, locations = self.get_options_localization()

        for localization in localizations:
            data[localization] = []

            """ Selecionando uma opção"""
            options = self.driver.find_elements_by_xpath("//md-option//div[@class='md-text'][contains(text(),'{}')]/.."
                                                         .format(localization))
            for option in options:
                self.driver.execute_script("$('#{}').click()".format(option.get_attribute("id")))
                sleep(2)
                self.driver.execute_script("$('.md-select-backdrop').click()")

            for table in tables:
                finish = False

                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    if finish is True:
                        continue

                    tds = tr.find_elements_by_tag_name("td")

                    """ Verificando se é td(valores) ou th(titulos) """
                    if len(tds) > 0:
                        if len(tds) != 5:
                            continue

                        columns, index = {}, 0

                        for td in tds:
                            text_th = titles[index]
                            if text_th not in columns:
                                columns[text_th] = []

                            columns[text_th] = td.text
                            index += 1

                        if columns['Machine type'] is not None and columns['Price (USD)'] is not None \
                                and columns['Memory'] is not None:
                            data[localization].append(columns)

                            if columns['Machine type'] not in instances_keys:
                                columns[localization] = columns['Price (USD)']
                                instances.append(columns)
                                instances_keys.append(columns['Machine type'])
                            else:
                                index = instances_keys.index(columns['Machine type'])
                                obj = instances[index]
                                obj[localization] = columns['Price (USD)']
                    else:
                        ths = tr.find_elements_by_tag_name("th")
                        if len(ths) != 5 or ths[1].text == 'Item':
                            finish = True
                            continue

                        for th in ths:
                            if th.text not in titles:
                                titles.append(th.text)

        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        pprint(data_json)
        self.driver.close()

        with open('Google_Regions.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open('Google.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            titles.remove('Price (USD)')
            titles.remove('Preemptible price (USD)')

            w = csv.DictWriter(f, fieldnames=titles + localizations, delimiter=';')
            w.writeheader()
            for instance in instances:
                del instance['Price (USD)']
                del instance['Preemptible price (USD)']
                w.writerow(instance)

    def get_options_localization(self):
        options = []
        options_name = []

        options_page = self.driver.find_elements_by_tag_name("md-option")
        for opt in options_page:
            option = opt.find_element_by_class_name('md-text').get_attribute('innerHTML')
            if option not in options and len(option) > 0:
                options.append(option)
                options_name.append({'Name': option})

        return options, options_name


if __name__ == "__main__":
    prices_drive = PricesDriver()
    prices_drive.get_price("https://cloud.google.com/compute/pricing")
