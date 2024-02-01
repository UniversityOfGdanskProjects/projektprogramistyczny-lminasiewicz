import { useLayoutEffect, useState } from "react"
import { DB_LINK } from "../constants";
import axios from "axios";


export default function UserStats({ username }) {
    const [user, setUser] = useState({username: username, registered: "", admin: false});
    const [activity, setActivity] = useState(0);

    useLayoutEffect(() => {
        axios.get(`${DB_LINK}/api/users/user/${username}`).then((res) => {
            const new_user = {username: res.data.user.username, registered: res.data.user.registered, admin: res.data.user.admin.toString()};
            setUser(new_user);
        }).catch((err) => {
            console.error(err);
        })
    }, [])

    useLayoutEffect(() => {
        axios.get(`${DB_LINK}/api/users/user/${username}/activity`).then((res) => {
            setActivity(res.data.score);
        }).catch((err) => {
            console.error(err);
        })
    }, [])

    return (
        <div className="user-stats">
            <h3 className="user-name">Username: {user.username}</h3>
            <div className="user-data">
                <p>Registered on: {user.registered}</p>
                <p>Admin?: {user.admin}</p>
                <p>Activity score: {activity}</p>
            </div>
        </div>
    );
}