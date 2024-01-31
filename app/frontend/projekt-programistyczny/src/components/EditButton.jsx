import axios from "axios"
import { DB_LINK } from "../constants"
import { useNavigate } from "react-router-dom"

export default function DeleteButton({id}) {
    const navigate = useNavigate();

    return <div className="btn-admin btn-edit flex-center" onClick={() => navigate(`/posts/${id}/edit`)}>Edit</div>
}

// localStorage.getItem("auth").admin &&