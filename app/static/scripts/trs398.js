$(document).ready(function () {
  $("#tem_pres_u").click(function (e) {
    e.preventDefault();
    $(".tp_table").hide();
    $("#tem_pres_u").hide();
    $(".update_env").show();
  });

  function isInt(n) {
    return Number(n) === n && n % 1 === 0;
  }

  function isFloat(n) {
    return Number(n) === n && n % 1 !== 0;
  }

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

  $("#beam_data").click(function (e) {
    e.preventDefault();
    var machine = $("#machine_tag").text();
    var beam = $("#sele_beam").find(":selected").text();
    var chamber = $("#sele_chamber").find(":selected").text();
    $("#beamDataStatus").val("Active");

    $.ajax({
      type: "POST",
      url: "/trs_398/check_beam_data",
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
              <td><b>TPR<sub>20,10</sub> :</b></td>
              <td id = "tpr_2010_data">${data.beam_data.tpr2010}</td>
            </tr>
            <tr>
            <td><b>PDD<sub>10</sub> :</b></td>
            <td id = "pdd_10_data">${data.beam_data.pdd10.toFixed(1)}</td>
          </tr>
            <tr>
              <td><b>K<sub>Q,Q0</sub> :</b></td>
              <td id = "beam_quality_corr">${data.beam_data.k_corr}</td>
            </tr>
            `
          );
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
        } else {
          if ($("#status_bg").hasClass("success")) {
            $("#status_bg").removeClass("success");
          }
          $("#status_bg").addClass("danger");
          $("#status").html(data.message);

          $("#status_bg").removeClass("hidden");
          setTimeout(() => {
            $("#status_bg").addClass("hidden");
          }, 3000);
        }
      },
    });
  });

  $("#readings_col").change(function (event) {
    event.preventDefault();
    var ndw = parseFloat($("#ndw_corr").text().split(" ")[0]);
    var k_corr = parseFloat($("#beam_quality_corr").text());
    var pdd10 = parseFloat($("#pdd_10_data").text());
    var temp = $("#temp_d").text();
    var press = $("#pres_d").text();

    var k_tp =
      (1013.2 / parseFloat(press.split(" ")[0])) *
      ((parseFloat(temp.split(" ")[0]) + 273.2) / 293.2);

    if ($("#beamDataStatus").val() === "Active") {
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
    var d_zmax = d_zref / (pdd10 / 100);
    $("#dose_dmax").text(d_zmax.toFixed(3));
  });

  $("#val_btn").click(function (e) {
    e.preventDefault();

    var ndw = parseFloat($("#ndw_corr").text().split(" ")[0]);
    var k_corr = parseFloat($("#beam_quality_corr").text());
    var pdd10 = parseFloat($("#pdd_10_data").text());
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
        var thirdReading_1 = ((m1 + m2) / 2).toFixed(1);
        $("#m13_reading").val(thirdReading_1);
        m3 = parseFloat(thirdReading_1);
        break;

      default:
        m1 = parseFloat($("#m11_reading").val());
        m2 = parseFloat($("#m12_reading").val());
        m3 = parseFloat($("#m13_reading").val());
        break;
    }

    avrg_reading = ((m1 + m2 + m3) / 3).toFixed(1);

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
          var d_zmax = d_zref / (pdd10 / 100);
          $("#mref").text(avrg_reading);
          $("#ndw").text(ndw);
          $("#kqq").text(k_corr);
          $("#ktp").text(k_tp.toFixed(3));
          $("#ks").text(k_s);
          $("#pdd").text(pdd10);
          $("#dose_dmax").text(d_zmax.toFixed(3));
        } else {
          if ($("#status_bg").hasClass("success")) {
            $("#status_bg").removeClass("success");
          }
          $("#status_bg").addClass("danger");
          $("#status").html(data.message);

          $("#status_bg").removeClass("hidden");
          setTimeout(() => {
            $("#status_bg").addClass("hidden");
          }, 3000);
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

  $("#next_beam").click(function (e) {
    e.preventDefault();
    //work on adding data for here so we can move on to ellectron beams
    var v1 = $("#bias_voltage1").find(":selected").text();
    var m1 = $("#m11_reading").val();
    var m2 = $("#m12_reading").val();
    var m3 = $("#m13_reading").val();
    var ndw = parseFloat($("#ndw_corr").text());
    var m_avrg_reading = parseFloat($("#mref").text());
    var kqq1 = parseFloat($("#kqq").text());
    var ktp1 = parseFloat($("#ktp").text());
    var ks1 = parseFloat($("#ks").text());
    var dose_ref = (m_avrg_reading * ndw * kqq1 * ktp1 * ks1).toFixed(3);
    console.log(
      "Dose_ref: " +
        dose_ref +
        ", M_avrg: " +
        m_avrg_reading +
        ", Ndw: " +
        ndw +
        ", kqq: " +
        kqq1 +
        ", ktp: " +
        ktp1 +
        ", ks: " +
        ks1
    );
    var v2 = $("#bias_voltage2").find(":selected").text();
    var m21 = $("#m21_reading").val();
    var m22 = $("#m22_reading").val();

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
    console.log(beam_data_date);
    $.ajax({
      type: "POST",
      url: "/trs398/photons_2",
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
        dose_ref: dose_ref,
        beam_data_date: beam_data_date,
      },
      success: function (data) {
        if (data.success) {
          if ($("#status_bg").hasClass("danger")) {
            $("#status_bg").removeClass("danger");
            $("#status_bg").addClass("success");
          }
          $("#status").html(
            "The TRS-309 values were added to the database successfully!"
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
          $("#status").text(
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

  //This is the ast bracket anythin inside here wil be considered on document ready
});
