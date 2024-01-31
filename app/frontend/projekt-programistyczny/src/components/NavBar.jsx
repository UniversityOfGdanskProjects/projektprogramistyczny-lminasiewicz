import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import LogInOut from "./LogInOut";

export default function NavBar() {
    const navigate = useNavigate();
    return (
        <div id="navbar">
            <div className="flex-horizontal-left flex-generic" onClick={() => navigate('/')}>
                <div className="navbar-link logo"/>
                <div className="navbar-link b-right"><div className="flex-generic page-name">Blog</div></div>
            </div>
            
            <div className="flex-horizontal-right flex-generic">
                <div className="navbar-link navbar-hover b-left" href=""><div className="flex-generic">Posts</div></div>
                <div className="navbar-link navbar-hover b-left" href=""><div className="flex-generic">Users</div></div>
                <div className="navbar-link navbar-hover b-left" href=""><div className="flex-generic">About</div></div>
                <LogInOut/>
            </div>
        </div>
    )
}
//<AdminPanelLink/>