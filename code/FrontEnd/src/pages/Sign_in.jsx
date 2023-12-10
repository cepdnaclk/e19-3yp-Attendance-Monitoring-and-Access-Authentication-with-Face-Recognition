import React from 'react';
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

function Signin() {

  
  return (
    <MDBContainer className="my-5 gradient-form" style={{ boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.2)'}}>

          <div className="d-flex flex-column ms-4 me-4 mt-4 mb-4">

            <div className="text-center">
              <img src= {loginimage}
                style={{width: '185px',marginTop:20}} alt="logo" />
              <h4 className="mt-3 mb-3 pb-1" >Attedance Management System</h4>
            </div>

            <p>Please login to your account</p>


            <MDBInput wrapperClass='mb-4' label='Email address' id='form1' type='email'/>
            <MDBInput wrapperClass='mb-4' label='Password' id='form2' type='password'/>


            <div className="text-center pt-1 mb-3 pb-1">
              <MDBBtn className="mb-4 w-100 gradient-custom-2">Sign in</MDBBtn>
              <a className="text-muted" href="#!">Forgot password?</a>
            </div>

            <div className="d-flex flex-row align-items-center justify-content-center mt-3 pb-1 mb-3">
              <p className="mb-2 mt-1">Don't have an account?</p>
              <MDBBtn outline className='mx-2' color=''>
                Sign Up
              </MDBBtn>
            </div>

          </div>

        </MDBContainer>
      );
    }


export default Signin;