$(document).ready(function(){
    $('#hello').text('Hello world! I have just changed the text in this paragraph using JQuery');
    
    

    $("#chambst").click(function(event){
        //event.preventDefault();
        

        var serial_number = event.target.id;
        //console.log(serial_number)
        req2 = $.ajax({ 
            url : '/chambViewProcess',
            type: 'POST',
            data: {sn:serial_number} 
        });
        req2.done(function(data){
            //const j = 2 == 2 ? console.log('The button works fine'):console.log("nothing")

            ///  The code that will run after the post responce has been rendered

            var chamber_name = data.chamb_name;
            var date = data.date_ref;
            var electrometer = data.electrometer_ref;
            var voltage = data.elect_voltage_ref;
            var source = data.source_ref;
            var decay_ref1 =  data.decay_ref;
            var ref_exposure = data.exposure_ref;

            $('#chambhist').css("display", "block");
            $('#refmeas_b').html(`
                <i><h2 style ="margin-top:-20mm;"> ${chamber_name}</h2></i>
                <p style="margin-top:-5mm;"><i> reference data</i></p>

                <table>
                <tr><td> Date: </td><td> <b> ${date}</b> </td></tr>
                <tr><td> Electrometer: </td><td><b>${electrometer}</b> </td></tr>
               <tr> <td> Biasing Voltage:</td><td> <b>${voltage} </b> </td></tr>
                <tr><td> Check Source: </td><td><b>${source} </b></td></tr>
                <tr><td> Decay Factor:</td><td><b> ${decay_ref1}</b> </td></tr>
                <tr><td> Exposure:</td><td><b> ${ref_exposure.toFixed(2)} mGy</b></td></tr>
                <tr></table>
            `)

            $('#chambhist').html(`
            <div class="w3-row">
            <div class="w3-col l8">
            <div class = "w3-responsive" style="background-color: #FAB340;">
            <table id= "numbanumba" class = " w3-table-all w3-small">
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
            </table>
            </div>

            <p style="margin-top:3mm;"> <i> <b>Table 2.</b> Previouse Sr-90 stability check measurements for ${chamber_name}. </i></p> <br><br>
            </div>
            <div class="w3-col l4"><p></p></div>
            </div>

            `)
            if(data.ref_only !== 'true'){

                var size = Object.keys(data.data).length;

                for (let i = 0; i<size; i++){
                    var date1 = data.data[i].date;
                    var mean_exposure = data.data[i].mean_exposure;
                    var temp = data.data[i].m_temp;
                    var press = data.data[i].m_press;
                    var ktp = data.data[i].ktp;
                    var decay = data.data[i].decay;
                    var exposure_corr = data.data[i].exposure_corr;
                    var percent_diff = data.data[i].percent_diff;
                    $('#numbanumba').append(`
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
                     `)

            }
 
            }

            
            
            

        });
        
        



        
         
    });


    /*
    $("#addmore").click(function(){
        $("#mytable").append("<tr><td>Mfeka</dt><td>J. P</dt><td>KZ003344</dt><td>10 MV</dt></tr>");
       });

    $('#addjson').click(function(event) {
    event.preventDefault();
    $.getJSON('b.json');
    });

    $('#check').click(function(){

        var name = $('#chamber').val();

        req = $.ajax({

            url : '/process',
            type : 'POST',
            data : {name : name}

        });

        req.done(function(data){

            $('#adddata').html('<h2>'+ data.name +'</h2> <br><br><br> <table class = "w3-table-all"> <tr><td>Calibration Lab</td><td>' + data.cal_lab + '</td></tr><tr><td>Calibration date</td><td>' +data. cal_date + '</td></tr><tr><td>Calibration factor</td><td>' + data.cal_factor + '</td></tr></table>'
                
                );
        });
    }); */


}); 

