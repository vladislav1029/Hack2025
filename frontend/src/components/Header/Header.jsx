import React, { useState } from 'react';
import styles from './Header.module.css';
import LoginModal from '../Modal/LoginModal';
import { useAuth } from '../../hooks/useAuth';

const Header = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { user, logout, isAuthenticated } = useAuth();

  const handleSignInClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.header__content}>
          {/* Логотип */}
          <div className={styles.header__logo}>
            <div className={styles.logoIcon}>N</div>
            <span className={styles.logoText}>Adabe Ab</span>
          </div>

          {/* Действия */}
          <div className={styles.header__actions}>
            {isAuthenticated ? (
              <div className={styles.userMenu}>
                <span className={styles.userInfo}>
                  Welcome, {user?.email} ({user?.role === 0 ? 'Administrator' : user?.role === 1 ? 'Manager' : 'User'})
                </span>
                <button className={styles.logoutBtn} onClick={handleLogout}>
                  Logout
                </button>
              </div>
            ) : (
              <button className={styles.signInBtn} onClick={handleSignInClick}>
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>
      <LoginModal isOpen={isModalOpen} onClose={handleCloseModal} />
    </header>
  );
};

export default Header;
