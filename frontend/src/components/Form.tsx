import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

const Form = ({ route, method }: { route: string; method: string }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const name = method === "login" ? "Login" : "Register";

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      const response = await api.post(route, {
        username,
        password,
      });
      if (method === "login") {
        alert("User logged in successfully");
        localStorage.setItem(ACCESS_TOKEN, response.data.accessToken);
        navigate("/");
      } else {
        alert("User registered successfully");
        navigate("/login");
      }
    } catch (error) {
      console.error(error);
      alert("Invalid credentials");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{name}</h1>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="form-button" type="submit">
        {name}
      </button>
    </form>
  );
};

export default Form;
