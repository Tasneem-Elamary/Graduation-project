

const baseURL = 'http://localhost:3000'
const patientID = localStorage.getItem('patientID')
let patient = {};



// function getData() {
        
//     axios({
//         method: 'get',
//         url: `${baseURL}/user`,
//         headers: { 'Content-Type': 'application/json; charset=UTF-8' },
       
//     }).then(function (response) {
//         console.log(response);
//         const { message, users } = response.data
//         patient = users
        
//         //showData()
//     }).catch(function (error) {
//         console.log(error);
//     });
// }

function getpatient() {
    console.log('getpatient')
    axios({
        method: 'get',
        url: `${baseURL}/user/${localStorage.getItem('patientID')}`,
        headers: { 'Content-Type': 'application/json; charset=UTF-8' }
    }).then(function (response) {
        const { message, user } = response.data;
        patient = user;
        
        showPatient();
        //console.log(user);
     
    }).catch(function (error) {
        console.log(error);
    });
}

function showPatient() {
    

        let cartonna = ` 

        <div class="form-group col-md-6">                                       
        <div class="row">
            <label for="patient-identifier" class="col-4">Patient identifier</label>
            <div class="col-8">${patient.identifier}</div>
        </div>
    </div>

    <div class="form-group col-md-6">
        <div class="row">
            <label for="phone" class="col-4">Phone</label>
            <div class="col-8">${patient.phone}</div>
        </div>
    </div>

    

    <div class="form-group col-md-6">                                           
        <div class="row">
            <label for="email" class="col-4">Email</label>
            <div class="col-8">${patient.Email}</div>
        </div>                                           
   </div>

    <div class="form-group col-md-6">
        <div class="row">
            <label for="age" class="col-4">Age</label>
            <div class="col-8">${patient.age}</div>

        </div>
    </div>
                        
    
    <div class="form-group col-md-6">
        <div class="row">
            <label for="gender" class="col-4">Gender</label>
            <div class="col-8">${patient.gender}</div>
        </div>                                            -->
    <!-- </div> -->`
       $('#orignal_img'). attr('src',`${patient.originalimage}`);
       $('#plugin-result-img'). attr('href',`${patient.originalimage}`);
       grade.innerText = `${patient.grade}`
       


    document.getElementById('result_container').innerHTML = cartonna
    localStorage.removeItem('patientID')
}

function createDate(dd){
    const date = new Date(dd);

let day = date.getDate();
let month = date.getMonth() + 1;
let year = date.getFullYear();

let currentDate = `${day}/${month}/${year}`;
console.log(currentDate); 
return  currentDate
}

getpatient();

function micro() { 
  console.log(patient);
  //document.getElementById("micro").classList.toggle("hideME");
//   console.log(patient.microimage)
  $('#orignal_img'). attr('src',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689595426/retinopathy/70832/ki4rutwwa4jmmarmk6oy.png");
  $('#plugin-result-img'). attr('href',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689595426/retinopathy/70832/ki4rutwwa4jmmarmk6oy.png");
}

function hemo() {
  //document.getElementById("hemo").classList.toggle("hideME");
  $('#orignal_img'). attr('src',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689594505/retinopathy/70845/lxwzksxrymvdflda5sxy.png");
   $('#plugin-result-img'). attr('href',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689594505/retinopathy/70845/lxwzksxrymvdflda5sxy.png");
}

function SE() {
  //document.getElementById("soft").classList.toggle("hideME");
  $('#orignal_img'). attr('src',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689595615/retinopathy/70832/bp98apumay7hdece1vri.png");
   $('#plugin-result-img'). attr('href',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689595615/retinopathy/70832/bp98apumay7hdece1vri.png");
}

function EX() {
//   console.log(patient.hardEXimage)
 // document.getElementById("hard").classList.toggle("hideME");
   $('#orignal_img'). attr('src',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689594296/retinopathy/70845/qiesia3jirjrj1wtivp0.png");
   $('#plugin-result-img'). attr('href',"https://res.cloudinary.com/dfvv2i9vk/image/upload/v1689594296/retinopathy/70845/qiesia3jirjrj1wtivp0.png");
}

// $("#hard").click(() => {
//   //console.log(patient)
//   // $('#orignal_img'). attr('src',`${patient.hardEXimage}`);
//   // $('#plugin-result-img'). attr('href',`${patient.hardEXimage}`);
// })



