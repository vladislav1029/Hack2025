import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, ApiError } from '../utils/api';
import { toast } from 'react-toastify';

// Auth context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state on app start
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const userData = await authAPI.getCurrentUser();
        setUser(userData);
      }
    } catch (error) {
      // Token is invalid or expired, remove it
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      setError(null);
      setLoading(true);

      const response = await authAPI.login(username, password);

      // Store tokens
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('token_type', response.token_type);

      // Get user data
      const userData = await authAPI.getCurrentUser();
      setUser(userData);

      // Show success notification with role
      toast.success(`Welcome back! You are logged in as ${getRoleName(userData.role)}.`, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });

      return {
        success: true,
        user: userData
      };
    } catch (error) {
      let errorMessage = 'Login failed. Please check your credentials.';

      if (error instanceof ApiError) {
        if (error.status === 401) {
          errorMessage = 'Invalid username or password.';
        } else if (error.status === 422) {
          errorMessage = 'Please check your input data.';
        } else {
          errorMessage = error.message || errorMessage;
        }
      }

      // Show error notification
      toast.error(errorMessage, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });

      setError(errorMessage);
      return {
        success: false,
        message: errorMessage
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, password) => {
    try {
      setError(null);
      setLoading(true);

      const response = await authAPI.register(email, password);

      // After successful registration, log the user in
      const loginResponse = await login(email, password);

      // Show success notification
      toast.success('Registration successful! Welcome!', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });

      return {
        success: true,
        message: 'Registration successful! Welcome!'
      };
    } catch (error) {
      let errorMessage = 'Registration failed. Please try again.';

      if (error instanceof ApiError) {
        if (error.status === 422) {
          errorMessage = 'Please check your email and password.';
        } else {
          errorMessage = error.message || errorMessage;
        }
      }

      // Show error notification
      toast.error(errorMessage, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });

      setError(errorMessage);
      return {
        success: false,
        message: errorMessage
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      // Continue with logout even if API call fails
      console.warn('Logout API call failed:', error);
    } finally {
      // Clear local storage and state
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      setUser(null);
      setError(null);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const getRoleName = (role) => {
    switch (role) {
      case 0: return 'User';
      case 1: return 'Moderator';
      case 2: return 'Administrator';
      default: return 'Unknown';
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    isAuthenticated: !!user,
    getRoleName,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
