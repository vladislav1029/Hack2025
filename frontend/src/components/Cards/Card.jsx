import React from 'react';
import styles from './Card.module.css';

const Card = ({ title, subtitle, price, deliveryTime, buttonText = '-', onButtonClick, onExpand, isExpanded = false }) => {
  const handleExpandClick = () => {
    if (onExpand) {
      onExpand();
    }
  };

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
    <div className={`${styles.card} ${isExpanded ? styles.expanded : ''}`}>
      <div className={styles.cardHeader}>
        <h3 className={styles.title}>{title}</h3>
        <button className={styles.threeDotBtn} onClick={handleExpandClick}>
          ⋮
        </button>
      </div>
      <p className={styles.subtitle}>{subtitle}</p>
      <div className={styles.priceSection}>
        <span className={styles.price}>{price}</span>
        <button className={styles.minusBtn} onClick={onButtonClick}>
          {buttonText}
        </button>
      </div>
      <p className={styles.deliveryTime}>{deliveryTime}</p>
      {isExpanded && (
        <div className={styles.expandedContent}>
          <div className={styles.detailRow}>
            <span className={styles.detailLabel}>Описание:</span>
            <span className={styles.detailValue}>Подробное описание проекта {title} с дополнительными характеристиками и требованиями.</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailLabel}>Категория:</span>
            <span className={styles.detailValue}>{subtitle}</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailLabel}>Сложность:</span>
            <span className={styles.detailValue}>Средняя</span>
          </div>
          <div className={styles.detailRow}>
            <span className={styles.detailLabel}>Технологии:</span>
            <span className={styles.detailValue}>React, Node.js, MongoDB</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Card;
