import React, { useState } from 'react';
import Modal from './Modal';
import styles from './LoginModal.module.css';
import { useAuth } from '../../hooks/useAuth';

const LoginModal = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState('login');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login, register } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isSubmitting) return;

    // Validation
    if (activeTab === 'register') {
      if (formData.password !== formData.confirmPassword) {
        return;
      }
      if (formData.password.length < 6) {
        return;
      }
    }

    setIsSubmitting(true);

    try {
      if (activeTab === 'login') {
        await login(formData.username, formData.password);
      } else {
        await register(formData.email, formData.password);
      }

      // Close modal on success (notifications are handled in useAuth)
      resetForm();
      onClose();
    } catch (error) {
      // Error notifications are handled in useAuth
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    resetForm();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className={styles.loginModal}>
        {/* Заголовок */}
        <div className={styles.header}>
          <div className={styles.userIcon}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <h2 className={styles.title}>Ligo In</h2>
        </div>

        {/* Вкладки */}
        <div className={styles.tabs}>
          <button
            type="button"
            className={`${styles.tab} ${activeTab === 'login' ? styles.activeTab : ''}`}
            onClick={() => setActiveTab('login')}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`${styles.tab} ${activeTab === 'register' ? styles.activeTab : ''}`}
            onClick={() => setActiveTab('register')}
          >
            Sign Up
          </button>
        </div>

        {/* Форма */}
        <form onSubmit={handleSubmit} className={styles.form}>
          {/* Поле username */}
          <div className={styles.inputGroup}>
            <div className={styles.inputIcon}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="username"
              className={styles.input}
              required
            />
          </div>

          {/* Поле email (только для регистрации) */}
          {activeTab === 'register' && (
            <div className={styles.inputGroup}>
              <div className={styles.inputIcon}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="22,6 12,13 2,6" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="email"
                className={styles.input}
                required
              />
            </div>
          )}

          {/* Поле password */}
          <div className={styles.inputGroup}>
            <div className={styles.inputIcon}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="password"
              className={styles.input}
              required
            />
          </div>

          {/* Поле подтверждения пароля (только для регистрации) */}
          {activeTab === 'register' && (
            <div className={styles.inputGroup}>
              <div className={styles.inputIcon}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                  <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="confirm password"
                className={styles.input}
                required
              />
            </div>
          )}

          {/* Кнопка */}
          <button
            type="submit"
            className={styles.signInButton}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <span className={styles.loadingText}>
                <svg className={styles.spinner} width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" strokeDasharray="32" strokeDashoffset="32">
                    <animate attributeName="stroke-dashoffset" dur="1s" values="32;0;32" repeatCount="indefinite"/>
                  </circle>
                </svg>
                {activeTab === 'login' ? 'Signing In...' : 'Signing Up...'}
              </span>
            ) : (
              activeTab === 'login' ? 'Sign In' : 'Sign Up'
            )}
          </button>
        </form>
      </div>
    </Modal>
  );
};

export default LoginModal;
