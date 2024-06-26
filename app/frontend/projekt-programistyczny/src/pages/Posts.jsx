import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import PostItem from "../components/PostItem";
import { useFormik } from "formik";


export default function Posts() {
    const navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const initialTags = {university: false, programming: false, personal: false, hobbies: false}
    const uniRef = useRef()
    const proRef = useRef()
    const perRef = useRef()
    const hobRef = useRef()

    const reducer = (state, action) => {
        switch (action.type) {
            case "UNIVERSITY":
                if (!state.university) {
                    uniRef.current.style.filter = "brightness(1.3)";
                }
                else {
                    uniRef.current.style.filter = "brightness(1)";
                }
                
                return {university: !state.university, programming: state.programming, personal: state.personal, hobbies: state.hobbies};
            case "PROGRAMMING":
                if (!state.programming) {
                    proRef.current.style.filter = "brightness(1.3)";
                }
                else {
                    proRef.current.style.filter = "brightness(1)";
                }
                return {university: state.university, programming: !state.programming, personal: state.personal, hobbies: state.hobbies};
            case "PERSONAL":
                if (!state.personal) {
                    perRef.current.style.filter = "brightness(1.3)";
                }
                else {
                    perRef.current.style.filter = "brightness(1)";
                }
                return {university: state.university, programming: state.programming, personal: !state.personal, hobbies: state.hobbies};
            case "HOBBIES":
                if (!state.hobbies) {
                    hobRef.current.style.filter = "brightness(1.3)";
                }
                else {
                    hobRef.current.style.filter = "brightness(1)";
                }
                return {university: state.university, programming: state.programming, personal: state.personal, hobbies: !state.hobbies};
            default:
                return state;
        }
    }
    

    const searchPosts = (vals) => {
        if (vals.before === "" && vals.after === "" && !tags.university && !tags.programming && !tags.personal && !tags.hobbies) {
            axios.get(`${DB_LINK}/api/posts`).then((res) => {
                setPosts(res.data.posts)
            }).catch((err) => {
                console.error(err);
            });
        }
        else {
            const arrTags = Object.keys(tags).filter((tag) => tags[tag] === true)
            console.log(vals.before, vals.after, arrTags);
            axios.get(`${DB_LINK}/api/posts/filters?${vals.before == ""? "" : `before=${vals.before}`}&${vals.after == ""? "" : `after=${vals.after}`}&${arrTags == null? [] : `tags=${arrTags}`}`).then((res) => {
                console.log(res.data.posts);
                setPosts(res.data.posts)
            }).catch((err) => {
                console.error(err);
            });
        }
    };


    const formik = useFormik({
        initialValues: {
            before: "",
            after: "",
        },
        onSubmit: searchPosts
    });

    useEffect(() => {
        axios.get(`${DB_LINK}/api/posts`).then((res) => {
            setPosts(res.data.posts)
        }).catch((err) => {
            console.error(err);
        });
    }, [])


    const [tags, dispatch] = useReducer(reducer, initialTags)


    return (
        <div className="page posts-page">
            <div className="page-title"><h1>Posts</h1></div>
            <div className="users-wrapper">
                <div className="post-searchbar">
                    <form className="form post-form" onSubmit={formik.handleSubmit}>
                        <label htmlFor="before">Before</label>
                        <input type="text" id="before" {...formik.getFieldProps('before')} />
                        <label htmlFor="after">After</label>
                        <input type="text" id="after" {...formik.getFieldProps('after')} />
                        <div className="flex-generic width50">
                            <input type="submit" value="Search" />
                        {localStorage.getItem("auth") ? JSON.parse(localStorage.getItem("auth")).admin && 
                        (<div className="write-post" onClick={() => navigate("/posts/edit/-1")}><p>Write Post</p></div>) : null
                        }
                        </div>
                        
                    </form>
                    <div className="tag-selector">
                        <div className="tag" ref={uniRef} onClick={() => dispatch({type: "UNIVERSITY"})}>University</div>
                        <div className="tag" ref={proRef} onClick={() => dispatch({type: "PROGRAMMING"})}>Programming</div>
                        <div className="tag" ref={perRef} onClick={() => dispatch({type: "PERSONAL"})}>Personal</div>
                        <div className="tag" ref={hobRef} onClick={() => dispatch({type: "HOBBIES"})}>Hobbies</div>
                    </div>
                </div>
                <div className="posts">
                    <ul className="posts-list">
                        {posts && posts.map((post) => {
                            return <PostItem title={post.title} content={post.content} date={post.date} id={post.id}/>
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
};