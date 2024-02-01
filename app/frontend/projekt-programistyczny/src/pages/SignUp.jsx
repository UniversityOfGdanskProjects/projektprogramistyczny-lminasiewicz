import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import SignupForm from "../components/SignupForm.jsx";


export default function SignUp() {
    const navigate = useNavigate();
    if (localStorage.getItem("auth")) {
        return (
            <div className="page signup-page">
                <div className="page-title" style={{"margin-bottom": "20em"}}><h1>Log out before accessing.</h1></div>
            </div>
        );
    }
    else {
        return (
            <div className="page signup-page">
                <div className="page-title">
                    <h1>Sign Up</h1>
                </div>
                <div className="form-wrapper">
                    <div className="form-select login-select" onClick={() => navigate("/login")}>
                        <p>Log In</p>
                    </div>
                    <div className="form-select signup-select" onClick={() => navigate("/signup")}>
                        <p>Sign Up</p>
                    </div>
                    <div className="form acc-form">
                        <SignupForm/>
                    </div>
                </div>
            </div>
        );
    }
}