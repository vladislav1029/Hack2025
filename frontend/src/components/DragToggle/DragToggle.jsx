import React from 'react';
import styles from './DragToggle.module.css';

const DragToggle = ({ isDragMode, onToggle }) => {
  return (
    <button
      className={`${styles['drag-toggle']} ${isDragMode ? styles.active : ''}`}
      onClick={onToggle}
      title={isDragMode ? 'Отключить перемещение компонентов' : 'Включить перемещение компонентов'}
      aria-label={isDragMode ? 'Зафиксировать компоненты' : 'Разблокировать компоненты для перемещения'}
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={isDragMode ? 'lock-open' : 'lock-closed'}
      >
        {isDragMode ? (
          // Open lock icon (drag mode enabled)
          <>
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <circle cx="12" cy="16" r="1"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </>
        ) : (
          // Closed lock icon (drag mode disabled)
          <>
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <circle cx="12" cy="16" r="1"/>
            <path d="M7 11V7a5 5 0 0 1 9.9-1"/>
          </>
        )}
      </svg>
      <span className={styles['toggle-text']}>
        {isDragMode ? 'Редактирование' : 'Перемещение'}
      </span>
    </button>
  );
};

export default DragToggle;
