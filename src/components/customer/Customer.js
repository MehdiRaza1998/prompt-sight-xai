// Customer.js
import React, { useState } from 'react';
import './Customer.css'; // Import CSS for Customer component

const Customer = () => {
  // Dummy customer data with an additional "age" attribute
  const [customers, setCustomers] = useState([
    { id: 1, name: 'John Doe', email: 'john@example.com', phone: '123-456-7890', age: 30 },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '987-654-3210', age: 25 },
    { id: 3, name: 'Alice Johnson', email: 'alice@example.com', phone: '456-789-0123', age: 35 }
  ]);

  // Function to add a new customer
  const handleAddCustomer = () => {
    const newCustomer = {
      id: customers.length + 1,
      name: 'New Customer'+customers.length+1,
      email: 'newcustomer@example.com',
      phone: '123-456-7890',
      age: 25
    };
    setCustomers([...customers, newCustomer]);
  };

  return (
    <div className="customer-container">
      <h2 className="center">Customer List</h2>
      <button type='primary' onClick={handleAddCustomer}>Add Customer</button>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Age</th>
          </tr>
        </thead>
        <tbody>
          {customers.map(customer => (
            <tr key={customer.id}>
              <td>{customer.id}</td>
              <td>{customer.name}</td>
              <td>{customer.email}</td>
              <td>{customer.phone}</td>
              <td>{customer.age}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Customer;
