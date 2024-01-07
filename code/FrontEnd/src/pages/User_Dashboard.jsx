import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import '../css/User_Dashboard.css';

const UserDashboard = () => {
  const getDaysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();

  const AttendanceDaysCard = () => {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const totalWorkingDays = getDaysInMonth(currentYear, currentMonth);

    // Assuming you have an array of attendance data (replace with your actual data)
    const attendanceData = [
      { date: '2024-01-01', status: 'present' },
      { date: '2024-01-02', status: 'absent' },
      { date: '2024-01-03', status: 'absent' },
      // Add more entries as needed
    ];

    const workingDaysAttended = attendanceData.filter(entry => {
      const entryDate = new Date(entry.date);
      return entryDate.getMonth() === currentMonth && entryDate.getDay() !== 0 && entryDate.getDay() !== 6;
    });

    return (
      <div className="card AttendanceDaysCard" style={{height: '200px' }}>
        <div className="card-body">
          <h5 className="card-title">Attendance Days</h5>
          <p className="card-text">
            <strong>Total Working Days:</strong> {totalWorkingDays}<br />
            <strong>Working Days Attended:</strong> {workingDaysAttended.length}
          </p>
        </div>
      </div>
    );
  };

  const CalendarAndClockCard = () => {
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
  
    useEffect(() => {
      const intervalId = setInterval(() => {
        setCurrentDateTime(new Date());
      }, 1000);
  
      return () => clearInterval(intervalId);
    }, []);
  
    const formattedDate = currentDateTime.toLocaleDateString();
    const formattedTime = currentDateTime.toLocaleTimeString();
  
    return (
      <div className="card CalendarAndClockCard" style={{ height: '200px' }}>
        <div className="card-body">
          <h5 className="card-title">Calendar and Digital Clock</h5>
          <div className="calendar">
            <p className="calendar-text">{formattedDate}</p>
          </div>
          <div className="digital-clock">
            <p className="clock-text">{formattedTime}</p>
          </div>
        </div>
      </div>
    );
  };

  const TodayAttendanceCard = () => {
    const [todayAttendance, setTodayAttendance] = useState(null);

    useEffect(() => {
      // Assuming you have a function to fetch today's attendance data
      const fetchTodayAttendance = async () => {
        // Replace this with your actual API call or data fetching logic
        const todayData = await fetchTodayAttendanceData();
        setTodayAttendance(todayData);
      };

      fetchTodayAttendance();
    }, []);

    const fetchTodayAttendanceData = () => {
      // Replace this with your actual API call or data fetching logic
      // Here, I'm using dummy data for illustration
      const dummyData = {
        date: '2024-01-06',
        status: 'present',
        time: '09:30 AM',
      };

      return Promise.resolve(dummyData);
    };

    if (!todayAttendance) {
      return <p>Loading today's attendance...</p>;
    }

    return (
      <div className="card TodayAttendanceCard" style={{height: '200px' }}>
        <div className="card-body">
          <h5 className="card-title">Today's Attendance</h5>
          <p className="card-text">
            <strong>Status:</strong> {todayAttendance.status === 'present' ? 'Present' : 'Absent'}<br />
            <strong>Time:</strong> {todayAttendance.time}
          </p>
        </div>
      </div>
    );
  };


  const location = useLocation();
  const email = location.state && location.state.email;

  return (
    <div>
      <h1>This is {email} Dashboard</h1>
      <div className='row'>
        <div className="col-md-6"  >
            <CalendarAndClockCard />
        </div>
        <div className="col-md-6" >
            <AttendanceDaysCard  />
        </div>
      </div>

      <TodayAttendanceCard />
      
      <div className="card">
        <div className="card-body">
          <h5 className="card-title">Employee Details</h5>
          <p className="card-text">
            <strong>Name:</strong> John Doe<br />
            <strong>Employee ID:</strong> EMP123<br />
            <strong>Department:</strong> Marketing<br />
            <strong>Position:</strong> Senior Marketing Analyst
          </p>
          <button type="button" className="btn btn-primary">View Attendance</button>
        </div>
      </div>
      
    </div>
  );
};

export default UserDashboard;
