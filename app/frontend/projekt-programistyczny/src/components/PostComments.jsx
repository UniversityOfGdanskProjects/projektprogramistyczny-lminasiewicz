import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import { useFormik } from "formik";
import Comment from "./Comment";

export default function PostComments({ id }) {
    const navigate = useNavigate();
    const [comments, setComments] = useState([]);

    const submitComment = (vals) => {
        const content = vals.comment
        if (localStorage.getItem("auth")) {
            const auth = JSON.parse(localStorage.getItem("auth"))
            axios.post(`${DB_LINK}/api/comments/submit?username=${auth.username}&token=${auth.token}`, {content: content, under: id}).then((res) => {
                console.log(res.data);
                setComments([...comments]);
            }).catch((err) => {
                console.error(err);
            })
        }
    }

    const formik = useFormik({
        initialValues: {
            comment: "",
        },
        onSubmit: submitComment
    });

    useEffect(() => {
        axios.get(`${DB_LINK}/api/comments/byPost/${id}`).then((res) => {
            setComments(res.data.comments)
        }).catch((err) => {
            console.error(err);
        });
    }, []);


    return (
        <div className="users-wrapper comments-part">
            <form className="form post-form" onSubmit={formik.handleSubmit}>
                <label htmlFor="comment">Comment</label>
                <input type="text" id="comment" {...formik.getFieldProps('comment')} />
                <input type="submit" value="Post" />
            </form>
            <div className="comments">
                <ul className="post-comments-list">
                    {comments.map((comment) => {
                        return !comment.deleted && <Comment id={comment.id} author={comment.author} date={comment.date} content={comment.content} deleted={comment.deleted}/>
                    })}
                </ul>
            </div>
        </div>
    );
}