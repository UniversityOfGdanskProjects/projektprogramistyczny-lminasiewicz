import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { DB_LINK } from '../constants'


export default function LoginForm() {

    const onSubmit = (vals) => {
        const login = vals.login;
        const pwd = vals.pwd;
        axios.post(`${DB_LINK}/api/users/login`, {login: login, password: pwd}).then((res) =>{
            console.log(res);
            if (typeof res.data === "object") {
                setErr("");
                console.log(`Logged In User: ${res.data.username}`);
                localStorage.setItem("loggedIn", res.data);
                navigate("/");
            }
            else {
                setErr("Login Failed. Incorrect username or password.");
            }
        }).catch((err) => {
            setErr("Login Failed. Server error.");
        })
    };

    const [err, setErr] = useState("");
    const navigate = useNavigate();

    const formik = useFormik({
        initialValues: {
            login: "",
            pwd: ""
        },

        validationSchema: Yup.object({
            login: Yup.string()
            .min(4, 'Must be more than 3 characters.')
            .max(15, 'Must be less than 15 characters')
            .required('*required'),
            pwd: Yup.string().matches(
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,20}$/,
            'Password must be between 5 and 20 characters, contain a lowercase letter, an uppercase letter, and a digit.'
        )}),

        onSubmit: onSubmit
    });

    return (
        <div className="login-wrapper">
            <form className="login" onSubmit={formik.handleSubmit}>
                <label htmlFor="login">Login</label>
                <br />
                <input type="text" id="login" {...formik.getFieldProps('login')} />
                {formik.touched.login && formik.errors.login ? (
                <p className="form-error">{formik.errors.login}</p>
                ) : null}
                <br />
                <label htmlFor="pwd">Password</label>
                <br />
                <input type="password" id="pwd" {...formik.getFieldProps('pwd')} />
                {formik.touched.pwd && formik.errors.pwd ? (
                <p className="form-error">{formik.errors.pwd}</p>
                ) : null}
                <br />
                <input type="submit" value="Submit" />
                <p className="form-error">{err}</p>
                <br />
            </form>
        </div>
    )
}