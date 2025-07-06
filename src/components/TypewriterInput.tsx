import React, { useState, useEffect } from 'react';
import styles from '../styles/TypewriterInput.module.css';

interface TypewriterInputProps {
  text: string;
  className?: string;
}

const TypewriterInput: React.FC<TypewriterInputProps> = ({ text, className }) => {
  const [placeholder, setPlaceholder] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index <= text.length) {
      const timeout = setTimeout(() => {
        setPlaceholder(text.slice(0, index));
        setIndex(index + 1);
      }, 100);

      return () => clearTimeout(timeout);
    } else {
      // Reset after completing
      const timeout = setTimeout(() => {
        setIndex(0);
      }, 3000); // Wait 3 seconds before restarting

      return () => clearTimeout(timeout);
    }
  }, [index, text]);

  return (
    <input
      type="text"
      placeholder={placeholder}
      className={`${styles.typewriterInput} ${className || ''}`}
    />
  );
};

export default TypewriterInput; 