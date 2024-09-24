datefact = document.getElementById('id_datefact');
datenext = document.getElementById('id_datenext');
contact = document.getElementById('id_contact')
hint_org = document.getElementById('id_hint_organization');
hint_spec = document.getElementById('id_hint_special');

datefact.onchange = function () {
let dat2e =new Date(datefact.value);


let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let url = new URL('http://127.0.0.1:8000/hintwork');
url.searchParams.set('work', contact.value);
xhr.open('GET', url); 
xhr.send();

xhr.onload = function() {
if (xhr.status != 200) {
  datenext.value=''
} else {
  let cat
  let delta
  cat=xhr.response.category
  console.log(xhr.response.category)
  delta = 0
  if (cat=='A') {delta =15}
  if (cat=='B') {delta =30}
  console.log(delta)
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
xhr.responseType = 'json';
let url = new URL('http://127.0.0.1:8000/hintwork');
url.searchParams.set('work', contact.value);
xhr.open('GET', url); 
xhr.send();

xhr.onload = function() {
if (xhr.status != 200) {
  hint_org.value=''
  hint_spec.value=''
} else {

  hint_org.value=xhr.response.work
  hint_spec.value=xhr.response.spec
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

 


