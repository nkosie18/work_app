$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/sr_checks/checkConnection",
    success: function (data) {
      if (data["status"] == "success") {
        $(".success-alert").text(
          "An electrometer: " + data["electrometer"] + "was found"
        );
        alert_message("success-alert");
        $(".electrometer1").text(data["electrometer"] + " connected!");
        $(".electrometer1").removeClass("w3-pale-red");
        $(".electrometer1").addClass("w3-pale-green");
        $("#connect").css("display", "none");
        $("#disconnect").css("display", "block");
      }
    },
  });

  function alert_message(alert) {
    //$("." + alert).css("display", "block");
    $("." + alert).fadeIn(500);
    setTimeout(function () {
      $("." + alert).hide();
    }, 3000);
  }

  $("#connect").click(function (e) {
    e.preventDefault();
    var chamber = $(".selected_chamber :selected").text();
    var electrometer = $(".selected_electrometer :selected").text();
    var source = $(".selected_source :selected").text();

    console.log(electrometer);

    if ((electrometer = "UNIDOS 1")) {
      alert_message("connecting-alert");
      setTimeout(function () {
        $.ajax({
          type: "GET",
          url: "/sr_checks/connect electrometer",
          success: function (data) {
            if (data["status"] == "success") {
              $(".connecting-alert").css("display", "none");
              alert_message("success-alert");
              $(".electrometer1").text(data["electrometer"] + " connected!");
              $(".electrometer1").removeClass("w3-pale-red");
              $(".electrometer1").addClass("w3-pale-green");
              $("#connect").css("display", "none");
              $("#disconnect").css("display", "block");
              $("#null").css("display", "none");
            }
            if (data["status"] == "failor") {
              alert_message("failed-alert");
            }
          },
        });
      }, 2000);
    }
  });

  $("#disconnect").click(function (e) {
    e.preventDefault();

    $.ajax({
      type: "GET",
      url: "/sr_checks/disconnect electrometer",
      success: function (data) {
        if (data["status"] == "success") {
          $(".failed-alert").text("Electrometer disconnected successfully.");
          alert_message("failed-alert");
          $(".electrometer1").text("NO Electrometer Connected");
          $(".electrometer1").addClass("w3-pale-red");
          $(".electrometer1").removeClass("w3-pale-green");
          $("#connect").css("display", "block");
          $("#start_meas").css("display", "none");
          $("#disconnect").css("display", "none");
          $("#null").css("display", "none");
        }
      },
    });
  });

  $("#start_meas").click(function (e) {
    e.preventDefault();
    var selected_ch = $("#chamb_list :selected").text();
    var electrometer = $(".selected_electrometer :selected").text();
    var source = $(".selected_source :selected").text();
    $("#disconnect").css("display", "none");
    $("#null").css("display", "none");
    $(".success-alert").text("Measurements started successfully.");
    alert_message("success-alert");
    $(".electrometer1").text("Measurement in Progress....");
    setTimeout(function () {
      $("#start_meas").css("display", "none");
    }, 1000);
    $(".m_inProgress").css("display", "block");
    $.ajax({
      type: "POST",
      url: "/sr_checks/auto_measure",
      data: {
        selected_chamber: selected_ch,
        selected_electrometer: electrometer,
        selected_source: source,
      },
      success: function (data) {
        if (data["status"] == "success") {
          $(".m_inProgress").css("display", "none");
          $(".m_comSuccess").css("display", "block");
        }
      },
    });
  });

  // $("#next_m").click(function (e) {
  //   e.preventDefault();
  //   location.reload();
  // });

  $("#null").click(function (e) {
    e.preventDefault();

    $(".success-alert").text("Nulling electrometer started successfully.");
    alert_message("success-alert");
    $(".electrometer1").text("Nulling electrometer in Progress....");
    setTimeout(function () {
      $("#null").css("display", "none");
      $("#disconnect").css("display", "none");
      $("#start_meas").css("display", "none");
    }, 1000);
    $.ajax({
      type: "GET",
      url: "/sr_checks/null",
      success: function (data) {
        if (data["status"] == "success") {
          $(".success-alert").text(
            "Nulling electrometer completed successfully."
          );
          alert_message("success-alert");
          setTimeout(function () {
            location.reload();
          }, 2000);
        }
        if (data["status"] == "failor") {
          $(".failed-alert").text(data["message"]);
          alert_message("failed-alert");
          $(".electrometer1").text("Nulling of Electrometer Not Possible....");
        }
      },
    });
  });

  // $.ajax({
  //   type: "GET",
  //   url: "/sr_checks/chamber_list",
  //   success: function (data) {
  //     var list_chamb_available = data.chamb_list_todo;
  //     var list_chamb_unavailable = data.chamb_list_done;

  //     for (var i = 0; list_chamb_available.length - 1; i++) {
  //       $("#chamb_list").append(
  //         '<option value="' +
  //           list_chamb_available[i] +
  //           '">' +
  //           list_chamb_available[i] +
  //           "</option>"
  //       );
  //     }
  //   },
  // });
});
