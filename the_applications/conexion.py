import psycopg2


class selecciona_basedatos:
    @staticmethod
    def inicia_odoo():
        conexion = psycopg2.connect(user="apps", password="4pps_.Re4d0nly+", host="10.150.4.190", port="5432",
                                    database="raloy_productivo")
        return conexion

