import axios from 'axios';
import { GEMINI_API, OPENAI_API, TOKEN } from '../constants/llama';
import LlamaAI from 'llamaai';
import OpenAI from 'openai';
const { GoogleGenerativeAI } = require("@google/generative-ai");

const apiToken = TOKEN;
const llamaAPI = new LlamaAI(apiToken);
const openai = new OpenAI({ apiKey: OPENAI_API, dangerouslyAllowBrowser: true });


// const systemPrompt = `
// You are a highly intelligent SQL query generator. Your task is to generate a SQL query based on the provided schema and user question.
// Schema: {schema}
// If any part of the question is outside the scope of the schema, indicate that in your response.
// Return only the SQL query within *genQuery object. Format: *genQuery='SELECT * FROM ...'
// After generating the SQL query, provide a detailed explanation of each part of the query. Format the explanation as follows:
// *Explanation: "This part of the query corresponds to ..."
// No additional text or comments should be included.`;

// const systemPrompt = `
// You are a highly intelligent SQL query generator and explainer. Your task is to generate a SQL query based on the provided schema and user question, and then explain the query by linking each part of the input to the corresponding part of the SQL query in a table format.
// Schema: {schema}
// If any part of the question is outside the scope of the schema, indicate that in your response.
// Return the SQL query within *genQuery object. Format: *genQuery='SELECT * FROM ...'
// After generating the SQL query, provide a detailed explanation in a table format. Each row should link a part of the input to its corresponding part in the query. Format the explanation as follows:
// *Explanation: | Input Element | SQL Query Element | Explanation |
// No additional text or comments should be included.`;



const systemPrompt = `
You are a highly intelligent SQL query generator and explainer. Your task is to generate a SQL query based on the provided schema and user question, and then explain the query by linking each part of the input to the corresponding part of the SQL query in a detailed manner.
Schema: {schema}
If any part of the question is outside the scope of the schema, indicate that in your response.
Return the SQL query within *genQuery object. Format: *genQuery='SELECT * FROM ...'
After generating the SQL query, provide a detailed explanation in JSON format. Each object should link a part of the input to its corresponding part in the query.
Format:
[
  { 'input_element': 'input part', 'output_element': 'query part', 'explanation': 'reasoning' },
  ...
]
No additional text or comments should be included.`;

const systemPromptOthers = `
You are a highly intelligent SQL query generator and explainer. Your task is to generate a SQL query based on the provided schema and user question, and then explain the query by linking each part of the input to the corresponding part of the SQL query in a detailed manner.
Schema: {schema} and Question: {question} 
If any part of the question is outside the scope of the schema, indicate that in your response.
Return the SQL query within '*genQuery' object, '*' is must. Format: *genQuery='SELECT * FROM ...'
After generating the SQL query, provide a detailed explanation in JSON format. Each object should link a part of the input to its corresponding part in the query.
Format:
[
  { 'input_element': 'input part', 'output_element': 'query part', 'explanation': 'reasoning' },
  ...
]
No additional text or comments should be included.`;

const getApiRequestJsonQuery = (schema, userQuestion) => {
    const prompt = systemPrompt.replace("{schema}", schema);
    return {
        "messages": [
            { "role": "system", "content": prompt },
            {
                "role": "user",
                "content": userQuestion
            }
        ],
        "stream": false,
        "max_tokens": 1024
    }
};
//LLAMA
export const runLlama = async (schema, question) => {
    const requestGot = getApiRequestJsonQuery(schema, question);

    try {
        const response = await llamaAPI.run(requestGot);
        const content = response.choices[0].message.content;
        const query = getFormatted(content, 'query');
        const explanation = getFormatted(content, 'explanation');
        return { query, explanation };
    } catch (error) {
        console.error('Error generating query:', error);
        return { query: "ERROR: " + error, explanation: "ERROR: " + error };
    }
};

//GEMINI
export const runGemini = async (schema, question) => {
    const genAI = new GoogleGenerativeAI(GEMINI_API);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash"});

    let prompt = systemPromptOthers.replace("{schema}", schema).replace("{question}", question)

    try {
        const result = await model.generateContent(prompt);
        const content = result.response.text()
        const query = getFormatted(content, 'query');
        const explanation = getFormatted(content, 'explanation');
        return { query, explanation };
    } catch (error) {
        console.error('Error generating SQL query:', error);
        return null;
    }
}


const getFormatted = (response, type) => {
    if (type === 'query') {
        const match = response.match(/\*genQuery=['"](.*?)['"]/);
        return match ? match[1] : "Could not parse the query. Please check the input.";
    } else if (type === 'explanation') {
        const explanationStart = response.indexOf("[");
        const explanationEnd = response.lastIndexOf("]");
        return explanationStart !== -1 && explanationEnd !== -1 ? JSON.parse(response.substring(explanationStart, explanationEnd + 1)) : [];
    }
};


//for second
// const getFormatted = (response, type) => {
//     if (type === 'query') {
//         const match = response.match(/\*genQuery=['"](.*?)['"]/);
//         return match ? match[1] : "Could not parse the query. Please check the input.";
//     } else if (type === 'explanation') {
//         const explanationStart = response.indexOf("Explanation:");
//         return explanationStart !== -1 ? response.substring(explanationStart) : "Could not parse the explanation. Please check the input.";
//     }
// };