import React, { createContext, useState, useCallback, useEffect } from "react";
import { auth } from "../api/services";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if user is already logged in
  useEffect(() => {
    if (token) {
      setUser({ id: 1, username: "aditya" }); // Placeholder - should be from JWT
    }
  }, [token]);

  const signup = useCallback(async (username, password) => {
    setLoading(true);
    setError(null);

    try {
      const response = await auth.signup(username, password);
      setUser(response);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (username, password) => {
    setLoading(true);
    setError(null);

    try {
      const response = await auth.login(username, password);
      
      if (response.access_token) {
        localStorage.setItem("access_token", response.access_token);
        setToken(response.access_token);
        setUser({ id: 1, username }); // Placeholder
      }
      
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    token,
    loading,
    error,
    signup,
    login,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  
  return context;
};