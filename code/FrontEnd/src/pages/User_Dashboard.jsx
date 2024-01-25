import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import '../css/User_Dashboard.css';
import backgroundImg from '../assets/background.jpg'; 
import UserNavbar from "../component/userNavbar";
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import Clock from 'react-clock';
import 'react-clock/dist/Clock.css';

const User_Dashboard = () => {
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
      <div className="card AttendanceDaysCard" style={{height: '200px' ,backgroundColor: 'rgba(15, 33, 103, 0.3)', color: 'rgba(0,0,0,1)' }}>
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
      <div className="card CalendarAndClockCard ms-10 me- 10 mt" style={{ height: '450px', backgroundColor: 'rgba(15, 33, 103, 0.3)', color: '#414f6a', display: 'flex', flexDirection: 'column', alignItems: 'left', justifyContent: 'center' }}>
        <div className="card-body">
          {/* <h5 className="card-title">Calendar and Digital Clock</h5> */}
          {/* <div className="calendar" style={{ display: 'flex', alignItems: 'center' }}>
            <svg
              // xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              style={{ marginRight: '8px' }}
            >
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            <p className="calendar-text" style={{ fontSize: '18px', fontWeight: 'bold' }}>{formattedDate}</p>
          </div> */}
          <div className="graphical-calendar " style={{ display: 'flex', alignItems: 'left'}}>
            <Calendar
              onChange={(date) => setCurrentDateTime(date)}
              value={currentDateTime}
            />
          </div>
          <div className="analog-clock" style={{ alignItems: 'center'}}>
            <Clock
              value={currentDateTime}
              size={150}
              renderNumbers
              hourHandWidth={8}
              hourHandLength={50}
              minuteHandWidth={4}
              minuteHandLength={70}
              secondHandWidth={2}
              secondHandLength={80}
              hourMarksWidth={4}
              minuteMarksWidth={2}
            />
          </div>
          {/* <div className="digital-clock">
            <p className="clock-text">{formattedTime}</p>
          </div> */}
        </div>
      </div>
    );
  };
  

  // const CalendarAndClockCard = () => {
  //   const [currentDateTime, setCurrentDateTime] = useState(new Date());
  
  //   useEffect(() => {
  //     const intervalId = setInterval(() => {
  //       setCurrentDateTime(new Date());
  //     }, 1000);
  
  //     return () => clearInterval(intervalId);
  //   }, []);
  
  //   const formattedDate = currentDateTime.toLocaleDateString();
  //   const formattedTime = currentDateTime.toLocaleTimeString();
  
  //   return (
  //     <div className="card CalendarAndClockCard" style={{ height: '200px',backgroundColor: 'rgba(15, 33, 103, 0.3)', color: 'rgba(0,0,0,1)'  }}>
  //       <div className="card-body">
  //         <h5 className="card-title">Calendar and Digital Clock</h5>
  //         <div className="calendar">
  //           <p className="calendar-text">{formattedDate}</p>
  //         </div>
  //         <div className="digital-clock">
  //           <p className="clock-text">{formattedTime}</p>
  //         </div>
  //       </div>
  //     </div>
  //   );
  // };

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
      <div className="card TodayAttendanceCard" style={{height: '200px',backgroundColor: 'rgba(15, 33, 103, 0.3)', color: 'rgba(0,0,0,1)' }}>
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
    <div style={{
        backgroundImage: `url(${backgroundImg})`,
        backgroundSize: 'cover',
        minHeight: '100vh', 
      }}
      >
      
      <UserNavbar/>  
      <h1 style={{marginLeft: '20px'}} className=' text mt-4'>Hi Nuwantha {email}</h1>

      <div className='row'>
      
      <div className='col-md-6'>
      <div className="card" style={{backgroundColor: 'rgba(15, 33, 103, 0.3)', color: 'rgba(0,0,0,1)'}}>
        <div className="card-body">
          <h3 className="card-title mb-4">Employee Details</h3>
          <p className="card-text">

            <h5>Employee ID : </h5>
            <h5>First Name : </h5>
            <h5>Last Name : </h5>
            <h5>Department : </h5>
            <h5>Position :</h5>
            <h5>Email : </h5>
            <h5>Contact address : </h5>
            <h5>PIN : </h5>
          </p>
          
        </div>
      </div>
      
      </div>

      <div className='col-md-6'>
      <TodayAttendanceCard />
      </div>
      
      </div>
      
      <div className='row'>
        <div className="col-md-6"  >
            <CalendarAndClockCard />
        </div>
        <div className="col-md-6" >
            <AttendanceDaysCard  />
        </div>
      </div>

     
      
    </div>
  );
};

export default User_Dashboard;
