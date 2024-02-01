import ReactDOM from "react-dom/client";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef, useReducer } from "react";
import axios from 'axios';
import { DB_LINK } from '../constants'
import { useFormik } from "formik";

export default function EditPost() {
    const navigate = useNavigate();
    const { id } = useParams();
    const [initialTitle, setTitle] = useState("");
    const [initialContent, setContent] = useState("");
    const initialTags = {university: false, programming: false, personal: false, hobbies: false}

    const uniRef = useRef();
    const proRef = useRef();
    const perRef = useRef();
    const hobRef = useRef();

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

    const [tags, dispatch] = useReducer(reducer, initialTags);

    const postPost = (vals) => {
        const auth = JSON.parse(localStorage.getItem("auth"));
        if (auth.admin) {
            if (id >= 0) {
                axios.put(`${DB_LINK}/api/posts/edit/${id}?username=${auth.username}&token=${auth.token}`, {title: vals.title, content: vals.content, tags: tags}).then((res) => {
                    console.log(res.data)
                    navigate("/posts")
                }).catch((err) => {
                    console.error(err);
                })
            }
            else {
                axios.post(`${DB_LINK}/api/posts/submit?username=${auth.username}&token=${auth.token}`, {title: vals.title, content: vals.content, tags: tags}).then((res) => {
                    console.log(res.data)
                    navigate("/posts")
                }).catch((err) => {
                    console.error(err);
                })
            }
        }
        else {
            console.log("No admin privileges to post.")
        }
    }

    useEffect(() => {
        if (id >= 0) {
            axios.get(`${DB_LINK}/api/posts/${id}`).then((res) => {
                const data = res.data.post
                setTitle(data.title)
                setContent(data.content)
                data.tags.map((tag) => {
                    if (Object.keys(tags).includes(tag)) {
                        dispatch({type: tag.toUpperCase()})
                    }
                })
            }).catch((err) => {
                console.error(err);
            })
        }
    }, []);

    const formik = useFormik({
        initialValues: {
            title: initialTitle,
            content: initialContent,
        },
        onSubmit: postPost
    });

    return (
        <div className="page">
            <div className="page-title">
                <h1>Edit Post</h1>
            </div>
            <div className="users-wrapper">
                <div className="post-searchbar">
                    <form className="form post-form" onSubmit={formik.handleSubmit}>
                        <label htmlFor="title">Title</label>
                        <input type="text" id="title" value={initialTitle} {...formik.getFieldProps('title')} />
                        <label htmlFor="content">Content</label>
                        <textarea id="content" className="post-content" {...formik.getFieldProps('content')}></textarea>
                        <div className="tag-selector">
                            <div className="tag" ref={uniRef} onClick={() => dispatch({type: "UNIVERSITY"})}>University</div>
                            <div className="tag" ref={proRef} onClick={() => dispatch({type: "PROGRAMMING"})}>Programming</div>
                            <div className="tag" ref={perRef} onClick={() => dispatch({type: "PERSONAL"})}>Personal</div>
                            <div className="tag" ref={hobRef} onClick={() => dispatch({type: "HOBBIES"})}>Hobbies</div>
                        </div>
                        <input type="submit" value="Submit" id="submit-post"/>
                    </form>
                </div>
            </div>
        </div>
    );

}