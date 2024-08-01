// UserQueryInput.js
import React, { useState } from 'react';
import './UserQueryInput.css';

function UserQueryInput({ userQuery, setUserQuery, onUserQuerySubmitLlama, onUserQuerySubmitGemini }) {

  return (
    <div className="user-query-form">
      <h2>Enter Your Query in Natural Language:</h2>
      <input
        className="user-query-input"
        type="text"
        value={userQuery}
        onChange={(e) => setUserQuery(e.target.value)}
        placeholder="E.g., Show me customers who bought yesterday."
      />
      <div className='centered-div'>
        <button onClick={onUserQuerySubmitLlama} className="submit-btn">Generate SQL Query (LLama)</button>
        <button onClick={onUserQuerySubmitGemini} className="submit-btn">Generate SQL Query (Gemini)</button>
      </div>
    </div>
  );
}

export default UserQueryInput;
