// Explanation.js
import React from 'react';
import './Explanation.css';

function Explanation({ explanation }) {
  return (
    <div className="explanation">
      <h2>Explanation:</h2>
      <table>
        <thead>
          <tr>
            <th>Input Element</th>
            <th>SQL Query Element</th>
            <th>Explanation</th>
          </tr>
        </thead>
        <tbody>
          {explanation.map((item, index) => (
            <tr key={index}>
              <td>{item.input_element}</td>
              <td>{item.output_element}</td>
              <td>{item.explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Explanation;
