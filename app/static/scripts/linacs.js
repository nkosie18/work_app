$(document).ready(function () {
  $("#linacs").click(function (event) {
    var machine = event.target.id;
    if (machine !== "" && machine !== "linacs") {
      var i, tablinks;
      tablinks = document.getElementsByClassName("tablink");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(
          " w3-disabled",
          ""
        );
      }

      $("#" + machine).addClass("w3-disabled");

      if (document.getElementById("bodyup").style.display != "block") {
        $("#bodyup").css("display", "block");
      }
      var tablinke = document.getElementsByClassName("tablinkr");
      for (i = 0; i < tablinke.length; i++) {
        if (tablinke[i].className.includes("w3-disabled")) {
          qachecks2 = tablinke[i].id;
          console.log("This is the just added data" + qachecks2);
          console.log(" this is the machine" + machine);
          if (qachecks2 == "trs398") {
            $("#trs_398e").css("display", "block");
          } else {
            $("#trs_398e").css("display", "none");
          }

          $("#trs_398ee").click(function (e) {
            e.preventDefault();
            location = "/trs_398/photons?machine=" + machine;
          });
          req_data = $.ajax({
            url: "/linacViewProcess",
            type: "POST",
            data: { machine_id: machine, test_name: qachecks2 },
          });

          req_data.done(function (data) {
            var status = data.result;
            if (status == "502") {
              console.log(data.data);
            } else {
              var size1 = Object.keys(data.data_p).length;
              for (let i = 0; i < size1; i++) {
                var date = data.data_p[i].date;
                var temp = data.data_p[i].temp;
                var press = data.data_p[i].press;
                var chamber = data.data_p[i].chamber;
                var bvoltage = data.data_p[i].bias_voltage;
                var dase_max = data.data_p[i].dose_dmax;
                var pdiff = data.data_p[i].percent_diff;

                loop_string += `<tr><td>${date}</td><td>${temp}</td><td>${press}</td><td>${chamber}</td><td>${bvoltage}</td><td>${dase_max}</td><td>${pdiff}</td><td> <button id ="phot_${date}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
              }

              new_string =
                "<tr><td>Date</td><td>Temperature</td><td>Pressure</td><td>Ionization Chamber</td><td>Bias Voltage</td> <td>Dose<sub>Z_max</sub></td><td>Percent diff</td></tr>" +
                loop_string;
              $("#data_table").innerHTML(new_string);

              $("#data_table").DataTable({
                lengthMenu: [
                  [5, 10, -1],
                  [5, 10, "All"],
                ],
                aoColumns: [
                  { orderSequence: ["desc"] },
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                ],
              });
            }
          });
        }
      }
    }
  });

  //$("#qabuttons").append(``);

  /*console.log(typeof(machine))
            req_linac = $.ajax({
                url : '/linacViewProcess',
                type: 'POST',
                data: {machine_id:machine}
            });
            }
            else{console.log('You did not click the button on the table')} */

  $("#qabuttons").click(function (event) {
    var qachecks = event.target.id;
    if (qachecks !== "" && qachecks !== "qabuttons") {
      var i, j, tablinke, machine_stat;
      tablinke = document.getElementsByClassName("tablinkr");
      for (i = 0; i < tablinke.length; i++) {
        tablinke[i].className = tablinke[i].className.replace(
          " w3-disabled",
          ""
        );
      }
    }

    $("#" + qachecks).addClass("w3-disabled");

    machine_stat = document.getElementsByClassName("tablink");
    for (j = 0; j < machine_stat.length; j++) {
      if (machine_stat[j].className.includes("w3-disabled")) {
        machine = machine_stat[j].id;
      }
    }
    var current_machine = machine;
    var current_check = qachecks;
    console.log(current_check);

    switch (current_check) {
      //The TRS-398 block of code
      case "trs398":
        $("#trs398_qcCheks").css("display", "block");
        $("#energy_checks").css("display", "none");
        $("#flatandaym_checks").css("display", "none");
        $("#mechanical_checks").css("display", "none");
        req3_data = $.ajax({
          url: "/linacViewProcess",
          type: "POST",
          data: { machine_id: current_machine, test_name: current_check },
        });

        req3_data.done(function (data) {
          var status = data.result;
          if (status == "502") {
            console.log(data.data);
          } else {
            var loop_string = "";
            var size1 = Object.keys(data.data_p).length;
            for (let i = 0; i < size1; i++) {
              var date = data.data_p[i].date;
              var temp = data.data_p[i].temp;
              var press = data.data_p[i].press;
              var chamber = data.data_p[i].chamber;
              var bvoltage = data.data_p[i].bias_voltage;
              var dase_max = data.data_p[i].dose_dmax;
              var pdiff = data.data_p[i].percent_diff;
              loop_string += `<tr><td>${date}</td><td>${temp}</td><td>${press}</td><td>${chamber}</td><td>${bvoltage}</td><td>${dase_max}</td><td>${pdiff}</td><td> <button id ="phot_${date}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
            }

            new_string =
              "<tr><td>Date</td><td>Temperature</td><td>Pressure</td><td>Ionization Chamber</td><td>Bias Voltage</td> <td>Dose <sub>Z_max</sub></td><td>Percent diff</td></tr>" +
              loop_string;
            $("#data_table").innerHTML(new_string);

            $("#data_table").DataTable({
              lengthMenu: [
                [5, 10, -1],
                [5, 10, "All"],
              ],
              aoColumns: [
                { orderSequence: ["desc"] },
                null,
                null,
                null,
                null,
                null,
                null,
                null,
              ],
            });
          }
        });

        break;
      //The energy checks code block
      case "energy_chk":
        $("#energy_checks").css("display", "block");
        //The loop to get data from the server

        req4_data = $.ajax({
          url: "/EnergyChecks",
          type: "POST",
          data: { machine_id: current_machine, test_name: current_check },
        });

        req4_data.done(function (data) {
          var status = data.result;
          if (status == "502") {
            console.log(data.data);
          } else {
            $("#trs_398e").css("display", "none");
            $("#trs398_qcCheks").css("display", "none");
            $("#flatandaym_checks").css("display", "none");
            $("#mechanical_checks").css("display", "none");
            var loop_string1 = "";
            var size1 = Object.keys(data.data_p).length;
            for (let i = 0; i < size1; i++) {
              var date = data.data_p[i].date;
              var energy_p = data.data_p[i].energy;
              var uid_p = data.data_p[i].uid;
              var dmax_p = data.data_p[i].dose_dmax;
              var pdd_10 = data.data_p[i].pdd10;
              var tpr = data.data_p[i].tpr;
              var added_by = data.data_p[i].added_by;
              loop_string1 += `<tr><td>${date}</td><td>${energy_p}</td><td>${dmax_p}</td><td>${pdd_10}</td><td>${tpr}</td><td>${added_by}</td><td> <button id ="${uid_p}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
            }

            new_string1 = `<table id="energy_checks_table"  class="w3-table-all"><tr> <th>Date</th> <th>Energy</th> <th>D <sub>Zmax</sub></th> <th>PDD <sub>10</sub></th> <th>TPR <sub>20,10</sub></th> <th>Physicist</th> <th>  </th></tr> ${loop_string1} </table>`;
            $("#energy_checks_2").prepend(new_string1);

            $("#energy_checks_table").DataTable({
              lengthMenu: [
                [5, 10, -1],
                [5, 10, "All"],
              ],
              aoColumns: [null, null, null, null, null, null, null],
            });
          }
        });
        break;

      default:
        console.log("This is the default code");
        break;
    }
  });

  $("#energy_checks_b").click(function (e) {
    e.preventDefault();
    location = "/energyChecks/update_pdd";
  });

  $("#machine_stats").click(function (e) {
    e.preventDefault();
    var machine_stat = e.target.id;
    if (
      machine_stat === "l1_prog" ||
      machine_stat === "l2_prog" ||
      machine_stat === "l3_prog"
    ) {
      console.log(machine_stat.substring(0, 2) + "_data");
      m_name = machine_stat.substring(0, 2);

      $.ajax({
        type: "GET",
        url: "/linac/status",
        data: { machine_selected: m_name },
        success: function (data) {},
      });

      $("#" + m_name + "_data").replaceWith(`
      <tr>
              <td><b>L${m_name.substring(1, 2)}</b></td>
              <td>
                <ul>
                  <li>TRS-398: <span id="trs_stat_1" style="color: red;">Not Done</span></li>
                </ul>
                <ul>
                  <li>Energy checks: <span id="eng_stat_1" style="color: red;">Not Done</span></li>
                </ul>
                <ul>
                  <li>Machanicals: <span id="trs_stat_1" style="color: red;">Not Done</span></li>
                </ul>
                <ul>
                  <li>Flat and Sym: <span id="trs_stat_1" style="color: red;">Not Done</span></li>
                </ul>
              </td>
            </tr>
      `);
    } else {
      console.log("You did not click the button on the table");
    }
  });

  $("#trs_398ph").click(function (e) {
    e.preventDefault();
    machine_stat = document.getElementsByClassName("tablink");
    for (let j = 0; j < machine_stat.length; j++) {
      if (machine_stat[j].className.includes("w3-disabled")) {
        machine = machine_stat[j].id;
      }
    }

    location = "/trs_398/photons?machine=" + machine;
  });

  /*
    $("#addmore").click(function(){
        $("#mytable").append("<tr><td>Mfeka</dt><td>J. P</dt><td>KZ003344</dt><td>10 MV</dt></tr>");
       });

    $('#addjson').click(function(event) {
    event.preventDefault();
    $.getJSON('b.json');
    });

    $('#check').click(function(){

        var name = $('#chamber').val();

        req = $.ajax({

            url : '/process',
            type : 'POST',
            data : {name : name}

        });

        req.done(function(data){

            $('#adddata').html('<h2>'+ data.name +'</h2> <br><br><br> <table class = "w3-table-all"> <tr><td>Calibration Lab</td><td>' + data.cal_lab + '</td></tr><tr><td>Calibration date</td><td>' +data. cal_date + '</td></tr><tr><td>Calibration factor</td><td>' + data.cal_factor + '</td></tr></table>'
                
                );
        });
    }); */
});
