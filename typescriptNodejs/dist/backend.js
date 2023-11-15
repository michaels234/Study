import express from 'express';
import mysql from 'mysql';
import cors from 'cors';
const myFunction = () => {
    const app = express();
    app.use(cors());
    app.use(express.json());
    // MySQL configuration (replace with your actual database details)
    const dbConfig = {
        host: 'localhost',
        user: 'root',
        password: 'password',
        database: 'typescriptnodejsdb',
    };
    // Create a connection to MySQL
    const connection = mysql.createConnection(dbConfig);
    // Connect to the database
    connection.connect();
    // API endpoint to handle the user ID and fetch data from the database
    app.post('/api/data', (req, res) => {
        const userId = parseInt(req.body.userId, 10);
        // Example SQL query using parameterized query
        const sqlQuery = 'SELECT * FROM users WHERE user_id = ?';
        // Execute the parameterized SQL query
        connection.query(sqlQuery, [userId], (error, results) => {
            if (error) {
                console.error('Error in SQL query:', error);
                res.status(500).json({ error: 'Internal Server Error' });
            }
            else {
                // Send the results back in the API response
                res.json(results);
            }
        });
    });
    // Close the MySQL connection when the server is closed
    app.on('close', () => {
        connection.end();
    });
    // Start the server on port 3000
    const PORT = 3000;
    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
    });
};
myFunction();
