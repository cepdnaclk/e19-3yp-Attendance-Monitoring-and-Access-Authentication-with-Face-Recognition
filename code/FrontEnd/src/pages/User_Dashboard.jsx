import React from 'react'
import { useLocation } from 'react-router-dom';

function User_Dashboard() {
    const location = useLocation();
    const email = location.state && location.state.email;
    return (
        <div>
            <h1>this is {email} Dashboard</h1>
        </div>
    )
}

export default User_Dashboard;