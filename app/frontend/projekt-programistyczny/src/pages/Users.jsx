import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState, useLayoutEffect } from "react";
import { useFormik } from 'formik';
import axios from 'axios';
import { DB_LINK } from '../constants'
import UserItem from '../components/UserItem';


export default function Users() {
    const navigate = useNavigate();
    const [users, setUsers] = useState([]);

    const searchUsers = (vals) => {
        if (vals.phrase.length === 0) {
            axios.get(`${DB_LINK}/api/users`).then((res) => {
                setUsers(res.data.users)
            }).catch((err) => {
                console.error(err);
            });
        }
        else {
            axios.get(`${DB_LINK}/api/users/search?phrase=${vals.phrase}`).then((res) => {
                setUsers(res.data.users)
            }).catch((err) => {
                console.error(err);
            });
        }
    };

    const formik = useFormik({
        initialValues: {
            phrase: ""
        },
        onSubmit: searchUsers
    });


    useLayoutEffect(() => {
        axios.get(`${DB_LINK}/api/users`).then((res) => {
            setUsers(res.data.users)
            console.log(res.data.users);
        }).catch((err) => {
            console.error(err);
        });
    }, [])


    return (
        <div className="page users-page">
            <div className="page-title"><h1>Users</h1></div>
            <div className="users-wrapper">
                <div className="search-users">
                    <form className="form" onSubmit={formik.handleSubmit}>
                        <label htmlFor="phrase">Search Phrase</label>
                        <br />
                        <input type="text" id="phrase" {...formik.getFieldProps('phrase')} />
                        <input type="submit" value="Search" />
                    </form>
                </div>
                <div className="listing">
                    <ul className="users-list">
                        {users.map((user) => {
                            return (
                                <UserItem username={user.username} registered={user.registered}/>
                            );
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
};