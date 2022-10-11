$(document).ready(function () {
  function show_data(machine, qaTest) {
    if (document.getElementById("bodyup").style.display != "block") {
      $("#bodyup").css("display", "block");
    }

    try {
      switch (qaTest) {
        case "trs398":
          $("#qctest_block").html(`<div id="trs_398_calibration" class="w3-row">
          <div class="w3-col l9 m10">
            <button id="trs_398ph" class="w3-button w3-round w3-blue">
              Cal: Photons
            </button>
            <button id="trs_398el" class="w3-button w3-round w3-blue">
              Cal: Electrons
            </button>
          </div>
        </div>
        <div
          id="trs398_qcCheks"
          class="w3-row w3-padding"
          style = "display : none"
        >
          <div class="w3-container w3-responsive">
            <table id="data_table" class="w3-table-all">
              <tr>
                <td>Date</td>
                <td>Temperature</td>
                <td>Pressure</td>
                <td>Ionization Chamber</td>
                <td>Bias Voltage</td>
                <td>Dose <sub>Z_max</sub></td>
                <td>Percent diff</td>
              </tr>
            </table>
          </div>
        </div>`);
          $("#trs_398ph").click(function (e) {
            e.preventDefault();
            location = "/trs_398/photons?machine=" + machine;
          });

          $.ajax({
            type: "POST",
            url: "/linacViewProcess",
            data: { machine_id: machine, test_name: qaTest },
            success: function (data) {
              var status = data.result;
              if (status == "502") {
                console.log(data.data);
              } else {
                $("#trs398_qcCheks").css("display", "block"); ///////////////////
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
            },
          });

          break;

        case "energy_chk":
          $(
            "#qctest_block"
          ).html(`<div id="energy_checks" class="w3-row w3-padding">
          <div class="w3-col l9 m10">
            <button
              id="energy_checks_b"
              class="w3-button w3-round w3-blue"
              role="button"
            >
              PDD analysis
            </button>
            <div class="w3-row w3-padding"></div>
          </div>
          <div class="w3-col l3 m2"><p></p></div>
        </div>
        <div class="w3-row">
          <div id="energy_checks_2" class="w3-col s12 l9 m10"></div>
          <div class="w3-col s12 l3 m2"><p></p></div>
        </div>`);
          $("#energy_checks_b").click(function (e) {
            e.preventDefault();
            location = "/energyChecks/update_pdd";
          });

          $.ajax({
            type: "POST",
            url: "/EnergyChecks",
            data: { machine_id: machine, test_name: qaTest },
            success: function (data) {
              var status = data.result;
              if (status == "502") {
                console.log(data.data);
              } else {
                $("#energy_checks_2").html(
                  `<div class="w3-container w3-container-fluid "><h3>Photons Data</h3> <hr><table id="energy_checks_table"  class="w3-table-all"> <thead><tr> <th>Date</th> <th>Energy</th> <th>D <sub>Zmax</sub></th> <th>PDD <sub>10</sub></th> <th>TPR <sub>20,10</sub></th> <th>Physicist</th> <th>  </th></tr> </thead> <tbody id =" "</table></div>`
                );
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

                $("#energy_checks_table").append(loop_string1);

                $("#energy_checks_table").DataTable({
                  lengthMenu: [
                    [5, 10, -1],
                    [5, 10, "All"],
                  ],
                  aoColumns: [null, null, null, null, null, null, null],
                });
              }
            },
          });

          break;

        case "No_Tab_is_Selected":
          $("#trs_398_calibration").remove();
          $("#trs398_qcCheks").remove();
          $("#energy_checks").remove();
          $("#flatandaym_checks").remove();
          $("#mechanical_checks").remove();
          break;

        default:
          $("#trs_398_calibration").remove();
          $("#trs398_qcCheks").remove();
          $("#energy_checks").remove();
          $("#flatandaym_checks").remove();
          $("#mechanical_checks").remove();
          break;
      }
    } catch (error) {
      console.log(error);
    }
  }

  //
  function checkEnabled_qaTab() {
    var i, tabliks1;
    tabliks1 = document.getElementsByClassName("tablinkr");
    console.log("The number of element: " + tabliks1);
    for (i = 0; i < tabliks1.length; i++) {
      if (tabliks1[i].className.includes("w3-disabled")) {
        qaTab = tabliks1[i].id;
        return qaTab;
      }
    }
  }

  //
  function checkEnabled_machineTab() {
    var i, tabliks2;
    tabliks2 = document.getElementsByClassName("tablink");
    console.log(tabliks2);
    for (i = 0; i < tabliks2.length; i++) {
      if (tabliks2[i].className.includes("w3-disabled")) {
        machineTab = tabliks2[i].id;
        return machineTab;
      }
    }
  }
  //
  //
  $("#linacs").click(function (e) {
    e.preventDefault();
    var machine = e.target.id;
    if (machine !== "" && machine !== "linacs") {
      var machineTabz, i;
      machineTabz = document.getElementsByClassName("tablink");
      for (i = 0; i < machineTabz.length; i++) {
        if (
          machineTabz[i].id === machine &&
          !machineTabz[i].className.includes("w3-disabled")
        ) {
          $("#" + machine).addClass("w3-disabled");
        } else {
          machineTabz[i].className = machineTabz[i].className.replace(
            "w3-disabled",
            ""
          );
        }
      }
      var qaTestSelected = checkEnabled_qaTab();
      show_data(machine, qaTestSelected);
    }
  });

  $("#qabuttons").click(function (e) {
    e.preventDefault();
    var selectedQaTab = e.target.id;
    if (selectedQaTab !== "" && selectedQaTab !== "qabuttons") {
      var qaTesTabs, i;
      qaTesTabs = document.getElementsByClassName("tablinkr");
      for (i = 0; i < qaTesTabs.length; i++) {
        if (
          qaTesTabs[i].id === selectedQaTab &&
          !qaTesTabs[i].className.includes("w3-disabled")
        ) {
          $("#" + selectedQaTab).addClass("w3-disabled");
        } else {
          qaTesTabs[i].className = qaTesTabs[i].className.replace(
            "w3-disabled",
            ""
          );
        }
      }
      var machineSelected = checkEnabled_machineTab();
      show_data(machineSelected, selectedQaTab);
    }
  });
});
