import React, { useState } from 'react';
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
import backgroundImg from '../assets/background.jpg'; 

const Admin_Dashboard = () => {
    const [selectedValue, setSelectedValue] = useState('Not Selected');
    const handleDropdownSelect = (value) => {
        setSelectedValue(value);
    };


  return (
    <div style={{
        backgroundImage: `url(${backgroundImg})`,
        backgroundSize: 'cover',
        minHeight: '100vh', 
      }}>
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
                        <MDBCard className="card">
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Mode Selection</MDBCardTitle>
                                <div>
                                    <p>Device in <span className={`text-danger`}>{selectedValue}</span> Mode</p>
                                    
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
                                        <MDBRadio name='flexRadioDefault' id='flexRadioDefault1' label='Security Level 1' disabled={selectedValue === 'Active'}/>
                                        <MDBRadio name='flexRadioDefault' id='flexRadioDefault2' label='Security Level 2' disabled={selectedValue === 'Active'}/>
                                        <MDBRadio name='flexRadioDefault' id='flexRadioDefault2' label='Security Level 3' disabled={selectedValue === 'Active'} defaultChecked/>
                                    </div>
                                    <div className="d-grid gap-2 d-md-flex justify-content-md-end mb-1">
                                        <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Selected'}>Apply</MDBBtn>
                                    </div>
                                    <br />
                                </div>
                            
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='6'>
                        <MDBCard className="card">
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">NOTE</MDBCardTitle>
                            <p>
                                <strong>Change security level</strong> - Change mode to configure and apply
                            </p>
                            <ul>
                                <li>Security Level 1 - Keypad</li>
                                <li>Security Level 2 - Keypad + Finger Print</li>
                                <li>Security Level 3 - Keypad + Finger Print + Camera</li>
                            </ul>
                            <p>
                                <strong>Add New Employee</strong> - Change mode to configure and Capture Image, Finger Print and Pin from New Employee
                            </p>
                            <p>
                                <strong>Update Device</strong> - Use this if there is issue with Raspberry pi Device
                            </p>
                            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                                <MDBBtn>Update Device</MDBBtn>
                            </div>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>

            <MDBContainer>
                <MDBRow>
                    <MDBCol sm='4'>
                        <MDBCard className="card">
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Image Capturing for New Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBInput label='New Employee Name' id='form1' type='text' />
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Selected'} className='mt-3'>capture</MDBBtn>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='4'>
                        <MDBCard className="card">
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Take Finger Print from New Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Selected'} className='mt-3'>Capture</MDBBtn>
                        </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                    <MDBCol sm='4'>
                        <MDBCard className="card">
                        <MDBCardBody>
                            <MDBCardTitle className="text-danger">Capture Pin from new Employee</MDBCardTitle>
                            <MDBCardText>
                                This will Enable only for Configure mode
                            </MDBCardText>
                            <MDBBtn disabled={selectedValue === 'Active' || selectedValue === 'Not Selected'} className='mt-3'>Capture</MDBBtn>
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
