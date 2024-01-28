import React, { useState, useEffect } from "react";
import backgroundImg from '../assets/background.jpg';
import UserNavbar from "../component/userNavbar";
import { useNavigate, useLocation } from 'react-router-dom';
import { MDBContainer, MDBRow, MDBCol, MDBIcon, MDBTable, MDBTableHead, MDBTableBody } from 'mdb-react-ui-kit';
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
    const [selectedMonth, setSelectedMonth] = useState(1);
    const [attendanceData, setAttendanceData] = useState([]);

    const [Month, setMonth] = useState(null);
    const [Day, setDay] = useState(null);
    const [Year, setYear] = useState(null);
    const [presentStates, setPresentStates] = useState([]);
    const [inTimes, setInTimes] = useState([]);
    const [status, setStatus] = useState('');

    useEffect(() => {
        if (userData) {
            const fetchAttendanceData = async () => {
                try {
                    const response = await axios.get(`https://facesecure.azurewebsites.net/attendanceManagement/get-attendance-date-emp/${userData.emp_id}/2024/1/29/`);
                    const attendanceDetails = response.data.attendance_details;
                    const present = attendanceDetails.length > 0 ? attendanceDetails[0].present : false;
                    setStatus(present ? 'Present' : 'Absent');
                } catch (error) {
                    console.error('Error fetching attendance data:', error);
                }
            };

            fetchAttendanceData();
        }
    }, [userData]);

    const handleMonthChange = date => {
        setSelectedMonth(date.getMonth() + 1); // Get the month (0-indexed) and add 1 to get the month number (1-indexed)
    };

    const renderMonthContent = (month, shortMonth, longMonth, day) => {
        const fullYear = new Date(day).getFullYear();
        const tooltipText = `Select month: ${longMonth} ${fullYear}`;

        return <span title={tooltipText}>{shortMonth}</span>;
    };

    // set max date that can query by user
    const maxDate = new Date(); // Get current date
    maxDate.setDate(maxDate.getDate() - 1); // Subtract one day

    const fetchAttendanceData = async (id, day, month, year) => {
        try {
            // Construct the URL with the provided parameters
            const url = `https://facesecure.azurewebsites.net/attendanceManagement/get-attendance-date-emp/${id}/${year}/${month}/${day}/`;
    
            // Make a GET request to fetch the attendance data
            const response = await axios.get(url, {
                headers: {
                    'Content-Type': 'application/json',
                    
                },
            });
    
            // Extract the attendance details from the response
            const { attendance_details } = response.data;
    
            // Extract present state and in_time from each attendance detail
            const presentStates = attendance_details.map(detail => detail.present);
            const inTimes = attendance_details.map(detail => detail.in_time);
    
            // Update the state variables with the extracted data
            setPresentStates(presentStates);
            setInTimes(inTimes);

            console.log(day,"month", month);
            console.log(presentStates)
        } catch (error) {
            // Handle errors
            console.error('Error fetching attendance data:', error);
        }
    };

    const handleDateChange = date => {
        setSelectedDate(date);

        // Get the month, day, and year of the selected date
        const month = date.getMonth() + 1; // Months are zero-based, so add 1 to get the correct month
        const day = date.getDate();
        const year = date.getFullYear();


        // Set the state variables
        setMonth(month);
        setDay(day);
        setYear(year);

        fetchAttendanceData(userData.emp_id, day, month, year);
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
        // Check if userData is defined before fetching attendance data
        if (userData && selectedMonth) {
            // Fetch attendance data based on employee id (e.g., 1) and selected month (e.g., 1 for January)
            axios.get(`https://facesecure.azurewebsites.net/attendanceManagement/get-attendance/${userData.emp_id}/${selectedMonth}/`)
                .then(response => {
                    setAttendanceData(response.data.attendance_details);
                })
                .catch(error => {
                    console.error('Error fetching attendance data:', error);
                });
        }
    }, [userData, selectedMonth]); // Add userData and selectedMonth to the dependency array

    // useEffect(() => {
    //     console.log("Attendance data:", attendanceData);
    // }, [attendanceData]);


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
                        <h5><b>Email</b> : {userData.emp_email}</h5>
                        <h5><b>Contact address</b> : {userData.contact_address}</h5>

                    </MDBCol>

                    <MDBCol size='6'>
                        <h2>Today: <span style={{ color: 'blue' }}>{currentDate}</span></h2>

                        <h2>
                        <b>Status: <span style={{ color: 'blue' }}>{status}</span></b>
                        </h2>

                    </MDBCol>
                </MDBRow>

                <MDBRow className="mt-5">
                    <MDBCol size='6'>
                        <h2><b>SEARCH </b> <MDBIcon fas icon="search" /> </h2>
                        <div className="mt-4">
                            <DatePicker
                                selected={selectedDate}
                                onChange={handleDateChange}
                                dateFormat="MM/dd/yyyy" // Adjust date format
                                minDate={null} // Disable future dates
                                maxDate={maxDate} // Disable future dates
                                inline
                                showDisabledMonthNavigation
                            />
                        </div>
                        {selectedDate && (
                            <div className="mt-3">
                                <h5><b>Selected Date: {selectedDate.toLocaleDateString()}</b></h5>
                                <h5>State: {presentStates.length > 0 ? (presentStates[0] ? 'Present' : 'Absent') : 'Absent'}</h5>

                            </div>
                        )}
                        
                    </MDBCol>
                    <MDBCol size='6'>
                        <h2>Filter Present dates by Month</h2>
                        <div>
                            <DatePicker
                                selected={selectedMonth ? new Date(new Date().getFullYear(), selectedMonth - 1, 1) : null}
                                onChange={handleMonthChange}
                                renderMonthContent={renderMonthContent}
                                showMonthYearPicker
                                dateFormat="MM/yyyy"
                            />
                            {selectedMonth && (
                                <div className="mt-3">
                                    <p>Selected Month: {selectedMonth}</p>
                                </div>
                            )}
                            <MDBTable striped>
                                <MDBTableHead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Entrance Time</th>
                                    </tr>
                                </MDBTableHead>
                                <MDBTableBody>
                                    {attendanceData.map(attendance => (
                                        <tr key={attendance.attendance_id} >
                                            <td>{attendance.date}</td>
                                            <td>{attendance.in_time}</td>
                                        </tr>
                                    ))}
                                </MDBTableBody>
                            </MDBTable>
                        </div>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        </div>
    );

}

export default User_Dashboard2;
