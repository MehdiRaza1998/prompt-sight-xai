import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Changed import for BrowserRouter
import Header from './components/common/Header';
import Navbar from './components/common/Navbar';
import Welcome from './components/Welcome';
import CustomersPage from './pages/CustomersPage';
import ReportsPage from './pages/ReportsPage';

function App() {
  const [selectedOption, setSelectedOption] = useState('/');

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  return (
    <Router>
      <div className="App">
        <Header />
        <div className="content-container">
          <Navbar handleOptionChange={handleOptionChange} selectedOption={selectedOption} />
          <div className="route-container">
            <Routes>
              <Route path="/" element={<Welcome />} />
              <Route path="/customers" element={<CustomersPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              {/* Other routes go here */}
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
