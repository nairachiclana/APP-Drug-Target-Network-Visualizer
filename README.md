### APP-Drug-Target-Network-Visualizer 

---
- `Back-end`: 

Made in Python. Contains `forms.py` with the functions of making the interactions list with pchembl value using the external database *ChEMBL*, the function of the interactive *plotly* graph, and the one which search information in *ChEMBL* from a certain name.
`API-Rest.py` contains the  *GET* methods of differents URL for the different functionalities.


- `Front-end`: 

The folder `static` has a simple CSS sheet. The folder `templates` has an unique HTML5 sheet that uses W3S tabs for using different tabs. All the parts have been modeled with *Bootstrap* (with the posibility of adding a Bootstrap stylesheet and everything with work automatically). `Utilities.js` contains the JavaScript code to obtain information from HTML, and make AJAX calls to asynchronously send the response to the client side without having to refresh all the page with every change.

-`data` has some csv examples to try in the application.

- `BD_proteins_and_drugs` contiene el script SQL de creación de la BD con las tablas de proteinas y drogas disponibles.

-----

**Needed python libraries:**

- For the API: *flask, flask_resftul, mysql.connector, json, forms, gevent* and *flask_cors*.

- For the CSV and ChEMBL calls: *chembl_webresource_client.new_client, csv, mysql.connector*.

- For the interactive plotly graph: *pandas, networkx, matplotlib.pyplot, graphviz* and *pygraphviz*.
