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
        console.log(data["electrometer"]);
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
            }
            if (data["status"] == "failor") {
              alert_message("failed-alert");
            }
          },
        });
      }, 3000);
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
          $("#disconnect").css("display", "none");
        }
      },
    });
  });
});
