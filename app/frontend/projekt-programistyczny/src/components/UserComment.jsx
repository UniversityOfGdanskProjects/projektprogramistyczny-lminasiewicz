import { useNavigate } from "react-router-dom";
import { useMemo } from "react";

export default function UserComment({content, date, post}) {
    const navigate = useNavigate();
    const truncatedContent = useMemo(() => {
        console.log(content, content.length);
        if (content.length > 50) {
            return `${content.slice(0, 47)}...`
        }
        return content
    }, [])


    return (
        <li className="comment-item" onClick={() => navigate(`/posts/${post}}`)}>
            <h2 className="item-title">{truncatedContent}</h2>
            <div className="small">Posted: {date}</div>
        </li>
    );
};