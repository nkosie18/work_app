$(document).ready(function () {
  $("#beam_data_e").click(function (e) {
    e.preventDefault();
    var machine = $("#machine_tag").text();
    var beam = $("#sele_beam").find(":selected").text();
    var chamber = $("#sele_chamber").find(":selected").text();
    $("#beamDataStatuse").val("Active");

    $.ajax({
      type: "POST",
      url: "/trs_398e/check_beam_data",
      data: { machine: machine, beam: beam, chamber: chamber },

      success: function (data) {
        if (data.success) {
          $("#beam_data_table").html(
            `
            <tr>
              <td><b>Date Measured :</b></td>
              <td id= 'beam_data_date'>${data.beam_data.date}</td>
            </tr>
            <tr>
              <td><b>R<sub>50</sub> :</b></td>
              <td id = "r_50_data">${data.beam_data.r50} g/cm<sup>2</sup> </td>
            </tr>
            <tr>
            <td><b>Depth (<sub>Z<sub>ref</sub></sub>) :</b></td>
            <td id = "z_ref">${data.beam_data.zref} g/cm<sup>2</sup> </td>
          </tr>
            <tr>
              <td><b>K<sub>Q,Q0</sub> :</b></td>
              <td id = "kqq">${data.beam_data.kqq}</td>
            </tr>
            <tr>
              <td><b>PDD<sub>Z<sub>ref</sub></sub> :</b></td>
              <td id = "pdd_zref">${data.beam_data.pdd_zref}</td>
            </tr>
            `
          );

          $("#ref_depth ").html(data.beam_data.zref + " g/cm<sup>2</sup>");

          $("#chamber_data_table").html(
            `
            <tr>
              <td><b>Date Calibrated :</b></td>
              <td >${data.chamber_data.date}</td>
            </tr>
            <tr>
              <td><b>Calibration Lab :</b></td>
              <td>${data.chamber_data.lab}</td>
            </tr>
            <tr>
              <td><b>Calibration Energy :</b></td>
              <td>${data.chamber_data.energy}</td>
            </tr>
            <tr>
              <td><b>N<sub>DW</sub> :</b></td>
              <td id = "ndw_corr">${data.chamber_data.ndw} Gy/nC</td>
            </tr>
            `
          );
        }
      },
    });
  });

  $("#tem_pres_e").click(function (e) {
    e.preventDefault();
    $(".tp_table").hide();
    $("#tem_pres_u").hide();
    $(".update_env").show();
  });

  $("#update_tp").click(function (e) {
    e.preventDefault();

    var temp = parseFloat($("#temp_u").val());
    var press = parseFloat($("#press_u").val());

    if (!isNaN(temp) && !isNaN(press)) {
      $.ajax({
        type: "POST",
        url: "/trs398/update_tp",
        data: { temp: temp, press: press },
        success: function (data) {
          if (data.success) {
            location.reload();
          }
        },
      });
    } else {
      alert(
        "Please enter valid values. The values for temperature and pressure should be numbers"
      );
    }
  });

  $("#readings_col").change(function (event) {
    event.preventDefault();
    var ndw = parseFloat($("#ndw_corr").text().split(" ")[0]);
    var k_corr = parseFloat($("#kqq").text());
    var pdd_zref = parseFloat($("#pdd_zref").text());
    var temp = $("#temp_d").text();
    var press = $("#pres_d").text();

    var k_tp =
      (1013.2 / parseFloat(press.split(" ")[0])) *
      ((parseFloat(temp.split(" ")[0]) + 273.2) / 293.2);

    if ($("#beamDataStatuse").val() === "Active") {
      $("#validate").css("display", "block");
    }

    switch (true) {
      case $("#m12_reading").val() === "" && $("#m13_reading").val() === "":
        var mean_reading = parseFloat($("#m11_reading").val());
        break;

      case $("#m12_reading").val() !== "" && $("#m13_reading").val() === "":
        var mean_reading =
          (parseFloat($("#m11_reading").val()) +
            parseFloat($("#m12_reading").val())) /
          2;
        break;

      default:
        var mean_reading =
          (parseFloat($("#m11_reading").val()) +
            parseFloat($("#m12_reading").val()) +
            parseFloat($("#m13_reading").val())) /
          3;
        break;
    }

    var d_zref = mean_reading * ndw * k_corr * k_tp;
    var d_zmax = d_zref / (pdd_zref / 100);
    $("#dose_dmax").text(d_zmax.toFixed(3));
  });

  /*
the validation button is comming bellow
*/

  $("#val_btn").click(function (e) {
    e.preventDefault();

    var ndw = parseFloat($("#ndw_corr").text().split(" ")[0]);
    var k_corr = parseFloat($("#kqq").text());
    var pddzref = parseFloat($("#pdd_zref").text());
    var temp = $("#temp_d").text();
    var press = $("#pres_d").text();
    var v1 = $("#bias_voltage1").find(":selected").text();
    var v2 = $("#bias_voltage2").find(":selected").text();
    let avrg_reading, m1, m2, m3, m12, m22, avrg_reading2, k_s;

    var k_tp =
      (1013.2 / parseFloat(press.split(" ")[0])) *
      ((parseFloat(temp.split(" ")[0]) + 273.2) / 293.2);

    switch (true) {
      case $("#m12_reading").val() === "":
        m1 = parseFloat($("#m11_reading").val());
        m2 = m1;
        m3 = m1;
        $("#m12_reading").val(m1);
        $("#m13_reading").val(m1);
        break;

      case $("#m13_reading").val() === "":
        m1 = parseFloat($("#m11_reading").val());
        m2 = parseFloat($("#m12_reading").val());
        var thirdReading_1 = ((m1 + m2) / 2).toFixed(3);
        $("#m13_reading").val(thirdReading_1);
        m3 = parseFloat(thirdReading_1);
        break;

      default:
        m1 = parseFloat($("#m11_reading").val());
        m2 = parseFloat($("#m12_reading").val());
        m3 = parseFloat($("#m13_reading").val());
        break;
    }

    avrg_reading = ((m1 + m2 + m3) / 3).toFixed(3);

    switch (true) {
      case $("#m21_reading").val() === "":
        m12 = avrg_reading;
        m22 = m12;
        $("#m21_reading").val(m12);
        $("#m22_reading").val(m22);
        avrg_reading2 = (parseFloat(m12) + parseFloat(m22)) / 2;
        break;

      case $("#m22_reading").val() === "":
        m12 = $("#m21_reading").val();
        m22 = $("#m21_reading").val();
        $("#m22_reading").val(m22);
        avrg_reading2 = (parseFloat(m12) + parseFloat(m22)) / 2;
        break;

      default:
        m12 = $("#m21_reading").val();
        m22 = $("#m22_reading").val();
        avrg_reading2 = (parseFloat(m12) + parseFloat(m22)) / 2;
        break;
    }

    $.ajax({
      type: "POST",
      url: "/trs398/photons/correctionFactors",
      data: {
        avrg_reading: avrg_reading,
        avrg_reading2: avrg_reading2,
        v1: v1,
        v2: v2,
      },
      success: function (data) {
        if (data.success) {
          k_s = parseFloat(data.k_s);
          var d_zref =
            parseFloat(avrg_reading) * ndw * k_corr * k_tp * parseFloat(k_s);
          var d_zmax = d_zref / (pddzref / 100);
          $("#mref").text(avrg_reading);
          $("#ndw").text(ndw);
          $("#kqq").text(k_corr);
          $("#ktp").text(k_tp.toFixed(3));
          $("#ks").text(k_s);
          $("#pdd").text(pddzref);
          $("#dose_dmax").text(d_zmax.toFixed(3));
        }
      },
    });

    if (!isNaN(avrg_reading)) {
      $("#val_btn").css("display", "none");
      $("#submit").css("display", "block");
      $("#raw_data").removeClass("hidden");
      if ($("#status_bg").hasClass("danger")) {
        $("#status_bg").removeClass("danger");
        $("#status_bg").addClass("success");
        $("#status").html("The data was validated successfully!");
      }
      $("#status_bg").removeClass("hidden");
      setTimeout(() => {
        $("#status_bg").addClass("hidden");
      }, 3000);
    }

    if (isNaN(avrg_reading)) {
      if ($("#status_bg").hasClass("success")) {
        $("#status_bg").removeClass("success");
      }
      $("#status_bg").addClass("danger");
      $("#status").html(
        "The data was not validated successfully! Some of the values entered are not numbers."
      );

      $("#status_bg").removeClass("hidden");
      setTimeout(() => {
        $("#status_bg").addClass("hidden");
      }, 3000);
    }
  });

  /* 
Next button click does this
*/

  $("#next_beam").click(function (e) {
    e.preventDefault();
    var v1 = $("#bias_voltage1").find(":selected").text();
    var m1 = $("#m11_reading").val();
    var m2 = $("#m12_reading").val();
    var m3 = $("#m13_reading").val();

    var v2 = $("#bias_voltage2").find(":selected").text();
    var m21 = $("#m21_reading").val();
    var m22 = $("#m22_reading").val();
    var pdd_zref1 = $("#pdd_zref").text();
    var url = new URL(window.location.href);
    var machine = url.searchParams.get("machine");
    var date = $("#date").val();
    var energy = $("#sele_beam").find(":selected").text();
    var chamber = $("#chamber").find(":selected").text();
    var electometer = $("#electrometer").find(":selected").text();
    var temp = $("#temp_d").text();
    var press = $("#pres_d").text();
    var beam_data_date = $("#beam_data_date").text();
    var ndw = parseFloat($("#ndw_corr").text().split(" ")[0]);
    var m_average = $("#mref").text();
    var dose_zmax = $("#dose_dmax").text();
    console.log(beam_data_date);
    $.ajax({
      type: "POST",
      url: "/trs398/electrons_2",
      data: {
        v1: v1,
        m1_reading: m1,
        m2_reading: m2,
        m3_reading: m3,
        v2: v2,
        m21_reading: m21,
        m22_reading: m22,
        machine: machine,
        date: date,
        energy: energy,
        chamber: chamber,
        electrometer: electometer,
        temp: temp,
        press: press,
        ndw: ndw,
        beam_data_date: beam_data_date,
        pdd_zref: pdd_zref1,
        m_average: m_average,
        dose_zmax: dose_zmax,
      },
      success: function (data) {
        if (data.success) {
          if ($("#status_bg").hasClass("danger")) {
            $("#status_bg").removeClass("danger");
            $("#status_bg").addClass("success");
          }
          $("#status").html(
            "The TRS-398 Callibration values were added to the database successfully!"
          );
          $("#status_bg").removeClass("hidden");
          setTimeout(() => {
            $("#status_bg").addClass("hidden");
          }, 3000);
        }
        if (!data.success) {
          if ($("#status_bg").hasClass("success")) {
            $("#status_bg").removeClass("success");
          }
          $("#status_bg").addClass("danger");
          $("#status").html(
            "The TRS-398 data was NOT commited to the database, an ERROR occurred "
          );

          $("#status_bg").removeClass("hidden");
          setTimeout(() => {
            $("#status_bg").addClass("hidden");
          }, 3500);
        }

        setTimeout(() => {
          location.reload();
        }, 2000);
      },
    });
  });
});
