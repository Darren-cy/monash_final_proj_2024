import { useState } from "react";
import api from "../api";
import NavigationBar from "../components/NavigationBar";

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
    <>
      <NavigationBar></NavigationBar>
      <h1>Welcome to document processing app</h1>
    </>
  );
};

export default Home;
