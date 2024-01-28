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
    const [securityLevel, setSecurityLevel] = useState('level1');
    const [employees, setEmployees] = useState([]);
    const [selectedEmployeeId, setSelectedEmployeeId] = useState(null);
    const [selectedEmployeeFirstName, setSelectedEmployeeFirstName] = useState('');
    
    useEffect(() => {
        // Fetch data from the endpoint when the component mounts
        const fetchData = async () => {
          try {
            const response = await axios.get('https://facesecure.azurewebsites.net/attendanceManagement/get-no-face-employees/');
            setEmployees(response.data.employees_without_face);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
    
        fetchData(); // Call the fetch function
    }, []);

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true); 
        }
        else{
            navigate('/');
        }
       }, [isAuth]);
    

    const handleEmployeeSelect = (empId, firstName) => {
    setSelectedEmployeeId(empId);
    setSelectedEmployeeFirstName(firstName);
    };


    // trigger this when mode is active
    const onActiveMode = async () => {
        const activateData = {
            "mode" : "active",
            "level" : securityLevel,
            "topic" : 1
        };
      
        try {
        // Make a POST request with the constructed JSON object
        const response = await axios.post('https://facesecure.azurewebsites.net/attendanceManagement/active/', activateData, {
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
          const response = await axios.post('https://facesecure.azurewebsites.net/attendanceManagement/configure/', data, {
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
            "level" : securityLevel,
            "topic" : 1
        };

        handleConfigurePostRequest(securityLevelData);
    }

    // Train the face recognition model with new employees
    const handleUpdateDevice = () => {
        // Get the access token from local storage
        const accessToken = localStorage.getItem('access_token');

        // Make a GET request to fetch data with the access token included in the headers
        axios.get('https://facesecure.azurewebsites.net/attendanceManagement/encode-faces/', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
        })
        .then(response => {
            // Handle the response data here
            console.log('Response:', response.data);
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
        });
        
    };

    // Capture images for new employee
    const handleImageCapture = () => {
        
        // Construct JSON object based on the selected security level
        const Data = {
          "mode" : "configure",
          "cmd" : "capture_photo",
          "emp_id" : selectedEmployeeId,
          "emp_name" : selectedEmployeeFirstName,
          "topic" : 1
        };
        handleConfigurePostRequest(Data);
    };

    const handleFingerPrintCapture = () => {
        const data = {
          "mode" : "configure",
          "cmd" : "capture_finger",
          "emp_id" : selectedEmployeeId,
          "emp_name" : selectedEmployeeFirstName,
          "topic" : 1
        };
        handleConfigurePostRequest(data);
    };

    const handlePinCapture = () => {
        const data = {
          "mode" : "configure",
          "cmd" : "capture_pincode",
          "emp_id" : selectedEmployeeId,
          "emp_name" : selectedEmployeeFirstName,
          "topic" : 1
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
                                        checked = {securityLevel === 'level1'}
                                        onChange={() => handleRadioChange('level1')}
                                        />

                                        <MDBRadio 
                                        name='flexRadioDefault' 
                                        id='flexRadioDefault2' 
                                        label='Security Level 2' 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}
                                        checked = {securityLevel === 'level2'}
                                        onChange={() => handleRadioChange('level2')}
                                        />

                                        <MDBRadio 
                                        name='flexRadioDefault' 
                                        id='flexRadioDefault2' 
                                        label='Security Level 3' 
                                        disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}
                                        checked = {securityLevel === 'level3'}
                                        onChange={() => handleRadioChange('level3')}
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
                            <div>
                                {employees.length > 0 && (
                                <MDBDropdown dropright group className="mr-4" disabled={selectedValue === 'Active' || selectedValue === 'Not Configured'}>
                                <MDBDropdownToggle>
                                    {selectedEmployeeId ? (
                                    // Display the selected employee's name if one is selected
                                    `${selectedEmployeeFirstName} ${employees.find(emp => emp.emp_id === selectedEmployeeId).last_name}`
                                    ) : (
                                    // Show default text if no employee is selected
                                    'Select Employee'
                                    )}
                                </MDBDropdownToggle>
                                <MDBDropdownMenu>
                                    {employees.map(employee => (
                                    <MDBDropdownItem link childTag='button' key={employee.emp_id} onClick={() => handleEmployeeSelect(employee.emp_id, employee.first_name)}>
                                        {employee.first_name} {employee.last_name}
                                    </MDBDropdownItem>
                                    ))}
                                </MDBDropdownMenu>
                                </MDBDropdown>
                                )}
                            </div>
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