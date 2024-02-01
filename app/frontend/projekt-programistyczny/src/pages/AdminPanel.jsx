import ReactDOM from "react-dom/client";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'

export default function AdminPanel() {
    const auth = localStorage.getItem("auth")
    const [users, setUsers] = useState(0);
    const [posts, setPosts] = useState(0);
    const [comments, setComments] = useState(0);

    const backupData = () => {
        if (auth) {
            const username = JSON.parse(auth).username;
            const token = JSON.parse(auth).token;
            axios.post(`${DB_LINK}/api/backup/posts?username=${username}&token=${token}`).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.error(err);
            })
        }
    };

    const loadBackup = () => {
        if (auth) {
            const username = JSON.parse(auth).username;
            const token = JSON.parse(auth).token;
            axios.post(`${DB_LINK}/api/backup/load/posts?username=${username}&token=${token}`).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.error(err);
            })
        }
    };



    useEffect(() => {
        axios.get(`${DB_LINK}/api/users/count`).then((res) => {
            setUsers(res.data.count)
        }).catch((err) => {
            console.error(err);
        });

        axios.get(`${DB_LINK}/api/posts/count`).then((res) => {
            setPosts(res.data.count)
        }).catch((err) => {
            console.error(err);
        });

        axios.get(`${DB_LINK}/api/comments/count`).then((res) => {
            setComments(res.data.count)
        }).catch((err) => {
            console.error(err);
        });
    }, [])

    if (auth) {
        if (JSON.parse(auth).admin) {
            return (
                <div className="page">
                    <div className="page-title">
                        <h1>Admin Panel</h1>
                    </div>
                    <div className="users-wrapper admin-wrapper">
                        <div className="admin-data">
                            <div className="admin-data-point">Total Users: {users}</div>
                            <div className="admin-data-point">Total Posts: {posts}</div>
                            <div className="admin-data-point">Total Comments: {comments}</div>
                        </div>
                        <div className="admin-actions">
                            <div className="admin-action"><div className="btn-admin btn-csv" onClick={backupData}><p>Backup data</p></div></div>
                            <div className="admin-action"><div className="btn-admin btn-csv" onClick={loadBackup}><p>Load backup</p></div></div>
                        </div>
                    </div>
                </div>
            );
        }
    }
};