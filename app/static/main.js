
function storeCBCT(){
    var e = document.getElementById("unitSelection");
    var text_CBCT = e.options[e.selectedIndex].text;
    localStorage.setItem('unitname',text_CBCT);
}
function retrieve_cbct(){
    document.getElementById("unit").innerHTML = localStorage.getItem('unitname');
}

