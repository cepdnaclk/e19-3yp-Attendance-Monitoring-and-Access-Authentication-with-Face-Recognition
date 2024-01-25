import React, { useState, useEffect } from "react";
import backgroundImg from '../assets/background.jpg';
import UserNavbar from "../component/userNavbar";
import { useNavigate} from 'react-router-dom';
import { MDBContainer, MDBRow, MDBCol } from 'mdb-react-ui-kit';

const User_Dashboard2 = () => {
    const navigate = useNavigate();
    const [isAuth, setIsAuth] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true); 
        }
        else{
            navigate('/');
        }
    }, [isAuth]);

    if (!isAuth) {
        return null;
    }

    return(
        <div
            style={{
            backgroundImage: `url(${backgroundImg})`,
            backgroundSize: 'cover',
            minHeight: '100vh', 
            }}
        >
            <UserNavbar/>
            <h2 className="m-4">Hi.. First Name</h2>

            <MDBContainer>
                <MDBRow className="m-5">
                    <MDBCol size='6'>
                        <h5>Employee ID : </h5>
                        <h5>First Name : </h5>
                        <h5>Last Name : </h5>
                        <h5>Department : </h5>
                        <h5>Email : </h5>
                        <h5>Contact address : </h5>
                        <h5>PIN : </h5>

                    </MDBCol>

                    <MDBCol size='6'>
                        <p>lkjlkj</p>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        </div>
    );

}

export default User_Dashboard2;