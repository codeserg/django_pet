datefact = document.getElementById('id_datefact');
datenext = document.getElementById('id_datenext');
contact = document.getElementById('id_contact')
hint_org = document.getElementById('id_hint_organization');
hint_spec = document.getElementById('id_hint_special');

datefact.onchange = function () {
let dat2e =new Date(datefact.value);

let xhr = new XMLHttpRequest();

let url = new URL('http://mnopr.ru/hintwork');
url.searchParams.set('id', contact.value);
xhr.open('GET', url); 
xhr.send();

xhr.onload = function() {
if (xhr.status != 200) {
  datenext.value=''
} else {
  let cat
  let delta
 
  let prm= xhr.response.split('|')
  cat=prm[2]
  
  delta = 0
  if (cat=='A') {delta =15}
  if (cat=='B') {delta =30}
  
  if (delta !=0) {
    dat2e.setDate(dat2e.getDate()+delta)
    datenext.value=formatDate(dat2e)  
    }
    else {datenext.value=''}
}
};

};


contact.onchange = function () {

let xhr = new XMLHttpRequest();

let url = new URL('http://mnopr.ru/hintwork');
url.searchParams.set('id', contact.value);
xhr.open('GET', url); 
xhr.send();

xhr.onload = function() {
if (xhr.status != 200) {
  hint_org.value=''
  hint_spec.value=''
} else {
  
  let prm= xhr.response.split('|')

  hint_org.value=prm[0]
  hint_spec.value=prm[1]
  }
};

  
};


  function formatDate(date) {

    var dd = date.getDate();
    if (dd < 10) dd = '0' + dd;
  
    var mm = date.getMonth() + 1;
    if (mm < 10) mm = '0' + mm;
  
    var yy = date.getFullYear();

    var hh= date.getHours();
    if (hh < 10) hh = '0' + hh;
    
    var nu= date.getMinutes();
    if (nu < 10) nu = '0' + nu;
    

    return yy + '-' + mm + '-' + dd + ' ' + hh + ':' + nu;
  }

 

function splitString(stringToSplit, separator, index) {
    let arrayOfStrings = stringToSplit.split(separator)
 
    return  arrayOfStrings (index)

  }

