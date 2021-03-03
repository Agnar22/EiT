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

function insert_to_db(params, args) {
        const pool = new Pool({
          user: 'node_eit',
          host: 'localhost',
          database: 'postgres',
          password: 'node_eit_jernbane_pwd',
          port: 5432,
        });

        pool.query('INSERT INTO eit.test(ts, sensor_value) VALUES '+params, args).then(res => {
            pool.end();
        }).catch(err => {
            throw new Error("Database error.");
        });
}

app.post('/datapoint', authenticateJWT, (req, res) => {
    fs = require('fs');
    console.log(req.body.value);

    try {
        insert_to_db('(current_timestamp, $1)', [req.body.value]);
    } catch (e) {
        response_status=500;
        response_message="Database error.";
    }
    res.status(response_status).send(response_message);
});


app.post('/datapoints', authenticateJWT, (req, res) => {
    fs = require('fs');
    console.log(req.body.values);


    let datapoints_flattened = [];
    let parameters = "";
    let response_status=201;
    let response_message="Uploaded "+req.body.values.length+" datapoints.";

    for (let pos=0; pos<req.body.values.length; pos++) {
        console.log(req.body.values[pos]);
        datapoints_flattened.push(req.body.values[pos]);
        if (pos==0) {
            parameters = "(current_timestamp - interval \'"+ Number(pos+1) +" seconds\', $"+ Number(pos+1) + ")"
        } else {
            parameters = parameters + ",(current_timestamp - interval \'"+Number(pos+1)+" seconds\', $"+ Number(pos+1) + ")"
        }
    }
    try {
        insert_to_db(parameters, datapoints_flattened).then();
    } catch (e) {
        response_status=500;
        response_message="Database error.";
    }
    res.status(response_status).send(response_message);
});


app.post('/login', (req, res) => {
    // Read username and password from request body.
    const { username, password } = req.body;
    console.log(req.body.username);

    // Filter user from the users array by username and password.
    const user = users.find(u => { return u.username === username && u.password === password });

    if (user) {
        // Generate an access token.
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
