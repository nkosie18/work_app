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

    if (isFloat(temp) && isFloat(press)) {
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

    $.ajax({
      type: "POST",
      url: "/trs_398/check_beam_data",
      data: { machine: machine, beam: beam, chamber: chamber },

      success: function (data) {
        if (data.success) {
        }
      },
    });
  });
});
