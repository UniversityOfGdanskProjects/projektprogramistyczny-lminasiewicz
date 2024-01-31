import axios from "axios"
import { DB_LINK } from "../constants"
import { useNavigate } from "react-router-dom"

export default function DeleteButton({ id }) {
    const navigate = useNavigate();

    const deletePost = () => {
        const auth = JSON.parse(localStorage.getItem("auth"))
        axios.delete(`${DB_LINK}/api/posts/delete/${id}?username=${auth.username}&token=${auth.token}`).then((res) => {
            console.log(res.data);
            navigate(0);
        }).catch((err) => {
            console.error(err);
        })
    }

    return JSON.parse(localStorage.getItem("auth")).admin && <div className="btn-admin btn-del flex-center" onClick={deletePost}>Delete</div>
}