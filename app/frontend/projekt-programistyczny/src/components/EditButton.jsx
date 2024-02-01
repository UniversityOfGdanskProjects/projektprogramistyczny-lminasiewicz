import axios from "axios"
import { DB_LINK } from "../constants"
import { useNavigate } from "react-router-dom"

export default function EditButton({id}) {
    const navigate = useNavigate();

    return localStorage.getItem("auth") ? JSON.parse(localStorage.getItem("auth")).admin && 
    <div className="btn-admin btn-edit flex-center" onClick={() => navigate(`/posts/edit/${id}`)}>Edit</div> : null
}

