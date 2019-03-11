import xlrd
from enginecode.processor.database import DatabaseManager
import datetime
from PySide2 import QtCore

PROVIDERS = ('ARTEC', 'MONTENEGRO', 'AUDITOR')


class ProcessorThread(QtCore.QThread):
    updateProgress = QtCore.Signal(int)
    setMaximum = QtCore.Signal(int)

    def __init__(self, file_url):
        QtCore.QThread.__init__(self)
        self.database_manager = DatabaseManager()
        self.file_url = file_url

    def __del__(self):
        self.wait()

    def run(self):
        if PROVIDERS[0] in self.file_url:
            artec_price_list = self.open_worksheet(self.file_url, PROVIDERS[0])
            self.load_database(artec_price_list)
        elif PROVIDERS[1] in self.file_url:
            montenegro_price_list = self.open_worksheet(self.file_url, PROVIDERS[1])
            self.load_database(montenegro_price_list)
        elif PROVIDERS[2] in self.file_url:
            auditor_price_list = self.open_worksheet(self.file_url, PROVIDERS[2])
            self.load_database(auditor_price_list)
        print "Finished Run"

    def open_worksheet(self, dir_file, provider):
        workbook = xlrd.open_workbook(dir_file)
        sheet = workbook.sheet_by_index(0)
        dict_list = []
        if provider == PROVIDERS[0]:
            for row_index in xrange(1, sheet.nrows):
                code = sheet.cell(row_index, 0).value.encode('utf-8')
                description = sheet.cell(row_index, 1).value.encode('utf-8')
                list_price = self.parse_price(sheet.cell(row_index, 2).value.encode('utf-8'), PROVIDERS[0])
                d = {"Code": code,
                     "Description": description,
                     "ProviderPrice": list_price,
                     "Provider": provider,
                     "Category": " - ",
                     "Updated": str(datetime.datetime.today())}
                dict_list.append(d)
        elif provider == PROVIDERS[1]:
            for row_index in xrange(3, sheet.nrows):
                if sheet.cell(row_index, 0).value.encode('utf-8') != '' and \
                        sheet.cell(row_index, 2).value.encode('utf-8') != '':
                    code = sheet.cell(row_index, 0).value.encode('utf-8')
                    description = sheet.cell(row_index, 2).value.encode('utf-8')
                    list_price = sheet.cell(row_index, 4).value
                    d = {"Code": code,
                         "Description": description,
                         "ProviderPrice": list_price,
                         "Provider": provider,
                         "Category": " - ",
                         "Updated": str(datetime.datetime.today())}
                    dict_list.append(d)
        elif provider == PROVIDERS[2]:
            for row_index in xrange(10, sheet.nrows):
                if str(sheet.cell(row_index, 0).value).encode('utf-8') != '' and \
                        sheet.cell(row_index, 1).value.encode('utf-8') != '':
                    code = str(sheet.cell(row_index, 0).value).encode('utf-8').replace(".0", "")
                    description = sheet.cell(row_index, 1).value.encode('utf-8')
                    list_price = sheet.cell(row_index, 6).value
                    # category = sheet.cell(row_index, 0).value.encode('utf-8')
                    d = {"Code": code,
                         "Description": description,
                         "ProviderPrice": list_price,
                         "Provider": provider,
                         "Category": " - ",
                         "Updated": str(datetime.datetime.today())}
                    dict_list.append(d)
        return dict_list

    def parse_price(self, price, provider):
        if provider == PROVIDERS[0]:
            return float(price.split('$ ')[1].replace(',', '.'))
        elif provider == PROVIDERS[1]:
            return price.replace(",", '.')

    def load_database(self, price_list_dict):
        configuration = self.database_manager.get_coeficients()
        minorist_coef = float(configuration[0])
        mayorist_coef = float(configuration[1])
        self.setMaximum.emit(len(price_list_dict))
        counter = 0
        for dict in price_list_dict:
            sql_consult = self.database_manager.consult_data_code(dict['Code'])
            description = dict['Description']
            code = dict['Code']
            provider_price = "%.2f" % dict["ProviderPrice"]
            if dict["Provider"] == PROVIDERS[2]:
                minorist_price = float(dict["ProviderPrice"]) * 1.21 * 0.85 * minorist_coef
                mayorist_price = float(dict["ProviderPrice"]) * 1.21 * 0.85 * mayorist_coef
            else:
                minorist_price = float(dict["ProviderPrice"]) * minorist_coef
                mayorist_price = float(dict["ProviderPrice"]) * mayorist_coef
            category = dict['Category']
            if sql_consult is None:
                self.database_manager.load_new_product(description,
                                                       code,
                                                       category,
                                                       provider_price,
                                                       "%.2f" % minorist_price,
                                                       "%.2f" % mayorist_price,
                                                       1,
                                                       dict["Provider"],
                                                       dict["Updated"])
            else:
                self.database_manager.update_product(sql_consult[0], description, code,
                                                     category,
                                                     provider_price,
                                                     "%.2f" % minorist_price,
                                                     "%.2f" % mayorist_price,
                                                     1,
                                                     dict["Provider"],
                                                     dict["Updated"])
            counter += 1
            self.updateProgress.emit(counter)

