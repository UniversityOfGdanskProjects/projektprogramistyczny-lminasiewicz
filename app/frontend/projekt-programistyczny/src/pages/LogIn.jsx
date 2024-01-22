import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import LoginForm from "../components/LoginForm";


export default function LogIn() {
    return (
        <div className="page login-page">
            <div className="page-title">
                <h1>Log In</h1>
            </div>
            <div className="form-wrapper">
                <div className="form-select login-select">
                    <p>Log In</p>
                </div>
                <div className="form-select signup-select">
                    <p>Sign Up</p>
                </div>
                <div className="form login-form">
                    <LoginForm/>
                </div>
            </div>
        </div>
    )
}