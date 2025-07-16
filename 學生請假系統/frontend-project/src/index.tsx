import React from 'react';
import ReactDOM from 'react-dom';
import HomePage from './components/HomePage';
import './styles/HomePage.css';

const App = () => {
    return <HomePage />;
};

ReactDOM.render(<App />, document.getElementById('root'));