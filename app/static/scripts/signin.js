$(document).ready(function () {
  function calc(a) {
    var number_fractions = $("#numbfr").val();
    var beam_numbe = $("#" + a).val();
    if (beam_numbe !== null || beam_numbe !== "Undefined") {
      var ans = (beam_numbe / number_fractions).toFixed(3);
      return ans;
    }
  }

  $("#calctbl").click(function (event) {
    var beam_id = event.target.id;
    var number_fractions = $("#numbfr").val();
    var my_beams = ["beam1", "beam2", "beam3", "beam4", "beam5"];
    if (number_fractions !== "") {
      if (my_beams.includes(beam_id)) {
        $("#" + beam_id).change(function () {
          var ref_dose = calc(beam_id);
          $("#ivdb" + beam_id[4]).text("Ref Dose: " + ref_dose + " Gy");
        });
      }
    }

    /*
            $('#'+ beam_id).change(function(){
                console.log('we are here now')
                if (my_beams.includes(beam_id)){
                    console.log('The beam id is in the list')
                    var ref_dose = calc(beam_id)
                    console.log(ref_dose)
                    $('#ivdb' + beam_id[4]).text('Ref Dose: '+ ref_dose + ' Gy')
                }
            });
            */
  });
});
