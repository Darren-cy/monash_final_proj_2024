import { useState } from "react";
import api from "../api";
import NavigationBar from "../components/NavigationBar";
import { Link } from 'react-router-dom';

const Home = () => {
  const [message, setMessage] = useState("");
  const getData = async () => {
    try {
      const response = await api.get("/api/v1.0/protected");
      setMessage(response.data.message);
      console.log(response.data);
    } catch (error) {
      setMessage("An error occurred");
    }
  };
  return (
    <div className="bg-gradient-to-r from-cyan-300 to-blue-200">
      <NavigationBar></NavigationBar>
      
      <div className="home-container h-14 min-h-screen flex flex-col justify-center items-center text-center">
        <section className="hero p-10 ">
          <h1 className="text-5xl font-bold text-gray-800">Welcome to Document processing app</h1>
          <p className="text-gray-700 text-lg mt-4 leading-10">A streamline Document processing app for multiple purpose</p>
          <div className="space-x-4"> 
            <Link to="/dashboard" className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Go to assessment
            </Link>
          </div>  
        </section>
      </div>
    </div>
    
  );
};

export default Home;
