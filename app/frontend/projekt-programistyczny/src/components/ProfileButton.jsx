import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';

export default function ProfileButton({ user }) {
    return (
        <button>{ user }</button>
    )
}