import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import './App.scss';
import NavBar from './components/NavBar';
import Footer from "./components/Footer";
import Main from "./pages/Main";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import Users from "./pages/Users";
import User from "./pages/User";
import Posts from "./pages/Posts";
import EditPost from "./pages/EditPost";
import Post from "./pages/Post";
import AdminPanel from "./pages/AdminPanel";

function App() {
  return (
    <>
      <NavBar/>
      <Routes>
        <Route path="/" element={<Main />}></Route>
        <Route path="login" element={<LogIn />} />
        <Route path="signup" element={<SignUp />} />
        <Route path="users" element={<Users />} />
        <Route path="users/:username" element={<User/>} />
        <Route path="posts" element={<Posts />} />
        <Route path="posts/:id" element={<Post />} />
        <Route path="posts/edit/:id" element={<EditPost />} />
        <Route path="adminpanel" element={<AdminPanel />} />
      </Routes>
      <Footer/>
    </>
  );
}

export default App;

{/* 
          <Route path="" element={<Users />} />
          <Route path="*" element={<NoPage />} />
        </Route> */}