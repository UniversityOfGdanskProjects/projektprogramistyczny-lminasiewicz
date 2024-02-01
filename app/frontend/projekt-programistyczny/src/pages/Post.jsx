import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import { useFormik } from "formik";
import PostComments from '../components/PostComments'

export default function Post() {
    const navigate = useNavigate();
    const { id } = useParams();
    const [post, setPost] = useState({title: "", content: "", tags: [], date: ""});
    const [comments, setComments] = useState([])
    const [avgRating, setAvgRating] = useState(0);
    const [rated, setRated] = useState(-1);
    const starRef1 = useRef();
    const starRef2 = useRef();
    const starRef3 = useRef();
    const starRef4 = useRef();
    const starRef5 = useRef();


    const ratePost = (n) => {
        if (localStorage.getItem("auth")) {
            const auth = JSON.parse(localStorage.getItem("auth"));
            axios.post(`${DB_LINK}/api/posts/${id}/rating?username=${auth.username}&token=${auth.token}`, {rating: n}).then((res) => {
                if (res.data === "Rating added successfully.") {
                    const refs = [starRef1, starRef2, starRef3, starRef4, starRef5];
                    refs.slice(0, n-1).map((ref) => {
                        ref.current.styles.color = "gold"
                    })
                    setRated(n)
                }
            }).catch((err) => {
                console.error(err);
            });
        }
    }
    
    useEffect(() => {
        axios.get(`${DB_LINK}/api/posts/${id}`).then((res) => {
            const p = res.data.post
            setPost({title: p.title, content: p.content, tags: p.tags, date: p.date})
        }).catch((err) => {
            console.error(err);
        });
    }, [id])

    useEffect(() => {
        axios.get(`${DB_LINK}/api/posts/${id}/rating`).then((res) => {
            setAvgRating(res.data.score)
        }).catch((err) => {
            console.error(err);
        });
    }, [id, rated])

    useEffect(() => {
        if (localStorage.getItem("auth")) {
            const auth = JSON.parse(localStorage.getItem("auth"));
            axios.get(`${DB_LINK}/api/posts/${id}/userrating?username=${auth.username}&token=${auth.token}`).then((res) => {
                console.log(res.data.rating);
                setRated(res.data.rating);
                const refs = [starRef1, starRef2, starRef3, starRef4, starRef5];
                refs.slice(0, rated-1).map((ref) => {
                    ref.current.style.color = "gold";
                })

            }).catch((err) => {
                console.error(err);
            });
        }
    }, [id])

    const stringifyArray = (arr) => {
        const result = arr.reduce((acc, curr) => {return curr + ", " + acc}, "");
        return result.slice(0, result.length-2);
    };

    return (
        <div className="page post-page">
            <div className="users-wrapper post-part">
                <h2>{post.title}</h2>
                <div className="post-content">
                    {post.content}
                </div>
                <div className="post-data-wrapper">
                    <div className="rating-data">
                        <div className="rating">
                            <span ref={starRef1} className="star" onClick={() => rated === 0? ratePost(1) : {}}>★</span>
                            <span ref={starRef2} className="star" onClick={() => rated === 0? ratePost(2) : {}}>★</span>
                            <span ref={starRef3} className="star" onClick={() => rated === 0? ratePost(3) : {}}>★</span>
                            <span ref={starRef4} className="star" onClick={() => rated === 0? ratePost(4) : {}}>★</span>
                            <span ref={starRef5} className="star" onClick={() => rated === 0? ratePost(5) : {}}>★</span>
                        </div>
                        <div className="avg-rating">Average rating: {avgRating}</div>
                    </div>
                    <div className="post-data">
                        <div className="post-date"><b>Posted:</b> {post.date}</div>
                        <div className="post-tags"><b>Tags:</b> {stringifyArray(post.tags)}</div>
                    </div>
                </div>
            </div>
            <PostComments id={id}/>
        </div>
    );
};