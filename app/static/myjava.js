$(document).ready(function(){
    
    

    $("#chambst").click(function(event){
        //event.preventDefault();
        

        var serial_number = event.target.id;
        //console.log(serial_number)
        if (serial_number !=''){
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
                    <p style="margin-top:-5mm;"><i> reference data</i></p> <br>
    
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
                
                
                
    
                `)
                $('#chambCal').html(`
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
                `)
    
                var size_cert = Object.keys(data.cert).length;
    
                for (let i =0; i<size_cert; i++){
                    var date_loaded = data.cert[i].date_loaded;
                    var loaded_by = data.cert[i].added_by;
                    var date_cal = data.cert[i].date_cal;
                    var cal_lab = data.cert[i].cal_lab;
                    var cal_factor = data.cert[i].ndw;
                    var electrometer_cert = data.cert[i].electrometer;
                    var bias_voltage = data.cert[i].voltage;
                    var beam_quality = data.cert[i].cal_energy;
                    
                    $('#calCertBody').append(`
    
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
    
                    `)
                    $('#calcert').DataTable({"lengthMenu": [[5, 10, -1], [5, 10, "All"]],
                    "aoColumns": [
                        { "orderSequence": [ "desc" ] },
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null
                    ]

                
                });
                    
    
                }
    
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
                        $('#chambHistBody').append(`
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

                    $('#numbanumba').DataTable({"lengthMenu": [[5, 10, -1], [5, 10, "All"]],
                    "aoColumns": [
                        { "orderSequence": [ "desc" ] },
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null
                    ]
                
                });
     
                }
    
                
                
                
    
            });
            
            
    
    
    
        }    
             
    });


        
    

    $("#linacs").click(function(event){
        var machine = event.target.id
        if(machine !== '' && machine !== 'linacs'){
            var i, tablinks
            tablinks = document.getElementsByClassName("tablink");
            for(i = 0; i < tablinks.length; i++){   
                tablinks[i].className = tablinks[i].className.replace(" w3-disabled", "");
            } 

            $('#' + machine).addClass('w3-disabled');
    

            if(document.getElementById("bodyup").style.display != "block"){
                console.log("the block was not showing so we showed it")
                $("#bodyup").css("display", "block")

            };
            tablinke = document.getElementsByClassName("tablinkr");
            for(i = 0; i < tablinke.length; i++){
                if(tablinke[i].className.includes("w3-disabled")){
                    qachecks2 = tablinke[i].id

                    console.log(machine)
                    console.log(qachecks2)

                    req_data = $.ajax({
                        url : '/linacViewProcess',
                        type: 'POST',
                        data: {machine_id:machine, test_name : qachecks2}
                    });
                }   
            };

           
            //$("#qabuttons").append(``);




            /*console.log(typeof(machine))
            req_linac = $.ajax({
                url : '/linacViewProcess',
                type: 'POST',
                data: {machine_id:machine}
            });
            }
            else{console.log('You did not click the button on the table')} */
        };
        

    });

    $("#qabuttons").click(function(event){
        var qachecks = event.target.id
        if(qachecks !== '' && qachecks !== 'qabuttons'){
        var i, j, tablinke, machine_stat
        tablinke = document.getElementsByClassName("tablinkr");
        for(i = 0; i < tablinke.length; i++){   
            tablinke[i].className = tablinke[i].className.replace(" w3-disabled", "")};
            
        }

        $('#' + qachecks).addClass('w3-disabled');

        machine_stat = document.getElementsByClassName("tablink");
        for(j=0; j<machine_stat.length; j++){
            if(machine_stat[j].className.includes("w3-disabled")){

                machine = machine_stat[j].id 
            }
        }
        var current_machine = machine
        var current_check = qachecks
    
        console.log(current_machine)
        console.log(current_check)

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

