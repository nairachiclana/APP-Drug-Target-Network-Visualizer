
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}




//ENVIAR button
 $(document).ready(function(){

     document.getElementById("defaultOpen").click();

    var show_table_button=document.getElementById('show_t_button');
    show_table_button.style.visibility='hidden';
    var search_name_textbox=document.getElementById('graph_search_textbox');
    search_name_textbox.style.visibility='hidden';

    $('#button_enviar').click(function() {

        proteinList = document.getElementById('selectProteins').value;
        drugList = document.getElementById('selectDrug').value;
        console.log('proteinlist', proteinList);
        console.log('druglist', drugList);


        //LISTS CHOOSEN IN DESPLEGABLE
        if (proteinList != "None (I will upload my own CSV)" && drugList != "None (I will upload my own CSV)") {
            //Create CSV
            $.ajax({
                type: 'GET',
                dataType: "text",
                url: 'http://127.0.0.1:5000/api/chembl/' + proteinList + '/' + drugList,
                success: function (data) {
                    console.log('entra en success')
                    console.log(data)
                    //Call Graph
                    $.ajax({
                        type: "GET",
                        url: "../../data/interactions_" + proteinList+'_'+drugList+'.csv',
                        dataType: "text",
                        success: function (data) {
                            var lines = (data).split("\n").length;
                            console.log('lineas', lines)
                            //Check if csv or not
                            if(lines>2) {
                                $.ajax({
                                    type: 'GET',
                                    dataType: "html",
                                    url: 'http://127.0.0.1:5000/api/graph/' + 'interactions_' + proteinList + '_' + drugList + '.csv/',
                                    success: function (data) {
                                        document.getElementById("div_grafo").style.visibility = "visible";
                                        $('#div_grafo').append(data)
                                        search_name_textbox.style.visibility='visible';
                                    },
                                    error: function (xhr) {
                                        console.log(xhr)
                                    }
                                })
                            }
                            else {
                                alert("NO SE HAN ENCONTRADO INTERACCIONES \n Prueba una nueva comnbinación.")
                                document.getElementById("desplegables").reset();
                                document.getElementById("show_t_button").style.visibility="hidden";
                                document.getElementById('div_grafo').innerHTML = '';
                            }
                        },
                        error: function (xhr) {
                           console.log(xhr)
                        }
                })

                },
                error: function (xhr) {
                    console.log('entra en error')
                    console.log(xhr)
                }
            })
        }


        //LISTS LOADED IN CSV
        else if (proteinList == "None (I will upload my own CSV)" && drugList == "None (I will upload my own CSV)") {

            //Display button ver_tabla
            show_table_button.style.visibility = 'visible';

            //Process and parse input CSV
            var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
            if (regex.test($("#csvInput").val().toLowerCase())) {
                if (typeof (FileReader) != "undefined") {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var table = $("<table />");
                        var rows = e.target.result.split("\n");
                        for (var i = 0; i < rows.length; i++) {
                            var row = $("<tr />");
                            var cells = rows[i].split(",");
                            for (var j = 0; j < cells.length; j++) {
                                var cell = $("<td />");
                                cell.html(cells[j]);
                                row.append(cell);

                            }
                            table.append(row);
                        }

                        //Show table if click button ver_tabla
                        $('#button_ver_tabla').click(function () {
                            $("#dvCSV").html('');
                            $("#dvCSV").append(table);
                        });
                        console.log('la tabla tiene', table, 'la tabla es de tipo', typeof(table));

                    }

                    var info = $("#dvCSV")
                    console.log(info);
                    reader.readAsText($("#csvInput")[0].files[0]);

                } else {
                    alert("This browser does not support HTML5.");
                }
            } else {
                alert("Please upload a valid CSV file.");
            }


            //Call graph with inserted csv
            input_csv_name = document.getElementById('csvInput').files[0].name;
            console.log('name', input_csv_name);

            //Number of rows of generated csv to see if there are interactions (call graph) or not (alert)
            $.ajax({
                type: "GET",
                url: "../../data/" +input_csv_name,
                dataType: "text",
                success: function (data) {
                    var lines = (data).split("\n").length;
                    console.log('lineas', lines)
                    if(lines>2) {
                        $.ajax({
                            type: 'GET',
                            dataType: "html",
                            url: 'http://127.0.0.1:5000/api/graph/' + input_csv_name,
                            success: function (data) {
                                document.getElementById("div_grafo").style.visibility = "visible";
                                $('#div_grafo').append(data)
                                search_name_textbox.style.visibility='visible';
                            },
                            error: function (xhr) {
                                console.log(xhr)
                            }
                        });
                    }

                    else {
                        alert("NO SE HAN ENCONTRADO INTERACCIONES \n Prueba una nueva comnbinación.")
                        document.getElementById("desplegables").reset();
                        document.getElementById("show_t_button").style.visibility="hidden";
                        document.getElementById('div_grafo').innerHTML = '';
                    }
                },
                error: function (xhr) {
                    alert(xhr);
                }
            });
        }

        else {
            error_msg='Ambas opciones deben estar a None o con una tabla seleccionada';
            window.alert(error_msg);
        }

    });
 });


//SEARCH button
$(document).ready(function(){
    $('#search_button').click(function() {
        id_to_search=document.getElementById('graph_search_textbox2').value;
        console.log(id_to_search);
         $.ajax({
            type: 'GET',
            dataType: "json",
            url: 'http://127.0.0.1:5000/api/search_information/'+id_to_search,
            success: function(data) {
                document.getElementById('json_info').innerHTML = '';
                document.getElementById('titulo_bicho').innerHTML = '';
                console.log(data);
                console.log(typeof(data));
                jsonPretty = JSON.stringify(data);
                $('#json_info').append(jsonPretty);
                openCity(event, 'protein_or_drug_information');
                $('#titulo_bicho').append(id_to_search);

            },
             error: function (xhr) {
                console.log(xhr)
            }
        });
    });
});



 //RESET button
$(document).ready(function(){
    $('#button_reset').click(function() {
        document.getElementById("desplegables").reset();
        document.getElementById("show_t_button").style.visibility="hidden";
        document.getElementById('div_grafo').innerHTML = '';
        document.getElementById('graph_search_textbox').style.visibility="hidden";

    });
});

