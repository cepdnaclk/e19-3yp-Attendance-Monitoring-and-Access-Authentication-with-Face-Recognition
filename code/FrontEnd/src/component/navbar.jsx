// Don't use this navbar for client component. superuser logout component mounted here.
import React from 'react';
import { MDBNavbar } from 'mdb-react-ui-kit';
import '../css/Signin.css';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

const Navbar = () => {
    const navigate = useNavigate();

    const handleUnlockDoor = async () => {
      try {
        // Define the JSON payload
        const payload = {
          "mode" : 'configure',
          "cmd" : 'unlock_door',
          "topic" : 1
        };
  
        // Send a POST request to the endpoint
        const response = await axios.post('https://facesecure.azurewebsites.net/attendanceManagement/configure/', payload, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you have an access token stored in localStorage
          }
        });
  
        // Handle the response if needed
        console.log('Unlock door response:', response.data);
      } catch (error) {
        // Handle errors
        console.error('Error unlocking door:', error);
      }
    };

    const handleLogout = async () => {
      console.log("logout is pressed")
      try {
        const response = await axios.post(
          'https://facesecure.azurewebsites.net/attendanceManagement/logout/',
          {
            refresh_token: localStorage.getItem('refresh_token'),
          },
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            withCredentials: false,
          }
        );
        
        //console.log('Response:', response); // Log the response
        localStorage.clear();
        axios.defaults.headers.common['Authorization'] = null;
        navigate('/');
      } catch (e) {
        console.log('Logout not working', e);
      }
    };

    const handleUserDetailsButton = () => {
      navigate('/user_details');
    };

  return (
    <MDBNavbar expand="lg" light bgColor="body-tertiary" className="gradient-custom-2">
      {/* Container wrapper */}
      <div className="container-fluid"> {/* Use container-fluid instead of container */}

        {/* Collapsible wrapper */}
        <div className="collapse navbar-collapse" id="navbarButtonsExample">
          {/* Left links */}
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
            <a 
                className="nav-link" 
                style={{ color: "white" }} 
                onClick={() => navigate('/admin')}
                onMouseEnter={(e) => e.target.style.color = 'black'} // Change color on hover
                onMouseLeave={(e) => e.target.style.color = 'white'} // Restore color when mouse leaves
            >
                Dashboard
            </a>
            </li>
          </ul>
          {/* Left links */}

          <div className="d-flex align-items-center mr-5">
            <button style={{ backgroundColor: "white", color: "black" }} className="btn px-3 me-2" onClick={handleUserDetailsButton}>
              User Details
            </button>
          </div>

          <div className="d-flex align-items-center mr-5">
            <button style={{ backgroundColor: "white", color: "black" }} className="btn btn-link px-3 me-2" onClick={handleUnlockDoor}>
              Unlock door
            </button>
          </div>

          <div className="d-flex align-items-center">
            <button style={{ backgroundColor: "white", color: "black" }} className="btn btn-link px-3 me-2" onClick={handleLogout}>
              Logout
            </button>
          </div>

          {/* <div className="d-flex align-items-center">     style prop was changed
            <button style={{color:"black"}} className="btn btn-link px-3 me-2" onClick={handleLogout}>
              Logout
            </button>
          </div> */}
        </div>
        {/* Collapsible wrapper */}
      </div>
      {/* Container wrapper */}
    </MDBNavbar>
  );
};

export default Navbar;
