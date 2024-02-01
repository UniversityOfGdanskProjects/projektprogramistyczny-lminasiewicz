import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import LoginForm from "../components/LoginForm";


export default function LogIn() {
    const navigate = useNavigate();
    if (localStorage.getItem("auth")) {
        return (
            <div className="page login-page">
                <div className="page-title" style={{"margin-bottom": "20em"}}><h1>Log out before accessing.</h1></div>
            </div>
        );
    }
    else {
        return (
            <div className="page login-page">
                <div className="page-title">
                    <h1>Log In</h1>
                </div>
                <div className="form-wrapper">
                    <div className="form-select login-select" onClick={() => navigate("/login")}>
                        <p>Log In</p>
                    </div>
                    <div className="form-select signup-select" onClick={() => navigate("/signup")}>
                        <p>Sign Up</p>
                    </div>
                    <div className="form acc-form">
                        <LoginForm/>
                    </div>
                </div>
            </div>
        );
    }
}