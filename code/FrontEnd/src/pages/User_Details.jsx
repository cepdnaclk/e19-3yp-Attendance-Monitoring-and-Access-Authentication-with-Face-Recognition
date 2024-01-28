import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import backgroundImg from '../assets/background.jpg';
import Navbar from '../component/navbar';
import axios from 'axios';
import { MDBDropdown, MDBDropdownToggle, MDBDropdownMenu, MDBDropdownItem, MDBIcon } from 'mdb-react-ui-kit';
import '../css/User_Details.css';
import DatePicker from 'react-datepicker';

const User_Details = () => {
    const navigate = useNavigate();

    const [isAuth, setIsAuth] = useState(false);
    const [employees, setEmployees] = useState([]);
    const [selectedEmployeeId, setSelectedEmployeeId] = useState(1);
    const [selectedMonth, setSelectedMonth] = useState(1);


    const handleEmployeeSelect = (empId) => {
        setSelectedEmployeeId(empId);
    };

    const handleMonthChange = date => {
        setSelectedMonth(date.getMonth() + 1); // Get the month (0-indexed) and add 1 to get the month number (1-indexed)
    };

    const renderMonthContent = (month, shortMonth, longMonth, day) => {
        const fullYear = new Date(day).getFullYear();
        const tooltipText = `Select month: ${longMonth} ${fullYear}`;

        return <span title={tooltipText}>{shortMonth}</span>;
    };

    useEffect(() => {
    // Fetch all employee details from the endpoint
        const fetchEmployees = async () => {
            try {
            const response = await axios.get('https://facesecure.azurewebsites.net/attendanceManagement/save-employee/');
            setEmployees(response.data.all_emp);
            } catch (error) {
            console.error('Error fetching employees:', error);
            }
    };

    fetchEmployees();
    }, []);

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true); 
        } else {
            navigate('/');
        }
    }, [isAuth]);


    return(
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
                <h1 className="ml-5 mt-3">Take User Details</h1>
                <div className="m-5">
                <MDBDropdown dropright group className="mr-4">
                    <MDBDropdownToggle>
                        {employees.length > 0 ? (
                        `${employees.find(emp => emp.emp_id === selectedEmployeeId) ? 
                            `${employees.find(emp => emp.emp_id === selectedEmployeeId).first_name} ${employees.find(emp => emp.emp_id === selectedEmployeeId).last_name}` 
                            : 'Select Employee'}`
                        ) : 'Loading...'}
                    </MDBDropdownToggle>

                    <MDBDropdownMenu>
                        {employees.map(employee => (
                        <MDBDropdownItem link key={employee.emp_id} onClick={() => handleEmployeeSelect(employee.emp_id)}>
                            {employee.first_name} {employee.last_name}
                        </MDBDropdownItem>
                        ))}
                    </MDBDropdownMenu>
                    </MDBDropdown>

                    <DatePicker
                        selected={selectedMonth ? new Date(new Date().getFullYear(), selectedMonth - 1, 1) : null}
                        onChange={handleMonthChange}
                        renderMonthContent={renderMonthContent}
                        showMonthYearPicker
                        dateFormat="MM/yyyy"
                        className="mr-4"
                    />

                    <MDBIcon fab icon="searchengin" className='ms-1 ml-3' size='3x'/>
                </div>
            </div>

        </div>
    );
}

export default User_Details;