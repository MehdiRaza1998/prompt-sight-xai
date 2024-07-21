// Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ handleOptionChange, selectedOption }) => {
  return (
    <div className="sidebar">
      <Link
        to="/"
        className={selectedOption === 'Home' ? 'option selected' : 'option'}
        onClick={() => handleOptionChange('Home')}
      >
        Home
      </Link>
      <Link
        to="/customers"
        className={selectedOption === 'Customers' ? 'option selected' : 'option'}
        onClick={() => handleOptionChange('Customers')}
      >
        Customers
      </Link>
      <Link
        to="/reports"
        className={selectedOption === 'Reports' ? 'option selected' : 'option'}
        onClick={() => handleOptionChange('Reports')}
      >
        Reports
      </Link>
    </div>
  );
}

export default Navbar;
