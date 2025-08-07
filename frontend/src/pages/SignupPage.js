// FILE: frontend/src/pages/SignupPage.js

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const SignupPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await fetch('https://health-predictor-backend.onrender.com/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Signup failed');
            }

            setSuccess('Account created successfully! Please log in.');
            setTimeout(() => {
                navigate('/login'); // Redirect to login page after a short delay
            }, 2000);

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-bold text-center text-gray-700">Create an Account</h2>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-600">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-600">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    {error && <p className="text-sm text-red-500">{error}</p>}
                    {success && <p className="text-sm text-green-500">{success}</p>}
                    <button type="submit" className="w-full py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                        Sign Up
                    </button>
                </form>
                <p className="text-sm text-center text-gray-600">
                    Already have an account?{' '}
                    <Link to="/login" className="font-medium text-blue-600 hover:underline">
                        Login
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default SignupPage;