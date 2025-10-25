import React, { useState } from 'react';
import LoginModal from '../components/Modal/LoginModal.jsx';
import Button from '../components/Buttons/Button.jsx';
import './LandingPage.css';

const LandingPage = () => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  const openLoginModal = () => setIsLoginModalOpen(true);
  const closeLoginModal = () => setIsLoginModalOpen(false);

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to Adabe</h1>
          <p className="hero-subtitle">
            Advanced project management and file collaboration platform built for teams of all sizes
          </p>
          <div className="hero-buttons">
            <Button
              onClick={openLoginModal}
              className="primary-button"
              text="Get Started"
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2 className="section-title">Why Choose Adabe?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📋</div>
              <h3 className="feature-title">Project Management</h3>
              <p className="feature-description">
                Create, organize, and track your projects with an intuitive dashboard.
                Manage tasks, deadlines, and collaborate with your team efficiently.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3 className="feature-title">Secure File Management</h3>
              <p className="feature-description">
                Store and share files securely. Access private files with role-based permissions.
                Download temporary links for easy sharing.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3 className="feature-title">Role-Based Access</h3>
              <p className="feature-description">
                Different access levels for administrators, managers, and users.
                Tailored dashboards based on your responsibilities.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3 className="feature-title">Analytics & Reports</h3>
              <p className="feature-description">
                Get insights into your projects and team performance.
                Track progress, productivity, and resource utilization.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3 className="feature-title">Real-time Collaboration</h3>
              <p className="feature-description">
                Work together seamlessly with real-time updates and notifications.
                Stay connected and informed about project changes.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3 className="feature-title">Responsive Design</h3>
              <p className="feature-description">
                Access your data from any device. Our responsive interface works
                perfectly on desktops, tablets, and mobile phones.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="steps-grid">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Register Account</h3>
              <p>Create your account and choose your role in the system</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Set Up Dashboard</h3>
              <p>Get a personalized dashboard based on your role and permissions</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Start Collaborating</h3>
              <p>Create projects, upload files, and collaborate with your team</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Transform Your Workflow?</h2>
            <p>Join thousands of teams already using Adabe for their project management needs.</p>
            <Button
              onClick={openLoginModal}
              className="cta-button"
              text="Sign In or Register Now"
            />
          </div>
        </div>
      </section>

      {/* Login Modal */}
      <LoginModal isOpen={isLoginModalOpen} onClose={closeLoginModal} />
    </div>
  );
};

export default LandingPage;
