import React,{ useState } from 'react';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput
}
from 'mdb-react-ui-kit';
import '../css/Signin.css';
import loginimage from '../assets/facerecog.png';
import { useNavigate} from 'react-router-dom';
import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';
import backgroundImg from '../assets/background.jpg'; 
import axios from "axios";

function Signin() {
  const navigate = useNavigate(); // Initialize the useNavigate hook
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // hadle authentication from django backend token
  const adminAuthentication = async() => {
    const user = {
      username: email,
      password: password
     };

     // Create the POST requuest
     const {data} = await                                                                            
     axios.post('https://face-secure.azurewebsites.net/token/',
     user ,{
       headers: {'Content-Type': 'application/json'},
       withCredentials: false,
     });

      console.log('Response:', data); // Log the response
     // Initialize the access & refresh token in localstorage.      
     localStorage.clear();
     localStorage.setItem('access_token', data.access);
     localStorage.setItem('refresh_token', data.refresh);
     axios.defaults.headers.common['Authorization'] = 
                                     `Bearer ${data['access']}`;
     //window.location.href = '/'
     navigate('/admin');
  }
  const handleSignin = (e) => {
    e.preventDefault();  // Prevent the default behaviour of the form submit button(reload the page)
    if (email == "aselahemantha"){
        adminAuthentication()
    }
    // This is for user login
    else{
      signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Signed in 
        console.log(userCredential);

        localStorage.clear();
        localStorage.setItem('access_token', userCredential._tokenResponse.idToken);
        localStorage.setItem('refresh_token', userCredential._tokenResponse.refreshToken);
        const email = userCredential.user.email;
      
        navigate('/user2' , { state: { email: email } }); // Use the push method to navigate to the user page
        
        
      }).catch((error) => {
        alert("Invalid Credentials")
      
        console.log(error);
      });
    }
  }

  

  const handleSignUpClick = () => {
    
    navigate('/signup'); // Use the push method to navigate to the signup page
    
  };


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
    <MDBContainer className="my-5 gradient-form" style={{ boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.2)', margin: '0 auto', maxWidth: '50%',backgroundColor: 'rgba(0,0,0, 0.2)',borderRadius: '15px',transition: 'transform 0.3s ease-in-out', 
        ':hover': {
          transform: 'scale(1.2)',
        },  }}>

          <div className="d-flex flex-column ms-4 me-4 mt-4 mb-4">

            <div className="text-center">
              <img src= {loginimage}
                style={{width: '185px',marginTop:20}} alt="logo" />
              <h4 className="mt-3 mb-3 pb-1" >Attedance Management System</h4>
            </div>

            <p>Please login to your account</p>


            <MDBInput wrapperClass='mb-4' label='Email address' id='form1' type='email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}/>


            <MDBInput wrapperClass='mb-4' label='Password' id='form2' type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}/>


            <div className="text-center pt-1 mb-3 pb-1">
              <MDBBtn className="mb-4 w-100 gradient-custom-2" onClick={handleSignin}>Sign in</MDBBtn>
              <a className="text-muted" href="#!">Forgot password?</a>
            </div>

            <div className="d-flex flex-row align-items-center justify-content-center mt-3 pb-1 mb-3">
              <p className="mb-2 mt-1">Don't have an account?</p>
              <MDBBtn outline className='mx-2' color='' onClick={handleSignUpClick}>
                Sign Up
              </MDBBtn>
            </div>

          </div>

        </MDBContainer>
      
        </div>
      
      );
    }


export default Signin;