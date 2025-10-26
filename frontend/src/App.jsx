import React from 'react';
import Header from './components/Header/Header.jsx';
import Home from './pages/Home.jsx';
import Profile from './pages/Profile.jsx';
import PrivateFiles from './pages/PrivateFiles.jsx';
import Files from './pages/Files.jsx';
import CreateProject from './pages/CreateProject.jsx';
import Templates from './pages/Templates.jsx';
import Calendar from './components/Calendar/Calendar.jsx';
import { AuthProvider, useAuth } from './hooks/useAuth.jsx';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// Dashboard component that shows different content based on user role
const RoleBasedDashboard = () => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <div className="loginMessage">Please log in to access the application</div>;
  }

  // Role-based content rendering
  switch (user?.role) {
    case 0: // Administrator - full access to all features
      return (
        <div className="adminDashboard">
          <h1>Administrator Dashboard</h1>
          <div className="dashboardGrid admin-equal-cards">
            <div className="dashboardCard">
              <h2>Projects</h2>
              <Home />
            </div>
            <div className="dashboardCard">
              <h2>Profile</h2>
              <Profile />
            </div>
            <div className="dashboardCard">
              <h2>Private Files</h2>
              <PrivateFiles />
            </div>
            <div className="dashboardCard">
              <h2>Templates</h2>
              <Templates />
            </div>
          </div>
        </div>
      );

    case 1: // Manager - project management and user files
      return (
        <div className="managerDashboard">
          <h1>Manager Dashboard</h1>
          <div className="dashboardGrid">
            <div className="dashboardCard">
              <h2>Projects Management</h2>
              <Home />
            </div>
            <div className="dashboardCard">
              <h2>Private Files</h2>
              <PrivateFiles />
            </div>
            <div className="dashboardCard">
              <h2>Profile</h2>
              <Profile />
            </div>
          </div>
        </div>
      );

    case 2: // User - basic access
      return (
        <div className="userDashboard">
          <h1>User Dashboard</h1>
          <div className="dashboardGrid">
            <div className="dashboardCard">
              <h2>My Projects</h2>
              <Home />
            </div>
            <div className="dashboardCard">
              <h2>Public Files</h2>
              <Files />
            </div>
            <div className="dashboardCard">
              <h2>Calendar</h2>
              <Calendar />
            </div>
          </div>
        </div>
      );

    default:
      return (
        <div className="unknownRole">
          <h1>Access Restricted</h1>
          <p>Your role is not recognized. Please contact an administrator.</p>
        </div>
      );
  }
};

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Header />
        <main>
          <RoleBasedDashboard />
        </main>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </div>
    </AuthProvider>
  );
}

export default App;
