import sqlite3

DATABASE_DIRECTORY = "./../database"


class DatabaseManager(object):

    def connection(self):
        try:
            self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
            self.cursor = self.conn.cursor()
        except sqlite3.DatabaseError as error:
            print "A Database Connection Error Ocurred: ", error.args[0]

    def consult_data_code(self, code):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("SELECT id FROM _Products WHERE providerCode='" + code + "'").fetchone()
        self.conn.commit()
        self.conn.close()
        return sql_data

    def return_product_data_with_code(self, code):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("SELECT * FROM _Products WHERE providerCode='" + code + "'").fetchall()
        self.conn.commit()
        self.conn.close()
        return sql_data

    def get_coeficients(self):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("SELECT minoristCoeficient, mayoristCoeficient FROM _Configuration").fetchone()
        self.conn.commit()
        self.conn.close()
        return sql_data

    def load_new_product(self, description,
                         provider_code, category, provider_price, minorist_price, mayorist_price, quantity, provider,
                         last_update):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("INSERT INTO _Products (description,providerCode,category,providerPrice,"
                                     "minoristCalculatedCost,mayoristCalculatedCost,quantity,provider,lastTimeUpdated) "
                                     "VALUES ('"
                                     + description + "', '" +
                                     provider_code + "', '" +
                                     category + "', " +
                                     str(provider_price) + ", " +
                                     str(minorist_price) + ", " +
                                     str(mayorist_price) + ", " +
                                     str(quantity) + ", '" +
                                     provider + "', '" +
                                     last_update + "')"
                                     )
        self.conn.commit()
        self.conn.close()

    def update_product(self, id, description,
                     provider_code, category, provider_price, minorist_price, mayorist_price, quantity, provider,
                     last_update):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("UPDATE _Products SET description='" + description + "', " +
                                     "providerCode='" + provider_code + "', " +
                                     "category='" + category + "', " +
                                     "providerPrice=" + str(provider_price) + " ," +
                                     "minoristCalculatedCost=" + str(minorist_price) + ", " +
                                     "mayoristCalculatedCost=" + str(mayorist_price) + ", " +
                                     "quantity=" + str(quantity) + ", " +
                                     "provider='" + provider + "', " +
                                     "lastTimeUpdated='" + last_update + "' WHERE id=" + str(id) + "")
        self.conn.commit()
        self.conn.close()

    def nueva_compra(self, code, provider, date, products_codes):
        self.conn = sqlite3.connect(DATABASE_DIRECTORY + '/database.db')
        self.cursor = self.conn.cursor()
        sql_data = self.conn.execute("INSERT INTO _Compras (code,provider,date) \
                                     VALUES ('" + code + "','" + provider + "','" + date + "')")
        self.conn.commit()
        sql_consult_id = self.conn.execute("SELECT id FROM _Compras WHERE code='" + code + "'").fetchone()[0]
        self.conn.commit()
        for code in products_codes:
            product_id = self.conn.execute("SELECT id FROM _Products WHERE providerCode='" + code + "'").fetchone()[0]
            sql_relational = self.conn.execute("INSERT INTO _ProductsXCompra (idCompra,idProducto) \
                                           VALUES (" + str(sql_consult_id) + "," + str(product_id) + ")")
            self.conn.commit()
        self.conn.close()

    def close_connection(self):
        self.conn.close()
