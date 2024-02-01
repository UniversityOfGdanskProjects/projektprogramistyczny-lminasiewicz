import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import ProfileButton from "./ProfileButton";

export default function LogInOut() {
    const navigate = useNavigate();
    if (!localStorage.getItem("auth")) {
        return (
            <div className="navbar-link navbar-hover b-left b-right"><div className="flex-generic" onClick={() => navigate("/login")}>Log In</div></div>
        )
    }
    else {
        return (
            <ProfileButton user={JSON.parse(localStorage.getItem("auth")).username}/>
        );
    }
}