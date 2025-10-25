import React, { useState } from 'react';
import styles from './Filter.module.css';

const Filter = () => {
  const [budgetToggle, setBudgetToggle] = useState(true);
  const [category, setCategory] = useState('timerange');

  return (
    <div className={styles.filter}>
      <div className={styles.filterHeader}>
        <span className={styles.filterIcon}>🔍</span>
        <h3 className={styles.filterTitle}>Filter</h3>
        <span className={styles.arrowIcon}>←</span>
      </div>
      <div className={styles.filterContent}>
        <div className={styles.filterGroup}>
          <label className={styles.label}>Budget</label>
          <div className={styles.toggleContainer}>
            <span className={styles.toggleLabel}>timerange</span>
            <label className={styles.switch}>
              <input
                type="checkbox"
                checked={budgetToggle}
                onChange={() => setBudgetToggle(!budgetToggle)}
              />
              <span className={styles.slider}></span>
            </label>
          </div>
        </div>
        <div className={styles.filterGroup}>
          <label className={styles.label}>Category</label>
          <select
            className={styles.select}
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="timerange">timerange</option>
            <option value="option1">Option 1</option>
            <option value="option2">Option 2</option>
          </select>
        </div>
      </div>
      <button className={styles.filterBtn}>Filter</button>
    </div>
  );
};

export default Filter;
