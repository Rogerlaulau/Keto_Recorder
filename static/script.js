const form = document.getElementById('form');

const firstname = document.getElementById('fname');
const lastname = document.getElementById('lname');
const device_id = document.getElementById('device_id');
const gender = document.getElementById('gender');
const birthday = document.getElementById('birthday');
const weight = document.getElementById('weight');
const height = document.getElementById('height');
const keto_level = document.getElementById('keto_level');
const start_date = document.getElementById('start_date');
const test_date = document.getElementById('test_date');
const test_time = document.getElementById('test_time');
const remark = document.getElementById('remark');


const result = document.getElementById('result');
let login = 'admin'
let password = 'admin'


function showSummary() { 
    //window.open("http://keto.rogerlau.net/summary_page", "_blank");  //open in new tab
    window.open("http://keto.rogerlau.net/summary_page", "_self");     //open in the same tab
}


function createRecord(){
    
    const data_in = {"device_id": device_id.value, 
                    "firstname": firstname.value,
                    "lastname": lastname.value,
                    "gender": gender.value,
                    "birthday": birthday.value,
                    "weight": weight.value,
                    "height": height.value,
                    "keto_level": keto_level.value,
                    "start_date": start_date.value,
                    "test_date": test_date.value,
                    "test_time": test_time.value,
                    "remark": remark.value
                };
    
    fetch('http://keto.rogerlau.net/create', {
    method: 'POST', // or 'PUT'
    headers: {
        'Content-Type': 'application/json',
        "Authorization": `Basic ${btoa(`${login}:${password}`)}`
    },
    body: JSON.stringify(data_in),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        //outbound.innerHTML = JSON.stringify(data);
        if (data.status == 1){
            //result.innerHTML = "successful operation";
            firstname.value = "";
            lastname.value = "";
            //device_id.value = "";
            gender.value = "";
            birthday.value = "";
            weight.value = "";
            height.value = "";
            keto_level.value = "";
            start_date.value = "";
            test_date.value = "";
            test_time.value = "";
            remark.value = "";
            alert(`[Success]: You records are saved`);
        }
        else {
            //alert(`[Failure]: Invalid device ID: ${device_id.value}`);
            alert(`[Failure]: Please contact your admin with your device ID: ${device_id.value}`);
            //confirm("Press a button!");
            //prompt("Please enter your name", "Harry Potter");
        }
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


// Event listeners
form.addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('log:', firstname.value);
    //result.innerHTML = firstname.value;
    createRecord();
    // if(!checkRequired([groupname])){
    //   if (checkLength(groupname, 3, 15)){
    //       //showPosts();
    //       //createGroup();
    //       result.innerHTML = ''; //remove all child in this div
    //       //showPosts(); // to refresh the page
    //   }
    // }
  
});