import React from 'react';
import styles from './Header.module.css';

const Header = () => {
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
            <button className={styles.signInBtn}>Sign In</button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
