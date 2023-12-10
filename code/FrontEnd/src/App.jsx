import React, { useState } from 'react';
import {BrowserRouter,Route,Routes} from 'react-router-dom';
import './App.css'
import Signin from './pages/Sign_in.jsx';
import Signup from './pages/Sign_up.jsx';

function App() {
  const [count, setCount] = useState(0)

  return (
    <React.Fragment>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />

        </Routes>
      </BrowserRouter>
    </React.Fragment>
  )
}

export default App
