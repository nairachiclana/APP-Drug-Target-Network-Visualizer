from chembl_webresource_client.new_client import new_client
import csv
import mysql.connector
import pandas
import networkx as nx
import matplotlib.pyplot as plt
import os
import plotly
import plotly.graph_objs as go
import graphviz
import pygraphviz


mydb = mysql.connector.connect(host="localhost", user="root", passwd='nairapass',database="rnvdb")



"""
Codigo que interactua con front-end para seleccionar la lista de targets o drugs de la base de datos.
"""


def get_list_from_DB(table_name):
    res = list()
    query = "SELECT chembl_id from " + table_name;
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myres = mycursor.fetchall()
    for i in range(1, len(myres)):
        res.append(myres[i][0])
    mycursor.close()
    return res


"""""
get_info_from_cheml recibe como primer parametro una lista con tagets(proteina) y como segundo una lista con farmacos
"""""


def get_info_from_chembl(name_target, name_drug, targets, drugs):

    activity = new_client.activity.filter(target_chembl_id__in=targets
                                          , molecule_chembl_id__in=drugs
                                          , pchembl_value__gte=6).only('molecule_pref_name', 'target_pref_name', 'pchembl_value')

    filename = os.path.join(os.path.dirname(__file__), '../data/interactions_' + name_target +'_'+name_drug+'.csv')

    with open(filename, 'w') as f:
        fieldnames = ['drug', 'target', 'pchembl_value']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        [writer.writerow({'drug': element['molecule_pref_name'], 'target': element['target_pref_name'],
        'pchembl_value': element['pchembl_value']}) for element in activity]


def print_graph_plotly(filename):

    plotly.tools.set_credentials_file(username='javimoreno96', api_key='koRb58Db0YrlUN9Y3MKf')

    # Building df
    print(filename)
    mydata = pandas.read_csv('../data/'+filename, sep=',')
    mydata = mydata.drop_duplicates(subset=['drug', 'target'])

    print("mydata:", mydata)

    # Building graph
    mygraph = nx.from_pandas_edgelist(mydata, source='drug', target='target', edge_attr='pchembl_value')

    nodes = nx.nodes(mygraph)
    edges = nx.edges(mygraph)
    print("mygraphNodes:",nodes)
    print("mygraphEdges:", edges)

    pos = nx.nx_pydot.graphviz_layout(mygraph)


    Xnod = [pos[node][0] for node in nodes]
    Ynod = [pos[node][1] for node in nodes]
    Xed = []
    Yed = []

    i = 0

    print("for")
    for edge in edges:
        source, target = edge
        Xed += [pos[source][0], pos[target][0], None]
        Yed += [pos[source][1], pos[target][1], None]
        i = i + 1

    print("edge_Trace")
    edge_trace = go.Scatter(
        x=Xed,
        y=Yed,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    print("node_names")
    node_names = list()
    [node_names.append(name) for name in nodes]
    node_trace = go.Scatter(
        x=Xnod,
        y=Ynod,
        mode='markers',
        name='net',
        text=node_names,
        hoverinfo='text',
        marker=dict(symbol='circle-dot',
                    size=5,
                    color='#6959CD',
                    line=dict(color='rgb(50,50,50)', width=0.5)
                    ))

    print("data1")
    data1 = [edge_trace, node_trace]
    layout = go.Layout(showlegend=True)
    fig1 = go.Figure(data=data1, layout=layout)

    plotlydiv = plotly.offline.plot(fig1, filename="dibujillo.html", auto_open=False, output_type='div', include_plotlyjs=False,)
    return(plotlydiv)


"""
Extrae informacion de una proteina o farmaco de chembl a partir de un nombre que recibe como parametro.
Devuelve el resultado en como objeto dict que se puede manejar con json al paso.
"""


def extract_info_from_name(name):
    # Comprobamos si el nombre corresponde a un medicamento
    res = new_client.molecule.filter(pref_name__icontains=name).only('pref_name', 'atc_classifications',
                                                                     'molecule_chembl_id', 'first_approval',
                                                                     'max_phase', 'molecule_synonyms',
                                                                     'molecule_properties')

    # En caso contrario, comprobamos si corresponde a una proteina
    if len(res) == 0:
        res = new_client.target.filter(pref_name__icontains=name).only('pref_name', 'target_chembl_id', 'organism',
                                                                       'target_type')

    return res[0]




"""



def insert_table(filename):
    if 'target' or 'drug' in filename:

        csv_file_path = str(filename)
        csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_path)

        # Building df
        mydata = pandas.read_csv(filepath_or_buffer=csv_file_path, sep=',')

        if {'chembl_id', 'name'}.issubset(mydata.columns):
            table_name = filename[0: filename.find(".")]


            cursor1=mydb.cursor()
            query_delete = "drop table  if exists `"+table_name+"`"
            cursor1.execute(query_delete)
            cursor1.close()

            query_create = "CREATE TABLE `"+table_name+"` (  `chembl_id` text,  `name` text) ENGINE=InnoDB DEFAULT CHARSET=latin1;"
            cursor2 = mydb.cursor()
            cursor2.execute(query_create)
            cursor2.close()

            try:
                cursor3=mydb.cursor()
                query=" INSERT INTO `"+table_name+ "`(`chembl_id`, `name`) VALUES (%s,%s)"
                subset = mydata[['chembl_id', 'name']]
                tuples = [tuple(x) for x in subset.values]
                cursor3.executemany(query,tuples)
                mydb.commit()
                cursor3.close()
            except mysql.connector.Error as error:
                print("Failed inserting record into python_users table {}".format(error))

        else:
            print("chiquillo debes poner los siguientes nombres a las columnas : 'chembl_id', 'name' ")
    else:
            print("el archivo .csv debe contener en el nombre la palabra drug o target")



"""

"""
id_drugs=get_list_from_DB('antineoplasic_drugs')
id_targets=get_list_from_DB('brca_targets')

pchembl_info=get_info_from_chembl('brca_targets', 'brca_targets', id_targets, id_drugs)

print_graph_plotly('interactions_brca_targets_antineoplasic_drugs.csv')
"""




