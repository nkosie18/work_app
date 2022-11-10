$(document).ready(function () {
  function show_data(machine, qaTest) {
    if (document.getElementById("bodyup").style.display != "block") {
      $("#bodyup").css("display", "block");
    }
    try {
      switch (qaTest) {
        /*
      TRS 398 Block of code.
      */
        case "trs398":
          $("#qctest_block").html(`<div id="trs_398_calibration" class="w3-row">
          <div class="w3-col l9 m10 padding-top">
            <button id="trs_398ph" class="w3-button w3-round w3-blue">
              Cal: Photons
            </button>
            <button id="trs_398el" class="w3-button w3-round w3-blue">
              Cal: Electrons
            </button>
          </div>
          <hr class="mt">
        </div>
        
        <div
          id="trs398_qcCheks"
          class="w3-row w3-padding "
          style = "display : none"
        >
          <div class="w3-row w3-container">
            <div class="w3-col l1 m1 w3-hide-small"><p></p></div>
            <div class="w3-col l8 m8">
            <div class = "padding-top">
            <h2> TRS-398 Data. </h2>
            <h3> <i>Photons</i> </h3>
          </div>
          <div class="w3-container w3-responsive">
            <table id="data_table" class="w3-table-all">
              <thead>
                <tr>  
                  <th>Date</th>
                  <th>Energy</th>
                  <th>Ionization Chamber</th>
                  <th>Dose <sub>Z_max</sub></th>
                  <th>Percent diff</th>
                  <th></th>
                </tr>
              </thead>
              <tbody id = "trs398_ph_body">
              </tbody>
            </table>
          </div>
        
          <div class = "padding-top">
            <h3> <i>Electrons</i> </h3>
          </div>
          <div class="w3-container w3-responsive">
            <table id= "data_table_elec" class= "w3-table-all">
              <thead>
                <tr>
                  <th> Date </th>
                  <th> Energy </th>
                  <th>Ionization Chamber</th>
                  <th>Dose <sub>Z_max</sub></th>
                  <th>Percent diff</th>
                  <th></th>
                </tr>
              </thead>
              <tbody id = "trs398_el_body">
              </tbody>
            </table>
          </div>
            </div>
            <div class="w3-col l3 m3 w3-hide-small"><p></p></div>
          </div>
        </div>

        `);
          $("#trs_398ph").click(function (e) {
            e.preventDefault();
            location = "/trs_398/photons?machine=" + machine;
          });

          $("#trs_398el").click(function (e) {
            e.preventDefault();
            location = "/trs_398/electrons?machine=" + machine;
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
                var loop_string_p = "";
                var loop_string_e = "";
                var size1 = Object.keys(data.data_p).length;
                var size2 = Object.keys(data.data_e).length;
                for (let i = 0; i < size1; i++) {
                  var date = data.data_p[i].date;
                  var temp = data.data_p[i].temp;
                  var energy = data.data_p[i].Beam;
                  var press = data.data_p[i].press;
                  var chamber = data.data_p[i].chamber;
                  var bvoltage = data.data_p[i].bias_voltage;
                  var dase_max = data.data_p[i].dose_dmax;
                  var pdiff = data.data_p[i].percent_diff;
                  loop_string_p += `<tr><td>${date}</td><td>${energy}</td><td>${chamber}</td><td>${dase_max} cGy/Mu</td><td>${pdiff} %</td><td> <button id ="phot_${date}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
                }

                for (let j = 0; j < size2; j++) {
                  var date1 = data.data_e[j].date;
                  var temp1 = data.data_e[j].temp;
                  var energy1 = data.data_e[j].Beam;
                  var press1 = data.data_e[j].press;
                  var chamber1 = data.data_e[j].chamber;
                  var bvoltage1 = data.data_e[j].bias_voltage;
                  var dase_max1 = data.data_e[j].dose_dmax;
                  var pdiff1 = data.data_e[j].percent_diff;
                  loop_string_e += `<tr><td>${date1}</td><td>${energy1}</td><td>${chamber1}</td><td>${dase_max1} cGy/Mu</td><td>${pdiff1} %</td><td> <button id ="elec_${date1}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
                }

                $("#trs398_ph_body").append(loop_string_p);

                $("#trs398_el_body").append(loop_string_e);

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
                  ],
                });

                $("#data_table_elec").DataTable({
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
                  ],
                });
              }
            },
          });

          break;

        /*
      Energy Checks Block of code.
      */

        case "energy_chk":
          $("#qctest_block").html(`
          <div id="energy_checks" class="w3-row w3-container">
            <div class="w3-row w3-padding">
              <button
                id="energy_checks_b"
                class="w3-button w3-round w3-blue"
                role="button">
                PDD analysis
              </button>
            </div>

            <div id="energy_checks_ph" class="w3-row w3-padding" style = "display : none">
              <div class="w3-row">
                <h2>Beam energy checks data.</h2>
              </div>
              <div class="w3-row w3-container">
                <div class ="w3-col l1 m1 w3-hide-small"><p></p></div>
                <div class= "w3-col  m9 l9">
                  <div class="w3-row">
                    <h3><i>Photons</i></h3>
                  </div>
                  
                  <div class="w3-row w3-container">
                  <table id = "eng_chks_photons" class="w3-table-all w3-padding">
                  <thead>
                    <tr>
                      <th> Date </th>
                      <th> Energy </th>
                      <th> D<sub>Z<sub>max</sub></sub></th>
                      <th> PDD<sub>10</sub></th>
                      <th> TPR<sub>20,10</sub></th>
                      <th> Physicist</th>
                      <th></th> 
                    </tr>
                  </thead>
                  <tbody id="eng_chcks_ph_body">

                  </tbody>
                </table>
                  </div>
                  
                </div>
                <div class="w3-col m3 l3 w3-hide-small">
                <p></p>
                </div>
              </div>
            </div>
            <div id = "energy_checks_el" class="w3-row w3-padding" style="display : none">
            <div class ="w3-col l1 m1 w3-hide-small"><p></p></div>
            <div class= "w3-col  m9 l9">
              <div class="w3-row">
                <h3><i>Electrons</i></h3>
              </div>
              
              <div class="w3-row w3-container">
              <table id = "eng_chks_electrons" class="w3-table-all w3-padding">
              <thead>
                <tr>
                  <th> Date </th>
                  <th> Energy </th>
                  <th> R<sub>50</sub></th>
                  <th> E<sub>0</sub></th>
                  <th> R<sub>P</sub></th>
                  <th> Physicist</th>
                  <th></th> 
                </tr>
              </thead>
              <tbody id="eng_chcks_el_body">

              </tbody>
            </table>
              </div>
              
            </div>
            <div class="w3-col m3 l3 w3-hide-small">
            <p></p>
            </div>
            </div>
          </div>`);
          $("#energy_checks_b").click(function (e) {
            e.preventDefault();
            location = "/energyChecks/update_pdd";
          });

          $("#eng_chks_photons").click(function (event) {
            event.preventDefault();
            var selection = event.target.id;
            if (selection.split("~")[0] === "uuid") {
              var new_uuid = selection.split("~")[1];
              location = `/energyChecks/upload_status?uid_new=${new_uuid}`;
            }
          });

          $("#eng_chks_electrons").click(function (event) {
            event.preventDefault();
            var selection = event.target.id;
            if (selection.split("~")[0] === "uuid") {
              var new_uuid = selection.split("~")[1];
              location = `/energyChecks/upload_status?uid_new=${new_uuid}`;
            }
          });

          $.ajax({
            type: "POST",
            url: "/EnergyChecks",
            data: { machine_id: machine, test_name: qaTest },
            success: function (data) {
              var status = data.results;
              if (status == "502") {
                console.log(data.data);
              }
              if (status == "success" && data.data_p !== undefined) {
                $("#energy_checks_ph").css("display", "block");
                var loop_string2 = "";
                var size1 = Object.keys(data.data_p).length;
                for (let i = 0; i < size1; i++) {
                  var date = data.data_p[i].date;
                  var energy_p = data.data_p[i].energy;
                  var uid_p = data.data_p[i].uid;
                  var dmax_p = data.data_p[i].dose_dmax;
                  var pdd_10 = data.data_p[i].pdd10;
                  var tpr = data.data_p[i].tpr;
                  var added_by = data.data_p[i].added_by;
                  loop_string2 += `<tr><td>${date}</td><td>${energy_p}</td><td>${dmax_p}</td><td>${pdd_10}</td><td>${tpr}</td><td>${added_by}</td><td> <button id ="uuid~${uid_p}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
                }

                $("#eng_chcks_ph_body").html(loop_string2);

                $("#eng_chks_photons").DataTable({
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
                  ],
                });
              }

              if (status == "success" && data.data_e !== undefined) {
                $("#energy_checks_el").css("display", "block");
                var loop_string3 = "";
                var size1 = Object.keys(data.data_e).length;
                for (let i = 0; i < size1; i++) {
                  var date = data.data_e[i].date;
                  var energy_e = data.data_e[i].energy;
                  var uid_e = data.data_e[i].uid;
                  var r50 = data.data_e[i].r50;
                  var e_not = data.data_e[i].e_not;
                  var r_p = data.data_e[i].r_p;
                  var added_by = data.data_e[i].added_by;
                  loop_string3 += `<tr><td>${date}</td><td>${energy_e}</td><td>${r50}</td><td>${e_not}</td><td>${r_p}</td><td>${added_by}</td><td> <button id ="uuid~${uid_e}" class="w3-button w3-blue w3-round w3-border">View</button></td></tr>`;
                }

                $("#eng_chcks_el_body").html(loop_string3);

                $("#eng_chks_electrons").DataTable({
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
                  ],
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
        }

        if (
          machineTabz[i].id !== machine &&
          machineTabz[i].className.includes("w3-disabled")
        ) {
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
        }

        if (
          qaTesTabs[i].id !== selectedQaTab &&
          qaTesTabs[i].className.includes("w3-disabled")
        ) {
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
