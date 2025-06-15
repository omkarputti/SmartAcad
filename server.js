const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/byte_battle', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// User schema
const userSchema = new mongoose.Schema({
    email: String,
    name: String,
    password: String,
    role: String,
});
const User = mongoose.model('User', userSchema);

// Login endpoint
app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user || user.password !== password) {
        return res.status(401).json({ message: 'Invalid credentials.' });
    }
    res.json({ message: 'Login successful!', user, token: 'dummy-token' });
});

app.listen(5000, () => {
    console.log('Server running on http://localhost:5000');
});