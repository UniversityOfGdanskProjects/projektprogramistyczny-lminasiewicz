import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import axios from 'axios';
import { DB_LINK } from "../constants";

export default function ProfileButton({ user }) {
    const navigate = useNavigate();
    const [dropdown, setDropdown] = useState(false);

    const logOut = () => {
        const auth = JSON.parse(localStorage.getItem("auth"))
        const username = auth.username
        const token = auth.token
        axios.delete(`${DB_LINK}/api/users/logout?username=${username}&token=${token}`).then((res) => {
            if (res.data === "Operation Successful") {
                navigate("/");
                localStorage.removeItem("auth")
            }
            else {
                console.log(`Log Out Failed with request data: ${res.data}`);
            }
        }).catch ((err) => {
            console.error(err)
        });
    }

    const elemHover = () => {
        setDropdown(true)
    }

    const elemLeave = () => {
        setDropdown(false);
    }


    return (
        <div onMouseEnter={elemHover} onMouseLeave={elemLeave}>
            <div className="navbar-link b-left b-right profile-button navbar-hover"><div className="flex-generic">{user}</div></div>
            {
                dropdown &&
                <div className="dropdown-menu">
                    <div className="dropdown-item navbar-hover" onClick={() => navigate(`/users/${user}`)}><p>Page</p></div>
                    <div className="dropdown-item navbar-hover" onClick={() => navigate(`/users/${user}/edit`)}><p>Edit Account</p></div>
                    <div className="dropdown-item navbar-hover" onClick={logOut}><p>Log Out</p></div>
                </div>
            }
        </div>
    )
}