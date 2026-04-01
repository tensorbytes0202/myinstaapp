import React, { useState } from "react";
import { auth } from "../api/service";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      await auth.signup(username, password);
      alert("Signup successful! Now login");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Signup</h2>

      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleSignup}>Signup</button>
    </div>
  );
};

export default Signup;