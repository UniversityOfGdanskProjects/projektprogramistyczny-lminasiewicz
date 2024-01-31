import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import './App.scss';
import NavBar from './components/NavBar';
import Footer from "./components/Footer";
import Main from "./pages/Main";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";

function App() {
  return (
    <>
      <NavBar/>
      <Routes>
        <Route path="/" element={<Main />}></Route>
        <Route path="login" element={<LogIn />} />
        <Route path="signup" element={<SignUp />} />
      </Routes>
      <Footer/>
    </>
  );
}

export default App;

{/* 
          <Route path="posts" element={<Posts />} />
          <Route path="posts/:id" element={<Post id={id}/>} />
          <Route path="users" element={<Users />} />
          <Route path="users/:username" element={<User username={username}/>} />
          <Route path="" element={<Users />} />
          <Route path="*" element={<NoPage />} />
        </Route> */}