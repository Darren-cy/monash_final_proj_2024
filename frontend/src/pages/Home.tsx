import { useState } from "react";
import api from "../api";

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
  }
  return (
    <div>
        <h1>Welcome to document processing app</h1>
        <button onClick={getData}>Get Data</button>
    </div>
  )
}

export default Home