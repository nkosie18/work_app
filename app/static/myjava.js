$(document).ready(function(){
    $('#hello').text('Hello world! I have just changed the text in this paragraph using JQuery');
    
    $('#btn-0390').click(function(event){
        event.preventDefault();

        var serial_number = $('#serial').text();
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

            $('#refmeas_b').html(`
                <h1 style ="margin-top:-20mm;"> ${chamber_name}</h1>

                <p> Date: ${date} </p>
                <p> Electrometer: ${electrometer} </p>
                <p> Biasing Voltage: ${voltage}  </p>
                <p> Check Source: ${source} </p>
                <p> Decay Factor: ${decay_ref1} </p>
                <p> Exposure: ${ref_exposure} mGy</p>
            `)

            $('#chambhist').html(`
             
            <table id= "numbanumba" class = " w3-table-all">
            <tr>
            <th> Date </th>
            <th> Mean Exposure(mGy) </th>
            <th> Temperatur(0C) </th>
            <th> Pressure (mm Hg) </th>
            <th> Ktp </th>
            <th> Sr-90 Decay </th>
            <th> Exposure corr (mGy)  </th>
            <th> Percent Diff </th>
            </tr>
            </table>

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
                    <td> ${mean_exposure} </td>
                    <td> ${temp} </td>
                    <td> ${press} </td>
                    <td> ${ktp} </td>
                    <td> ${decay} </td>
                    <td> ${exposure_corr} </td>
                    <td> ${percent_diff} </td>
                    </tr>
                     `)

            }
 
            }
            
            

        })
        
         
    });

    $("#addmore").click(function(){
        $("#mytable").append("<tr><td>Mfeka</dt><td>J. P</dt><td>KZ003344</dt><td>10 MV</dt></tr>");
       });

    $('#addjson').click(function(event) {
    event.preventDefault();
    $.getJSON('b.json');
    })

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
    });


}); 

