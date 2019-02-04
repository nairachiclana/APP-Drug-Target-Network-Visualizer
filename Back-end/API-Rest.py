from flask import Flask, jsonify, abort, request, render_template
import requests
from flask_restful import Resource, Api
import mysql.connector
import json
import forms
import time
from gevent import monkey
from flask_cors import CORS


monkey.patch_all()

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nairapass'
app.config['MYSQL_DB'] = 'rnvdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


cnx=mysql.connector.connect(user='root', password='nairapass',  host='localhost', database='rnvdb')
cur=cnx.cursor()



@app.route("/")
def main():
    return render_template('../templates/main.html', reload = time.time())



@app.route('/api/chembl/<string:name_table_target>/<string:name_table_drug>' ,methods=['GET'])
def get_tables(name_table_target,name_table_drug):
    table1 =forms.get_list_from_DB(name_table_target)
    table2=forms.get_list_from_DB(name_table_drug)
    forms.get_info_from_chembl(name_table_target, name_table_drug, table1,table2)
    return("Ha funcionado. Mira el archivo generado")


@app.route('/api/graph/<string:csv_file>/' ,methods=['GET'])
def print_graph(csv_file):
    graph_div = forms.print_graph_plotly(csv_file)
    return(graph_div)


@app.route('/api/search_information/<string:id_name>', methods=['GET'])
def get_information(id_name):
    information=forms.extract_info_from_name(id_name)
    json_inf=json.dumps(information, indent=4)
    return(json_inf)


"""
Esto sirve para hacer consulta en toda la base de datos, que se traiga el nombre de todas las tablas y que te devuelva una lista con las tablas que son drugs 
y targets

@app.route('/api/tables' ,methods=['GET'])
def show_tables():
    tables=forms.show_tables()
    print(tables)
    lista_tablas_targets =list()
    lista_tablas_drugs =list()
    for i in tables:
        if 'target' in i:
            lista_tablas_drugs.append(i)
        if 'drug' in i :
            lista_tablas_targets.append(i)

    print(lista_tablas_drugs)
    print(lista_tablas_targets)
    return("")

@app.route('/api/tables/insertcsv/<string:csv_file>' ,methods=['GET'])
def insert_table_drug_or_target(csv_file):
    forms.insert_table(csv_file)
    return("")

"""

if __name__ == '__main__':
    app.run()
