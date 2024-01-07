import React, { useState } from 'react';
import {BrowserRouter,Route,Routes} from 'react-router-dom';
//import './App.css'
import Signin from './pages/Sign_in.jsx';
import Signup from './pages/Sign_up.jsx';
import Admin_Dashboard from './pages/Admin_Dashboard.jsx';
import User_Dashboard from './pages/User_Dashboard.jsx';

function App() {
  const [count, setCount] = useState(0)

  return (
    <React.Fragment>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/admin" element={<Admin_Dashboard />} />
          <Route path="/user" element={<User_Dashboard />} />
        </Routes>
      </BrowserRouter>
    </React.Fragment>
  )
}

export default App
