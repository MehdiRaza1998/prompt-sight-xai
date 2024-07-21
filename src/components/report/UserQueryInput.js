// UserQueryInput.js
import React, { useState } from 'react';
import './UserQueryInput.css';

function UserQueryInput({userQuery, setUserQuery, onUserQuerySubmit }) {

  const handleSubmit = (event) => {
    event.preventDefault();
    onUserQuerySubmit();
  };

  return (
    <form onSubmit={handleSubmit} className="user-query-form">
      <h2>Enter Your Query in Natural Language:</h2>
      <input
        className="user-query-input"
        type="text"
        value={userQuery}
        onChange={(e) => setUserQuery(e.target.value)}
        placeholder="E.g., Show me customers who bought yesterday."
      />
      <button type="submit" className="submit-btn">Generate SQL Query</button>
    </form>
  );
}

export default UserQueryInput;
