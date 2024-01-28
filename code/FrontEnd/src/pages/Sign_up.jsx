import React, { useState} from 'react';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput
}
from 'mdb-react-ui-kit';
import '../css/Signup.css';
import loginimage from '../assets/facerecog.png';
import { useNavigate} from 'react-router-dom';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import backgroundImg from '../assets/background.jpg'; 
import axios from 'axios';


function Signup() {
  const navigate = useNavigate(); // Initialize the useNavigate hook

  const [firstname, setFirstname] = useState('');
  const [lastname, setLastname] = useState('');
  const [gender, setGender] = useState('');
  const [age, setAge] = useState('');
  const [number, setNumber] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmpassword, setConfirmpassword] = useState('');
  const [depname, setDepname] = useState('');
  const [address, setAddress] = useState('');

  const handleGenderChange = (e) => {
    setGender(e.target.value);
  };  
  const handleDepartmentChange = (e) => {
    setDepname(e.target.value);
  };

  const saveUserData = async (data) => {
    try {
      // Make a POST request with the constructed JSON object
      const response = await axios.post('https://facesecure.azurewebsites.net/attendanceManagement/save-employee/', data, {
          headers: {
              'Content-Type': 'application/json',
          },
      });
  
      // Handle the response as needed
      console.log('Response:', response.data);
      } catch (error) {
      // Handle errors
      console.error('Error:', error);
      }
  }


  const handleSignup = (e) => {
    e.preventDefault();  // Prevent the default behaviour of the form submit button(reload the page)

    let data;
    // password confirmpassword logic
    if(password !== confirmpassword){
      alert('pasword mismatch');
      setPassword('');
      setConfirmpassword('');
      return;
    }
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      //save data in database
      data = {
        'first_name' : firstname,
        'last_name' : lastname,
        'gender' : gender,
        'age' : parseInt(age),
        'contact_address' : address,
        'mobile_number' : number,
        'emp_email' : email,
        'department' : parseInt(depname),
        'face_state' : false,
        'fp_state' : false
      };

      saveUserData(data);
      
      
      console.log(userCredential);
      navigate('/'); // Use the push method to navigate to the signin page
      // ...
    }).catch((error) => {
      //const errorCode = error.code;
      //const errorMessage = error.message;
      console.log(error);
    });
  }

  const handleSigin = () => {
    navigate('/'); // Use the push method to navigate to the signin page
  }

  return (
    <div
    style={{
      backgroundImage: `url(${backgroundImg})`,
      backgroundSize: 'cover',
      minHeight: '100vh', 
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}
    >
    <MDBContainer className="my-5 gradient-form" style={{ boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.2)', margin: '0 auto', maxWidth: '50%',backgroundColor: 'rgba(255, 255, 255, 0.9)',borderRadius: '15px',transition: 'transform 0.3s ease-in-out'}}>

          <div className="d-flex flex-column ms-4 me-4 mt-4 mb-4">

            <div className="text-center">
              <img src= {loginimage}
                style={{width: '185px',marginTop:20}} alt="logo" />
              <h4 className="mt-1 mb-2 pb-1" >Attedance Management System</h4>
            </div>

            <p style={{fontSize:'20px'}}>Please enter your details</p>


            <MDBInput wrapperClass='mb-3' label='First name' id='form1' type='text'
            value={firstname}
            style={{ color: '#318CE7' }}
            onChange={(e) => setFirstname(e.target.value)}/>


            <MDBInput wrapperClass='mb-3' label='Last name' id='form2' type='text'
            value={lastname}
            style={{ color: '#318CE7' }}
            onChange={(e) => setLastname(e.target.value)}/>

           {/* <div className="mb-3" style={{ color: '#318CE7' }}>
                <select
                  id="form3"
                  className="form-select" 
                  value={gender}
                  onChange={handleGenderChange}
                >
                  <option value="">Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div> */}
            <MDBInput wrapperClass='mb-3' label='Gender' id='form3' type='text'
            value={gender}
            style={{ color: '#318CE7' }}
            onChange={(e) => setGender(e.target.value)}/>


            <MDBInput wrapperClass='mb-3' label='Age' id='form4' type='text'
            value={age}
            style={{ color: '#318CE7' }}
            onChange={(e) => setAge(e.target.value)}/>
            <MDBInput wrapperClass='mb-3' label='Contact number ' id='form5' type='text'
            value={number}
            style={{ color: '#318CE7' }}
            onChange={(e) => setNumber(e.target.value)}/>
            <MDBInput wrapperClass='mb-3' label='Email address' id='form6' type='email'
            value={email}
            style={{ color: '#318CE7' }}
            onChange={(e) => setEmail(e.target.value)}/>

            <MDBInput wrapperClass='mb-3' label='Password' id='form7' type='password'
            value={password}
            style={{ color: '#318CE7' }}
            onChange={(e) => setPassword(e.target.value)}/>


            <MDBInput wrapperClass='mb-3' label='Confirm your password' id='form8' type='password'
            value={confirmpassword}
            style={{ color: '#318CE7' }}
            onChange={(e) => setConfirmpassword(e.target.value)}/>

            {/* <div className="mb-3" style={{ color: '#318CE7' }}>
               
                <select
                  id="form9"
                  className="form-select" 
                  value={depname}
                  onChange={handleDepartmentChange}
                >
                  <option value="">Department</option>
                  <option value="com">Department of Computer Engineering</option>
                  <option value="elec">Department of Electrical Engineering</option>
                  <option value="management">Department of Management</option>
                </select>
              </div> */}

            <MDBInput wrapperClass='mb-3' label='Department name' id='form9' type='text'
            value={depname}
            style={{ color: '#318CE7' }}
            onChange={(e) => setDepname(e.target.value)}/>

            <MDBInput wrapperClass='mb-3' label='Contact address' id='form10' type='text'
            value={address}
            style={{ color: '#318CE7' }}
            onChange={(e) => setAddress(e.target.value)}/>

            <div className="text-center pt-1 mb-3 pb-1">
              <MDBBtn className="mb-1 w-100 gradient-custom-2" onClick={handleSignup}>Sign up</MDBBtn>
              
            </div>

            <div className="d-flex flex-row align-items-center justify-content-center mt-0 pb-1 mb-3">
              <p className="mb-2 mt-1">Do you have an account?</p>
              <MDBBtn outline className='mx-2' color='' onClick={handleSigin}>
                Sign in
              </MDBBtn>
            </div>

          </div>

        </MDBContainer>
        </div>
      );
    }
    

export default Signup;

