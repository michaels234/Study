"use strict";
// Sample frontend TypeScript code
const apiUrl = 'http://localhost:3000/api/data';
// Function to handle API requests
async function makeApiRequest(url, method, data) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: data ? JSON.stringify(data) : undefined,
    };
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
}
// Async function to handle API request and display results
async function handleApiRequest() {
    // Example of sending a POST request with a user ID
    const userId = 1; // Replace with the actual user ID
    const apiResponse = await makeApiRequest(apiUrl, 'POST', { userId });
    // Handle the API response outside of the then block
    const results = displayResults(apiResponse);
    console.log('Results:', results); // Results: [{"name": "john", "age": 23}]
}
// Function to display results in HTML and return them
function displayResults(results) {
    const resultContainer = document.getElementById('result-container');
    if (resultContainer) {
        resultContainer.innerHTML = '<h3>Results:</h3>';
        // Assuming results is an array of objects
        results.forEach((result) => {
            const resultItem = document.createElement('div');
            resultItem.textContent = JSON.stringify(result);
            resultContainer.appendChild(resultItem);
        });
    }
    return results;
}
// Call the async function to start the process
handleApiRequest();
