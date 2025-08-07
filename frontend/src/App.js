// FILE: frontend/src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import Predictor from './components/Predictor';

const App = () => {
    const token = localStorage.getItem('token');

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login'; // Redirect to login and refresh
    };

    return (
        <Router>
            <div className="min-h-screen bg-gray-100 font-sans">
                <Header isLoggedIn={!!token} onLogout={handleLogout} />
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/signup" element={<SignupPage />} />
                    <Route 
                        path="/predictor"
                        element={token ? <Predictor /> : <Navigate to="/login" />} 
                    />
                    <Route 
                        path="/"
                        element={<Navigate to={token ? "/predictor" : "/login"} />}
                    />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
};

const Header = ({ isLoggedIn, onLogout }) => (
    <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4 md:px-8 flex justify-between items-center">
            <div className="flex items-center">
                <svg className="w-10 h-10 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <h1 className="text-2xl font-bold text-gray-800">Chronic Disease Predictor</h1>
            </div>
            <nav>
                {isLoggedIn ? (
                    <button onClick={onLogout} className="px-4 py-2 font-semibold text-white bg-red-500 rounded-lg hover:bg-red-600">
                        Logout
                    </button>
                ) : (
                    <div>
                        <Link to="/login" className="px-4 py-2 font-semibold text-gray-700 rounded-lg hover:bg-gray-200">
                            Login
                        </Link>
                        <Link to="/signup" className="px-4 py-2 ml-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                            Sign Up
                        </Link>
                    </div>
                )}
            </nav>
        </div>
    </header>
);

const Footer = () => (
    <footer className="bg-white mt-8 py-4">
        <div className="container mx-auto px-4 text-center text-gray-600">
            <p>&copy; {new Date().getFullYear()} Chronic Disease Predictor. For educational purposes only.</p>
        </div>
    </footer>
);

export default App;