// QueryOutput.js
import React from 'react';
import './QueryOutput.css';

function QueryOutput({ query }) {
  return (
    <div className="query-output">
      <h2>Generated Query:</h2>
      <pre>{query}</pre>
    </div>
  );
}

export default QueryOutput;
