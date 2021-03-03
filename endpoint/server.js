const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');

const app = express();

const accessTokenSecret = 'somerandomaccesstoken';

const { Pool } = require('pg');

const users = [
    {
        username: 'john',
        password: 'password123admin',
        role: 'admin'
    }, {
        username: 'anna',
        password: 'password123member',
        role: 'member'
    }
]

app.use(bodyParser.json());

const authenticateJWT = (req, res, next) => {
    const authHeader = req.headers.authorization;

    if (authHeader) {
        const token = authHeader.split(' ')[1];

        jwt.verify(token, accessTokenSecret, (err, user) => {
            if (err) {
                return res.sendStatus(403);
            }
            req.user = user;
            next();
        });
    } else {
        res.sendStatus(401);
    }
};

app.post('/datapoint', authenticateJWT, (req, res) => {
    fs = require('fs');
    console.log(req.body.value);

    const pool = new Pool({
      user: 'node_eit',
      host: 'localhost',
      database: 'postgres',
      password: 'node_eit_jernbane_pwd',
      port: 5432,
    });

    pool.query('INSERT INTO eit.test(ts, sensor_value) VALUES (current_timestamp, $1)', [req.body.value], (err, res) => {
      console.log(err, res) 
      pool.end() 
    });

    res.sendStatus(201);
});


app.post('/login', (req, res) => {
    // read username and password from request body
    const { username, password } = req.body;
    console.log(req.body.username);

    // filter user from the users array by username and password
    const user = users.find(u => { return u.username === username && u.password === password });

    if (user) {
        // generate an access token
        //const accessToken = jwt.sign({ username: user.username, role: user.role }, accessTokenSecret, { expiresIn: '20m' });
        const accessToken = jwt.sign({ username: user.username, role: user.role }, accessTokenSecret);

        res.json({
            accessToken
        });
    } else {
        res.send('Username or password incorrect');
    }
});

app.listen(4013, () => {
    console.log('Authentication service started on port 3000');
});
