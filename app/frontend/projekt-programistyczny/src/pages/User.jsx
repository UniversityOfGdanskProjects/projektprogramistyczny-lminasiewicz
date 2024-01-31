import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'


export default function User() {
    const navigate = useNavigate();
    const { username } = useParams();

    return (
        <div className="page user-page">
            <div className="page-title"><h1>{username}</h1></div>
            <div className="users-wrapper">
                <div className="user-stats">
                    
                </div>
                <div className="user-comments">

                </div>
            </div>
        </div>
    );
};