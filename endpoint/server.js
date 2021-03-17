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
    client.query('INSERT INTO eit.sensor_values(ts, gforce_x, gforce_y, gforce_z, orientation_roll, orientation_pitch, orientation_yaw, lat, lon) VALUES '+params+' RETURNING *', args).then(res => {
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
        datapoints_flattened.push(req.body.values[pos][0]);
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


app.post('/datapoints_all_sensors', authenticateJWT, (req, res) => {
    fs = require('fs');

    let num_sensors = 9;
    let datapoints_flattened = [];
    let parameters = "";
    let response_status=201;
    let response_message="Uploaded "+req.body.values.length+" datapoints.";

    for (let row=0; row<req.body.values.length; row++) {
        let cur_parameters = "";
        for (let col=0; col<num_sensors; col++) {
            if (col==0) {
                cur_parameters += "$"+Number(row*num_sensors + col + 1)
            } else {
                cur_parameters += ",$"+Number(row*num_sensors + col + 1)
            }
            datapoints_flattened.push(req.body.values[row][col]);
        }
        if (row==0) {
            parameters = "("+ cur_parameters + ")"
        } else {
            parameters = parameters + ",(" + cur_parameters + ")"
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
