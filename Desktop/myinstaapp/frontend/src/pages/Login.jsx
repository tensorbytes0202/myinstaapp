import React, { useState } from "react";
import { auth } from "../api/service";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await auth.login(username, password);

      console.log("Login response:", res);

      // 🔐 Token save
      localStorage.setItem("access_token", res.access_token);

      onLogin(); // redirect
    } catch (err) {
      console.error("Login error:", err);
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>

      <input
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

      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;