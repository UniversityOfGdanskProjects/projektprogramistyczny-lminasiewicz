import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import { useFormik } from "formik";

export default function Comment({ id, author, date, content, deleted }) {
    const navigate = useNavigate();
    const [comments, setComments] = useState([]);
    const [formRevealed, setRevealed] = useState(false);
    const auth = localStorage.getItem("auth")

    const submitComment = (vals) => {
        const comm = vals.comment
        axios.post(`${DB_LINK}/api/comments/submit`, {content: comm, under: id}).then((res) => {
            console.log(res.data);
            navigate(0);
        }).catch((err) => {
            console.error(err);
        })
    }

    const formik = useFormik({
        initialValues: {
            comment: "",
        },
        onSubmit: submitComment
    });

    const deleteComment = () => {
        if (auth) {
            const username = JSON.parse(auth).username
            const token = JSON.parse(auth).token
            axios.delete(`${DB_LINK}/api/comments/delete/${id}?username=${username}&token=${token}`).then((res) => {
                console.log(res.data);
                navigate(0);
            }).catch((err) => {
                console.error(err);
            })
        }
    }

    useEffect(() => {
        axios.get(`${DB_LINK}/api/comments/byComment/${id}`).then((res) => {
            console.log(res.data.comments);
            setComments(res.data.comments);
        }).catch((err) => {
            console.error(err);
        });
    }, []);

    if (!deleted) {
        return (
            <li className="comment">
                <div className="comment-body">
                    <div>
                        <h3>{content}</h3>
                        <div className="info">{author} at {date}</div>
                    </div>
                    {auth? JSON.parse(auth).admin? <div className="buttons">
                        <div className="btn-admin" onClick={deleteComment}>Delete</div>
                    </div> : "" : ""}
                </div>
                {formRevealed && (<form className="form post-form" onSubmit={formik.handleSubmit}>
                    <label htmlFor="comment">Comment</label>
                    <input type="text" id="comment" {...formik.getFieldProps('comment')} />
                    <input type="submit" value="Post" />
                </form>)}
                <ul className="post-comments-list">
                    {comments.map((comment) => {
                        return comment? !comment.deleted && <Comment id={comment.id} author={comment.author} date={comment.date} content={comment.content} deleted={comment.deleted}/> : ""
                    })}
                </ul>
            </li>
        );
    }
}