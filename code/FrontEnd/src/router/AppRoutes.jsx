import { createBrowserRouter, Route, Routes } from 'react-router-dom';

import Signin from './pages/Sign_in.jsx';


const AppRoutes = () => {
    return <Routes>
        <Route path='/' element={<Signin />} />

        {/* <Route path={"/"} element={<AdminLayout/>}>
            <Route path='/adminhome' element={<AdminHome />} />
            <Route path='/studentdetails' element={<StudentDetails />} />
            <Route path='/teacherdetails' element={<TeacherDetails />} />
            <Route path='/departmentdetails' element={<DepartmentDetails />} />
            <Route path='/caursedetails' element={<CaurseDetails />} />
            <Route path='/projecdetails' element={<ProjectDetails />} />
            <Route path='/allstudents' element={<AllStudents/>}/>
            {/* <Route path='/studentcommentbyadmin' element={<StudentComment/>}/> */}
       
    </Routes>
};

export default AppRoutes;