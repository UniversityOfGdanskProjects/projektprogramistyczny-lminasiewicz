import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import ProfileButton from "./ProfileButton";

export default function LogInOut() {
    if (!localStorage.getItem("loggedIn")) {
        return (
            <div className="navbar-link b-left"><div className="flex-generic">Log In</div></div>
        )
    }
    else {
        return (
            <ProfileButton user={localStorage.getItem("loggedIn").username}/>
        )
    }
}