$(document).ready(function () {
  $("#tem_pres_u").click(function (e) {
    e.preventDefault();
    console.log("the button is pressed");
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
              <td>${data.beam_data.date}</td>
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
              <td>${data.chamber_data.date}</td>
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
          $("#dose_dmax").text(d_zmax.toFixed(3));
        }
      },
    });

    if (!isNaN(avrg_reading)) {
      $("#val_btn").css("display", "none");
      $("#submit").css("display", "block");
      if ($("#status_bg").hasClass("danger")) {
        $("#status_bg").removeClass("danger");
        $("#status_bg").addClass("success");
        $("#status").text("The data was validated successfully!");
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
      $("#status").text(
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
    var m1 = $("#m1").val();
  });

  //This is the ast bracket anythin inside here wil be considered on document ready
});
