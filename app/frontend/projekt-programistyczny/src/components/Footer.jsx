import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';

export default function Footer() {
    return (
        <div className="flex-generic" id="footer">
            <div className="footer-link">
                <a href="https://www.linkedin.com/in/łukasz-minasiewicz-192677243/">LinkedIn</a>
            </div>
            <div className="footer-link">
                <a href="https://github.com/UniversityOfGdanskProjects/projektprogramistyczny-lminasiewicz/tree/main">GitHub</a>
            </div>
            <div className="footer-link">
                <a href="https://www.youtube.com">YouTube</a>
            </div>
        </div>
    )
}