import axios from "axios"
import { DB_LINK } from "../constants"

export default function DeleteButton({ id }) {
    const deletePost = () => {
        axios.delete(`${DB_LINK}/api/posts/delete/${id}`).then((res) => {
            console.log("Success");
        }).catch((err) => {
            console.error(err);
        })
    }

    return <div className="btn-admin btn-del flex-center" onClick={deletePost}>Delete</div>
}