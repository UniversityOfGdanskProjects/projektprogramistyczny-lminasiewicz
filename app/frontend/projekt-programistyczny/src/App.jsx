import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import './App.scss';
import NavBar from './components/NavBar'
import Footer from "./components/Footer";

function App() {
  return (
    <>
      <NavBar/>
      <Routes>
      </Routes>
      <Footer/>
    </>
  );
}

export default App;

{/* <Route path="/" element={<Index />}>
          <Route index element={<Redirect/>} />
          <Route path="posts" element={<Blogs />} />
          <Route path="posts/<post>" element={<Contact />} />
          <Route path="*" element={<NoPage />} />
        </Route> */}