import React from 'react';
import styles from './Card.module.css';

const Card = ({ title, subtitle, price, deliveryTime, buttonText = '-', onButtonClick }) => {
  if (!title && !subtitle && !price && !deliveryTime) {
    // Empty card with only plus button
    return (
      <div className={`${styles.card} ${styles.emptyCardWrapper}`}>
        <div className={styles.emptyCard}>
          <button className={styles.minusBtn} onClick={onButtonClick}>
            {buttonText}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <h3 className={styles.title}>{title}</h3>
        <span className={styles.dropdownIcon}>▼</span>
      </div>
      <p className={styles.subtitle}>{subtitle}</p>
      <div className={styles.priceSection}>
        <span className={styles.price}>{price}</span>
        <button className={styles.minusBtn} onClick={onButtonClick}>
          {buttonText}
        </button>
      </div>
      <p className={styles.deliveryTime}>{deliveryTime}</p>
    </div>
  );
};

export default Card;
