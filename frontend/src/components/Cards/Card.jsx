import React from 'react';
import styles from './Card.module.css';

const Card = ({ title, subtitle, price, deliveryTime }) => {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <h3 className={styles.title}>{title}</h3>
        <span className={styles.dropdownIcon}>▼</span>
      </div>
      <p className={styles.subtitle}>{subtitle}</p>
      <div className={styles.priceSection}>
        <span className={styles.price}>{price}</span>
        <button className={styles.minusBtn}>-</button>
      </div>
      <p className={styles.deliveryTime}>{deliveryTime}</p>
    </div>
  );
};

export default Card;
