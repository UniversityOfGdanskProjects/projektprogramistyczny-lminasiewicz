import { useNavigate } from "react-router-dom";
import { useMemo } from "react";
import EditButton from "./EditButton";
import DeleteButton from "./DeleteButton";

export default function PostItem({title, content, date, id}) {
    const navigate = useNavigate();
    const truncatedContent = useMemo(() => {
        if (content.length > 60) {
            return `${content.slice(0, 57)}...`
        }
        return content
    }, []);

    const truncatedTitle = useMemo(() => {
        if (title.length > 40) {
            return `${title.slice(0, 37)}...`
        }
        return title
    }, []);


    return (
        <li className="post-result">
            <div className="post-item" onClick={() => navigate(`/posts/${id}}`)}>
                <h2 className="item-title">{truncatedTitle}</h2>
                <div className="item-content">{truncatedContent}</div>
                <div className="small">Posted: {date}</div>
            </div>
            <div className="admin-options">
                <EditButton id={id}/>
                <DeleteButton id={id}/>
            </div>
        </li>
    );
};