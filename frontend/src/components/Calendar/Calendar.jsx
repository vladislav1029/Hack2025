import React, { useState } from 'react';
import styles from './Calendar.module.css';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);

  // Days of the week
  const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Months array
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Get days in month
  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];

    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }

    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }

    return days;
  };

  // Navigate to previous month
  const previousMonth = () => {
    setCurrentDate(prev => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  };

  // Navigate to next month
  const nextMonth = () => {
    setCurrentDate(prev => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  };

  // Navigate to previous year
  const previousYear = () => {
    setCurrentDate(prev => new Date(prev.getFullYear() - 1, prev.getMonth(), 1));
  };

  // Navigate to next year
  const nextYear = () => {
    setCurrentDate(prev => new Date(prev.getFullYear() + 1, prev.getMonth(), 1));
  };

  // Check if date is today
  const isToday = (day) => {
    const today = new Date();
    return (
      day === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    );
  };

  // Check if date is selected
  const isSelected = (day) => {
    if (!selectedDate) return false;
    return (
      day === selectedDate.getDate() &&
      currentDate.getMonth() === selectedDate.getMonth() &&
      currentDate.getFullYear() === selectedDate.getFullYear()
    );
  };

  // Handle date selection
  const selectDate = (day) => {
    if (day) {
      const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
      setSelectedDate(newDate);
      console.log('Selected date:', newDate.toDateString());
    }
  };

  const days = getDaysInMonth(currentDate);

  return (
    <div className={styles.calendar}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.yearNavigation}>
          <button onClick={previousYear} className={styles.navBtn}>{'<<'}</button>
          <span className={styles.year}>{currentDate.getFullYear()}</span>
          <button onClick={nextYear} className={styles.navBtn}>{'>>'}</button>
        </div>

        <div className={styles.monthNavigation}>
          <button onClick={previousMonth} className={styles.navBtn}>{'<'}</button>
          <span className={styles.month}>
            {months[currentDate.getMonth()]} {currentDate.getFullYear()}
          </span>
          <button onClick={nextMonth} className={styles.navBtn}>{'>'}</button>
        </div>
      </div>

      {/* Weekdays header */}
      <div className={styles.weekdays}>
        {weekdays.map(day => (
          <div key={day} className={styles.weekday}>
            {day}
          </div>
        ))}
      </div>

      {/* Calendar grid */}
      <div className={styles.days}>
        {days.map((day, index) => (
          <div
            key={index}
            className={`${styles.day} ${day ? styles.dayCell : styles.emptyDay}
                       ${isToday(day) ? styles.today : ''}
                       ${isSelected(day) ? styles.selected : ''}`}
            onClick={() => selectDate(day)}
          >
            {day || ''}
          </div>
        ))}
      </div>

      {/* Selected date info */}
      {selectedDate && (
        <div className={styles.selectedDate}>
          Selected: {selectedDate.toDateString()}
        </div>
      )}
    </div>
  );
};

export default Calendar;
