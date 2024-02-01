import { useNavigate } from "react-router-dom"

export default function UserItem({username, registered}) {
    const navigate = useNavigate();
    return (
        <li className="user-item" onClick={() => navigate(`/users/${username}`)}>
            <h2 className="item-title">{username}</h2>
            <div className="small">Registered: {registered}</div>
        </li>
    )
}