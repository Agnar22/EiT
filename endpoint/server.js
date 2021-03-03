const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const audit = require('express-requests-logger');
const app = express();
const accessTokenSecret = 'somerandomaccesstoken';

const { Pool } = require('pg');
const { Client } = require('pg');
const users = [];

const client = new Client({
  user: '',
  host: '',
  database: '',
  password: '',
  port: ,
});

client.connect();

app.get('/', function (req, res) {
   res.send('Hello World');
});

app.use(bodyParser.json());

app.use(audit({
    audit:true,
    doubleAudit:true
}));

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
    client.query('INSERT INTO eit.test(ts, sensor_value) VALUES '+params+' RETURNING *', args).then(res => {
        console.log("Inserted into database.");
    }).catch(err => {
        console.log(err.stack);
    });
}

app.post('/datapoint', authenticateJWT, (req, res) => {
    fs = require('fs');
    let response_status=201;
    let response_message="Uploaded 1 datapoint.";

    try {
        insert_to_db('(current_timestamp, $1)', [req.body.value]);
    } catch (error) {
        console.log("Failed to insert a single datapoint: "+error);
        response_status=500;
        response_message="Database error.";
    }
    res.status(response_status).send(response_message);
});

app.post('/datapoints', authenticateJWT, (req, res) => {
    fs = require('fs');

    let datapoints_flattened = [];
    let parameters = "";
    let response_status=201;
    let response_message="Uploaded "+req.body.values.length+" datapoints.";

    for (let pos=0; pos<req.body.values.length; pos++) {
        //console.log(req.body.values[pos]);
        datapoints_flattened.push(req.body.values[pos]);
        if (pos==0) {
            parameters = "(current_timestamp - interval \'"+ Number(pos+1) +" seconds\', $"+ Number(pos+1) + ")"
        } else {
            parameters = parameters + ",(current_timestamp - interval \'"+Number(pos+1)+" seconds\', $"+ Number(pos+1) + ")"
        }
    }
    try {
        insert_to_db(parameters, datapoints_flattened);
    } catch (error) {
        console.log("Failed to insert multiple datapoints: "+error);
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
    console.log('Authentication service started on port 4013.');
});
