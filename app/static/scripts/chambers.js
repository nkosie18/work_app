$(document).ready(function () {
  $.ajax({
    url: "/chamberCalStatus",
    type: "GET",
    success: function (data) {
      if (data.status == "success") {
        var size = Object.keys(data.chamb_dates).length;
        for (let i = 0; i < size; i++) {
          $("#last_cal_" + data.chamb_dates[i].chamb_sn).html(
            data.chamb_dates[i].cal_date + " days ago"
          );
        }
      }
    },
  });

  $("#chambst").click(function (event) {
    //event.preventDefault();

    var serial_number = event.target.id;
    //console.log(serial_number)
    if (serial_number != "") {
      req2 = $.ajax({
        url: "/chambViewProcess",
        type: "POST",
        data: { sn: serial_number },
      });
      req2.done(function (data) {
        //const j = 2 == 2 ? console.log('The button works fine'):console.log("nothing")

        ///  The code that will run after the post responce has been rendered

        var chamber_name = data.chamb_name;
        var date = data.date_ref;
        var electrometer = data.electrometer_ref;
        var voltage = data.elect_voltage_ref;
        var source = data.source_ref;
        var decay_ref1 = data.decay_ref;
        var ref_exposure = data.exposure_ref;

        $("#chambhist").css("display", "block");
        $("#refmeas_b").html(`
                        <i><h2 style ="margin-top:-20mm;"> ${chamber_name}</h2></i>
                        <p style="margin-top:-5mm;"><i> reference data</i></p> <br>
        
                        <table>
                        <tr><td> Date: </td><td> <b> ${date}</b> </td></tr>
                        <tr><td> Electrometer: </td><td><b>${electrometer}</b> </td></tr>
                       <tr> <td> Biasing Voltage:</td><td> <b>${voltage} </b> </td></tr>
                        <tr><td> Check Source: </td><td><b>${source} </b></td></tr>
                        <tr><td> Decay Factor:</td><td><b> ${decay_ref1}</b> </td></tr>
                        <tr><td> Exposure:</td><td><b> ${ref_exposure.toFixed(
                          2
                        )} mGy</b></td></tr>
                        <tr></table>
                    `);

        $("#chambhist").html(`
                    <div class = "w3-responsive">
                    <table id= "numbanumba" class = " w3-table-all w3-small">
                    <thead>
                    <tr>
                    <th> Date </th>
                    <th> X <sub> mean</sub> (mGy) </th>
                    <th> Temp(<sup> 0 </sup> C) </th>
                    <th> Press (mm Hg) </th>
                    <th> Ktp </th>
                    <th> Sr-90 Decay </th>
                    <th> X <sub> corr </sub> (mGy)  </th>
                    <th> % Error </th>
                    </tr>
                    </thead>
                    <tbody id = "chambHistBody">
                    </tbody>
                    </table>
                    </div>
        
                    <p style="margin-top:3mm;"> <i> <b>Table 2.</b> Previouse Sr-90 stability check measurements for ${chamber_name}. </i></p> <br><br>
                    
                    
                    
        
                    `);
        $("#chambCal").html(`
                    <div class="w3-responsive">
                        <table id ="calcert" class="w3-table-all w3-small">
                        <thead>
                        <tr>
                        <th>Date Loaded</th>
                        <th>Loaded by</th>
                        <th>Calibration Lab</th>
                        <th>Date Calibrated</th>
                        <th>Calibration Factor</th>
                        <th>Electrometer</th>
                        <th>Bias Voltage</th>
                        <th>Beam Quality</th>
                        </tr>
                        </thead>
                        <tbody id ="calCertBody">
                        </tbody>
                        </table>
                        <p style="margin-top:3mm;"> <i> <b>Table 3.</b> Calibration certificates for ${chamber_name}. </i></p> <br><br> 
                    </div>
                    `);

        var size_cert = Object.keys(data.cert).length;

        for (let i = 0; i < size_cert; i++) {
          var date_loaded = data.cert[i].date_loaded;
          var loaded_by = data.cert[i].added_by;
          var date_cal = data.cert[i].date_cal;
          var cal_lab = data.cert[i].cal_lab;
          var cal_factor = data.cert[i].ndw;
          var electrometer_cert = data.cert[i].electrometer;
          var bias_voltage = data.cert[i].voltage;
          var beam_quality = data.cert[i].cal_energy;

          $("#calCertBody").append(`
        
                        <tr>
                        <td> ${date_loaded} </td>
                        <td> ${loaded_by} </td>
                        <td> ${cal_lab} </td>
                        <td> ${date_cal} </td>
                        <td> ${cal_factor.toFixed(5)} </td>
                        <td> ${electrometer_cert} </td>
                        <td> ${bias_voltage} </td>
                        <td> ${beam_quality} </td>
                        </tr>
        
                        `);
          $("#calcert").DataTable({
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

        if (data.ref_only !== "true") {
          var size = Object.keys(data.data).length;

          for (let i = 0; i < size; i++) {
            var date1 = data.data[i].date;
            var mean_exposure = data.data[i].mean_exposure;
            var temp = data.data[i].m_temp;
            var press = data.data[i].m_press;
            var ktp = data.data[i].ktp;
            var decay = data.data[i].decay;
            var exposure_corr = data.data[i].exposure_corr;
            var percent_diff = data.data[i].percent_diff;
            $("#chambHistBody").append(`
                            <tr>
                            <td> ${date1} </td>
                            <td> ${mean_exposure.toFixed(2)} </td>
                            <td> ${temp.toFixed(2)} </td>
                            <td> ${press.toFixed(1)} </td>
                            <td> ${ktp.toFixed(3)} </td>
                            <td> ${decay.toFixed(3)} </td>
                            <td> ${exposure_corr.toFixed(2)} </td>
                            <td> ${percent_diff.toFixed(2)} </td>
                            </tr>
                             `);
          }

          $("#numbanumba").DataTable({
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
  });
});
