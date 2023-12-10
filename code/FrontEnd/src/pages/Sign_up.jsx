import React, { useState} from 'react';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput
}
from 'mdb-react-ui-kit';
import '../css/signin.css';
import loginimage from '../assets/facerecog.png';
import { useNavigate} from 'react-router-dom';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';


function Signup() {
  const navigate = useNavigate(); // Initialize the useNavigate hook

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();  // Prevent the default behaviour of the form submit button(reload the page)
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in 
      
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
    <MDBContainer className="my-5 gradient-form" style={{ boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.2)'}}>

          <div className="d-flex flex-column ms-4 me-4 mt-4 mb-4">

            <div className="text-center">
              <img src= {loginimage}
                style={{width: '185px',marginTop:20}} alt="logo" />
              <h4 className="mt-3 mb-3 pb-1" >Attedance Management System</h4>
            </div>

            <p>Please enter your details</p>


            <MDBInput wrapperClass='mb-4' label='Email address' id='form1' type='email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}/>


            <MDBInput wrapperClass='mb-4' label='Password' id='form2' type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}/>


            <div className="text-center pt-1 mb-3 pb-1">
              <MDBBtn className="mb-4 w-100 gradient-custom-2" onClick={handleSignup}>Sign up</MDBBtn>
              
            </div>

            <div className="d-flex flex-row align-items-center justify-content-center mt-3 pb-1 mb-3">
              <p className="mb-2 mt-1">Do you have an account?</p>
              <MDBBtn outline className='mx-2' color='' onClick={handleSigin}>
                Sign in
              </MDBBtn>
            </div>

          </div>

        </MDBContainer>
      );
    }
    {/* <MDBRow> */}

      {/* <MDBCol col='2' className="mb-5"> */}

      // ---

        {/* </MDBCol> */}
        
        {/* <MDBCol col='6' className="mb-5">
          <div className="d-flex flex-column  justify-content-center gradient-custom-2 h-100 mb-4">

            <div className="text-white px-3 py-4 p-md-5 mx-md-4">
              <h4 class="mb-4">We are more than just a company</h4>
              <p class="small mb-0">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
                exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </p>
            </div>

          </div>

        </MDBCol> */}

      {/* </MDBRow> */}


export default Signup;