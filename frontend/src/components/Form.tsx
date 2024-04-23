import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

const Form = ({ route, method }: { route: string; method: string }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const name = method === "login" ? "Login" : "Register";

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      let response;
      // If the method is login, send a POST request to the login endpoint
      if (method === "login") {
        //
        response = await api.post(route, {
          username,
          password,
        });
      } else {
        // If the method is register, send a POST request to the register endpoint
        response = await api.post(route, {
          username,
          password,
          email,
        });
      }
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
      if (method === "login") {
        alert("Invalid credentials");
      } else {
        alert("Username already exists");
      }
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
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      {method === "register" && (
        <input
          type="text"
          placeholder="Email"
          style={{ display: method === "register" ? "block" : "none" }}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      )}
      <button className="form-button" type="submit">
        {name}
      </button>
    </form>
  );
};

export default Form;
