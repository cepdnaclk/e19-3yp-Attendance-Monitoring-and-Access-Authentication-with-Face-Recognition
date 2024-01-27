import React, { useState, useEffect } from "react";
import backgroundImg from '../assets/background.jpg';
import UserNavbar from "../component/userNavbar";
import { useNavigate, useLocation } from 'react-router-dom';
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const User_Dashboard2 = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isAuth, setIsAuth] = useState(false);
    const { email } = location.state;
    const [userData, setUserData] = useState(null); // Set initial value to null or an empty object
    const [isLoading, setIsLoading] = useState(true);
    const currentDate = new Date().toLocaleDateString();
    const [selectedDate, setSelectedDate] = useState(null);

    const maxDate = new Date(); // Get current date
    maxDate.setDate(maxDate.getDate() - 1); // Subtract one day

    const handleDateChange = date => {
        setSelectedDate(date);
    };

    useEffect(() => {
        // Function to fetch user data based on the email
        const fetchUserData = async () => {
            try {
                // Make a GET request to fetch user data
                const response = await axios.get(`https://facesecure.azurewebsites.net/attendanceManagement/get-emp/${email}/`, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                
                const employee = response.data.Emp_detail;
                setUserData(employee);
                setIsLoading(false); // Set loading to false after data is fetched
            } catch (error) {
                // Handle errors
                console.error('Error:', error);
            }
        };
    
        // Call the fetchUserData function when the component mounts
        fetchUserData();
    }, [email]); // Add email to the dependency array to re-run the effect when email changes

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true); 
        } else {
            navigate('/');
        }
    }, [isAuth]);

    // Conditional rendering based on whether data is loaded
    if (isLoading || !userData) {
        return <div>Loading...</div>; // You can replace this with a loading spinner or any other UI indication
    }

    return (
        <div
            style={{
                backgroundImage: `url(${backgroundImg})`,
                backgroundSize: 'cover',
                minHeight: '100vh', 
            }}
        >
            <UserNavbar/>
            <h2 className="m-4">Hi, {userData.first_name} {userData.last_name} !...</h2>

            <MDBContainer>
                <MDBRow className="mt-5">
                    <MDBCol size='6'>
                        <h5><b>Employee ID</b> : {userData.emp_id}</h5>
                        <h5><b>First Name</b> : {userData.first_name}</h5>
                        <h5><b>Last Name</b> : {userData.last_name}</h5>
                        <h5><b>Department</b> : {userData.department}</h5>
                        <h5><b>Email</b> : {userData.emp_email}</h5>
                        <h5><b>Contact address</b> : {userData.contact_address}</h5>

                    </MDBCol>

                    <MDBCol size='6'>
                        <h2>Today</h2>
                        <h2>{currentDate}</h2>
                        <h2><b>Status :</b></h2>
                    </MDBCol>
                </MDBRow>

                <MDBRow className="mt-5">
                    <MDBCol size='6'>
                        <h2><b>SEARCH  </b> <MDBIcon fas icon="search" /> </h2>
                        <div className="mt-4">
                            <DatePicker
                                selected={selectedDate}
                                onChange={handleDateChange}
                                dateFormat="dd/MM/yyyy" // Adjust date format
                                minDate={null} // Disable future dates
                                maxDate={maxDate} // Disable future dates
                                inline
                                showDisabledMonthNavigation
                            />
                        </div>
                        
                    </MDBCol>
                    <MDBCol size='6'>
                        <p>this is 4</p>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        </div>
    );

}

export default User_Dashboard2;
