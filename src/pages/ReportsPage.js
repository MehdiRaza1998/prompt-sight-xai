// ReportsPage.js
import React, { useState } from 'react';
import SchemaInput from '../components/report/SchemaInput';
import UserQueryInput from '../components/report/UserQueryInput';
import QueryOutput from '../components/report/QueryOutput';
import Explanation from '../components/report/Explanation';
import { runLlama } from '../services/llamaService';

function ReportsPage() {
  const [schema, setSchema] = useState('{name: varchar, age:number, has_glasses: boolean, married_status: boolean}');
  const [userQuery, setUserQuery] = useState('Show me the users who wear glasses and are married above 50 years age');
  const [generatedQuery, setGeneratedQuery] = useState('');
  const [explanation, setExplanation] = useState([]);

  const handleUserQuerySubmit = async () => {
    console.log('Schema:', schema);
    console.log('User Query:', userQuery);
    setGeneratedQuery('');


    try {
      const responseGot = await runLlama(schema, userQuery);
      setGeneratedQuery(responseGot.query);
      setExplanation(responseGot.explanation);
    } catch (error) {
      console.error('Error in generating query:', error);
      setGeneratedQuery('Error in generating query');
    }
};

  return (
    <div className="reports-page">
      <SchemaInput schema={schema} onSchemaChange={setSchema} />
      <UserQueryInput userQuery={userQuery} setUserQuery={setUserQuery} onUserQuerySubmit={handleUserQuerySubmit} />
      <QueryOutput query={generatedQuery} />
      <Explanation explanation={explanation} />
    </div>
  );
}

export default ReportsPage;
