import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Main() {
    const navigate = useNavigate()
    return (
        <>
            <div className="page main-page-intro">
                <div className="main-title">
                    <div className="main-title">Coffee & Code</div>
                    <div className="main-subtitle">Welcome to my blog.</div>
                </div>
                <img src="codefee_edited.jpg" className="main-image"/>
                <div className="image-coverer"/>
            </div>
            <div className="main-page-mid">
                <div className="main-paragraph flex-vertical">
                    <h1>I code, drink coffee, and do other stuff too</h1>
                    <div className="main-text">
                        Hi, welcome to my website. I study IT at University of Gdańsk. My hobbies include coding, economics, and music theory. I'll be using this site as a personal blog, so feel free to read some of my posts. Click the button below to be taken there!
                    </div>
                    <button className="main-button" onClick={() => navigate("/posts")}>Posts &gt;</button>
                </div>
                <div className="main-image">
                    <img src="coffeencode.jpg"/>
                </div>
            </div>
            <div className="main-page-end">
                <div className="main-image">
                    <img src="vscode.png"/>
                </div>
                <div className="main-paragraph flex-vertical">
                    <h1>About the website</h1>
                    <div className="main-text">
                        This website was built with React, Flask, and Neo4j, for a large university project that spans 2 different subjects: Frontend Development and Databases II. Wanna see the code? Check out the Github page below!
                    </div>
                    <a className="main-button" href="https://github.com/UniversityOfGdanskProjects/projektprogramistyczny-lminasiewicz/tree/main"><button>GitHub &gt;</button></a>
                </div>
            </div>
        </>
    )
}