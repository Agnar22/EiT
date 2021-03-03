var express = require('express');
var app = express();
const accessTokenSecret = 'youraccesstokensecret';

const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
app.use(bodyParser.json());

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
];


app.get('/', function (req, res) {
   res.send('Hello World');
});


const { Pool } = require('pg')

//const { Client } = require('pg');
//client = new Client({
//    host: 'localhost',
//    user: 'node_eit',
//    password: 'node_eit_jernbane_pwd',
//    database: 'postgres'
//});

//var connection = postgres.createConnection({
//    host: 'localhost',
//    user: 'node_eit',
//    password: 'node_eit_jernbane_pwd',
//    database: 'postgres',
//});
//


//connection.connect();

app.post('/data', (req, res) => {
    fs = require('fs');
    console.log(req.body);
    console.log(req.body.value);

    const text = 'INSERT INTO eit.test(ts, sensor_value) VALUES (current_timestamp, 2)';
    const values = [];

    const pool = new Pool({
      user: 'node_eit',
      host: 'localhost',
      database: 'postgres',
      password: 'node_eit_jernbane_pwd',
      port: 5432,
    });

    //pool.query('SELECT * FROM eit.test', (err, res) => {
    //  console.log(err, res) 
    //  pool.end() 
    //});
    pool.query('INSERT INTO eit.test(ts, sensor_value) VALUES (current_timestamp, $1)', [req.body.value], (err, res) => {
      console.log(err, res) 
      pool.end() 
    });
    //fs.appendFile('helloworld.txt', req.body.username + "\n", function (err) {
    //  if (err) return console.log(err);
    //    console.log('Hello World > helloworld.txt');
    //});
    //connection.query('INSERT INTO eit.test(ts, sensor_value) VALUES (current_timestamp, ?)', fs.body.value, function (err, res) {if (err) throw err;});
    //console.log("connecting");
    //client.connect(err => {
    //  if (err) {
    //      console.error('connection error', err.stack);
    //  } else {
    //      console.log('connected');
    //}
    //});
    //client.
    //console.log("quering");
    //client.query(text).then(res => {console.log(res.rows[0])}).catch(e => console.error(e.stack));


    //console.log("disconnecting");
    //client.end(err => {
    //  console.log('client has disconnected');
    //    if (err) {
    //        console.log('error during disconnection', err.stack);
    //          }
    //          });

    //console.log("posted\n");
    res.sendStatus(201);
});

app.post('/login', (req, res) => {
    // Read username and password from request body
    const { username, password } = req.body;

    console.log(req.body);
    console.log(username);
    console.log(password);

    // Filter user from the users array by username and password
    const user = users.find(u => { return u.username === username && u.password === password });
    console.log(user);

    if (user) {
        // Generate an access token
        const accessToken = jwt.sign({ username: user.username,  role: user.role }, accessTokenSecret);

        res.json({accessToken});
    } else {
        res.send('Username or password incorrect');
    }
});

var server = app.listen(4013, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("Example app listening at http://%s:%s", host, port)
})
