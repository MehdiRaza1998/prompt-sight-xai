// SchemaInput.js
import React from 'react';
import './SchemaInput.css';

function SchemaInput({ schema, onSchemaChange }) {
  return (
    <div className="schema-input-container">
      <h2>Enter Database Schema:</h2>
      <textarea
        className="schema-textarea"
        onChange={(e) => onSchemaChange(e.target.value)}
        placeholder="Type your schema here..."
        rows={6}
        value={schema}
      />
    </div>
  );
}

export default SchemaInput;
