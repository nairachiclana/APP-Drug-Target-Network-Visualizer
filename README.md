**APP-Drug-Target-Network-Visualizer**

---
- `Back-end`: 

Contains `forms.py` with the functions of making the interactions list with pchembl value using the external database *ChEMBL*, the function of the interactive *plotly* graph, and the one which search information in *ChEMBL* from a certain name.
`API-Rest.py` contains the  *GET* methods of differents URL for the different functionalities.


- `Front-end`: 

The folder `static` has a simple CSS sheet. The folder `templates` has an unique HTML5 sheet that uses W3S tabs for using different tabs. All the parts have been modeled with *Bootstrap* (with the posibility of adding a Bootstrap stylesheet and everything with work automatically). `Utilities.js` contains the JavaScript code to obtain information from HTML, and make AJAX calls to asynchronously send the response to the client side without having to refresh all the page with every change.
