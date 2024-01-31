import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import { useFormik } from "formik";

export default function EditPost() {
    const { id } = useParams();
    const [post exis]

    <div className="page">
        <div className="users-wrapper">
            <div className="post-searchbar">
                <form className="form post-form" onSubmit={formik.handleSubmit}>
                    <label htmlFor="before">Before</label>
                    <input type="text" id="phrase" {...formik.getFieldProps('before')} />
                    <label htmlFor="after">After</label>
                    <input type="text" id="phrase" {...formik.getFieldProps('after')} />
                    <input type="submit" value="Search" />
                </form>
                <div className="tag-selector">
                    <div className="tag" ref={uniRef} onClick={() => dispatch({type: "UNIVERSITY"})}>University</div>
                    <div className="tag" ref={proRef} onClick={() => dispatch({type: "PROGRAMMING"})}>Programming</div>
                    <div className="tag" ref={perRef} onClick={() => dispatch({type: "PERSONAL"})}>Personal</div>
                    <div className="tag" ref={hobRef} onClick={() => dispatch({type: "HOBBIES"})}>Hobbies</div>
                </div>
            </div>
        </div>
    </div>

}