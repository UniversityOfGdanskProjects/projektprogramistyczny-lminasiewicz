import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import UserStats from "../components/UserStats";
import UserComment from "../components/UserComment";


export default function User() {
    const navigate = useNavigate();
    const { username } = useParams();
    const [comments, setComments] = useState([]);

    useEffect(() => {
        axios.get(`${DB_LINK}/api/${username}/comments`).then((res) => {
            setComments(res.data.comments)
        }).catch((err) => {
            console.error(err);
        });
    }, [])

    return (
        <div className="page user-page">
            <div className="page-title"><h1>{username}</h1></div>
            <div className="users-wrapper">
                <div className>
                    <UserStats username={username}/>
                </div>
                <div className="user-comments">
                    <ul className="user-comments-list">
                        {comments && comments.map((comment) => {
                            return !comment.deleted && <UserComment content={comment.content} date={comment.date} post={comment.original_post}/>
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
};