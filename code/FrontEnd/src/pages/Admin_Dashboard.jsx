import React, { useState, useEffect } from 'react';
import { MDBCard,
    MDBContainer,
    MDBCardBody,
    MDBCardTitle,
    MDBCardText,
    MDBRow,
    MDBCol,
    MDBBtn,
    MDBDropdown, MDBDropdownMenu, MDBDropdownToggle, MDBDropdownItem,MDBRadio, MDBInput } from 'mdb-react-ui-kit';
import Navbar from '../component/navbar';
import { useNavigate} from 'react-router-dom';
import backgroundImg from '../assets/background.jpg';
import axios from 'axios';

const Admin_Dashboard = () => {
    const navigate = useNavigate(); // Initialize the useNavigate hook
    const [selectedValue, setSelectedValue] = useState('Not Configured');
    const [isAuth, setIsAuth] = useState(false);
    const [securityLevel, setSecurityLevel] = useState('easy');
    const [id, setId] = useState(0);
    const [newEmployee, setNewEmployee] = useState(''); 
    

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true); 
        }
        else{
            navigate('/');
        }
       }, [isAuth]);
    

    //generate a unique id for every new employee addition
    const generateId = () => {
        setId(prevId => {prevId+1})
    }

    const handleNameChange = (event) => {
        setNewEmployee(event.target.value);
      };

    // trigger this when mode is active
    const onActiveMode = async () => {
        const activateData = {
            "mode" : "activate",
            "sl" : securityLevel
        };
      
        try {
        // Make a POST request with the constructed JSON object
        const response = await axios.post('https://face-secure.azurewebsites.net/attendanceManagement/active/', activateData, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
        });
    
        // Handle the response as needed
        console.log('Response:', response.data);
        } catch (error) {
        // Handle errors
        console.error('Error:', error);
        }
    }   
    
    const handleDropdownSelect = (value) => {
        setSelectedValue(value);
        // if the mode is active give post request to backend
        if (value === 'Active'){
            onActiveMode();
        }
    };

    const handleRadioChange = (value) => {
        setSecurityLevel(value);
    };

    const handleConfigurePostRequest = async (data) => {
        // data is the json object to send to backend
    
        try {
          // Make a POST request with the constructed JSON object
          const response = await axios.post('https://face-secure.azurewebsites.net/attendanceManagement/configure/', data, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
    
          // Handle the response as needed
          console.log('Response:', response.data);
        } catch (error) {
          // Handle errors
          console.error('Error:', error);
        }
    };

    const handleApplyButton = () => {
        const securityLevelData = {
            "mode" : "configure",
            "cmd" : "change_level",
            "sl" : securityLevel
        };

        handleConfigurePostRequest(securityLevelData);
    }

    // Train the face recognition model with new employees
    const handleUpdateDevice = () => {
        // Construct JSON object based on the selected security level
        const updateData = {
          "mode" : "configure",
          "cmd" : "update_device"
        };
        handleConfigurePostRequest(updateData);
    };

    // Capture images for new employee
    const handleImageCapture = () => {
        //generate a id for the employee
        generateId();
        // Construct JSON object based on the selected security level
        const Data = {
          "mode" : "configure",
          "cmd" : "capture_image",
          "id" : id,
          "name" : newEmployee
        };
        handleConfigurePostRequest(Data);
    };

    const handleFingerPrintCapture = () => {
        const data = {
          "mode" : "configure",
          "cmd" : "capture_fp",
          "id" : id,
          "name" : newEmployee
        };
        handleConfigurePostRequest(data);
    };

    const handlePinCapture = () => {
        const data = {
          "mode" : "configure",
          "cmd" : "capture_pin",
          "id" : id,
          "name" : newEmployee
        };
        handleConfigurePostRequest(data);
    };


    if (!isAuth) {
        return null;
    }

  return (
    <div
    style={{
        backgroundImage: `url(${backgroundImg})`,
        backgroundSize: 'cover',
        minHeight: '100vh', 
      }}
    >
        <div style={{ width: '100%', marginLeft:0, top: 0, zIndex: 1000 }}>
            <Navbar />
        </div>
        <div>
            <h1 className='mt-2 text-center mb-3'>Admin Dashboard</h1>
        </div>
        <div>
            <MDBContainer className='mb-5'>
                <MDBRow>
                    <MDBCol sm='6'>
                        <MDBCard>
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Mode Selection</MDBCardTitle>
                                <div  style={{color:"black"}}>
                                    <p>Device in <span className={"text-danger"}>{selectedValue}</span> Mode</p>
                                    
                                    <div>
                                        <MDBDropdown>
                                        <MDBDropdownToggle>click here to change</MDBDropdownToggle>
                                        <MDBDropdownMenu>
                                            <MDBDropdownItem link onClick={() => handleDropdownSelect("Active")}>Active</MDBDropdownItem>
                                            <MDBDropdownItem link onClick={() => handleDropdownSelect("Configure")}>Configure</MDBDropdownItem>
                                        </MDBDropdownMenu>
                                        </MDBDropdown>
                                    </div>
                                    <div className='mt-5'>
                                        <MDBRadio
                                        name='flexRadioDefault' 
                                        id='flexRadioDefault1' 
                                        label='Security Level 1' 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'} 
                                        checked = {securityLevel === 'easy'}
                                        onChange={() => handleRadioChange('easy')}
                                        />

                                        <MDBRadio 
                                        name='flexRadioDefault' 
                                        id='flexRadioDefault2' 
                                        label='Security Level 2' 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}
                                        checked = {securityLevel === 'meadium'}
                                        onChange={() => handleRadioChange('meadium')}
                                        />

                                        <MDBRadio 
                                        name='flexRadioDefault' 
                                        id='flexRadioDefault2' 
                                        label='Security Level 3' 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}
                                        checked = {securityLevel === 'hard'}
                                        onChange={() => handleRadioChange('hard')}
                                        />
                                    </div>
                                    <div className="d-grid gap-2 d-md-flex justify-content-md-end mb-1">
                                        <MDBBtn 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}
                                        onClick={handleApplyButton}>
                                            Apply
                                        </MDBBtn>
                                    </div>
                                    <br />
                                </div>
                            
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='6'>
                        <MDBCard  style={{color:"black"}}>
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">NOTE</MDBCardTitle>
                            <p>
                                <strong>Change security level</strong> - Change mode to configure and apply
                            </p>
                            <ul>
                                <li>Security Level 1 - Only Attendance marking through camera</li>
                                <li>Security Level 2 - Attendance marking + finger print door unlock</li>
                                <li>Security Level 3 - Attendance marking + finger print + keypad for door unlock</li>
                            </ul>
                            <p>
                                <strong>Add New Employee</strong> - Change mode to configure and Capture Image, Finger Print and Pin from New Employee
                            </p>
                            <p>
                                <strong>Update Device</strong> - Use this after adding new employee data
                            </p>
                            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                                <MDBBtn onClick={handleUpdateDevice}>Update Device</MDBBtn>
                            </div>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>

            <MDBContainer>
                <MDBRow>
                    <MDBCol sm='4'>
                        <MDBCard  style={{color:"black"}}>
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Image Capturing for New Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBInput label='New Employee Name' id='form1' type='text' value={newEmployee} onChange={handleNameChange}/>
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'} className='mt-3' onClick={handleImageCapture}>capture</MDBBtn>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='4'>
                        <MDBCard  style={{color:"black"}}>
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Take Finger Print from New Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'} className='mt-3' onClick={handleFingerPrintCapture}>Capture</MDBBtn>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='4'>
                        <MDBCard  style={{color:"black"}}>
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Capture Pin from new Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'} className='mt-3' onClick={handlePinCapture}>Capture</MDBBtn>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        </div>
    </div>
  );
};

export default Admin_Dashboard;