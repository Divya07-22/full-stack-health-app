

import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Main App Component
const App = () => {
    const [formData, setFormData] = useState({
        age: '52',
        gender: 'male',
        bmi: '28.1',
        bloodPressure: '130',
        glucose: '140',
        cholesterol: '240',
        smoking: 'no',
        alcohol: 'no',
        exercise: 'moderate',
    });

    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        setPrediction(null);

        try {
            const backendUrl = 'https://health-predictor-backend.onrender.com/predict';
            
            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            
            const newPrediction = {
                diabetes: { risk: result.diabetes.risk.toFixed(1), recommendations: ['...'] },
                heartDisease: { risk: result.heartDisease.risk.toFixed(1), recommendations: ['...'] },
                cancer: { risk: result.cancer.risk.toFixed(1), recommendations: ['...'] }
            };
            setPrediction(newPrediction);

        } catch (err) {
            setError('Failed to get a prediction. Is the backend server running?');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 font-sans">
            <Header />
            <main className="container mx-auto p-4 md:p-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-1">
                        <PatientDataForm
                            formData={formData}
                            handleChange={handleChange}
                            handleSubmit={handleSubmit}
                            loading={loading}
                            error={error}
                        />
                    </div>
                    <div className="lg:col-span-2">
                        {loading && <LoadingSpinner />}
                        {prediction && !loading && (
                            <PredictionResults prediction={prediction} />
                        )}
                        {!prediction && !loading && <WelcomeMessage />}
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
};

// --- Sub-components ---
const Header = () => (
    <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4 md:px-8">
            <h1 className="text-2xl font-bold text-gray-800">Chronic Disease Predictor</h1>
        </div>
    </header>
);

const PatientDataForm = ({ formData, handleChange, handleSubmit, loading, error }) => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Enter Patient Health Data</h2>
        <form onSubmit={handleSubmit}>
            {/* Form fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputField label="Age" name="age" type="number" value={formData.age} onChange={handleChange} />
                <SelectField label="Gender" name="gender" value={formData.gender} onChange={handleChange} options={[{value: 'male', label: 'Male'}, {value: 'female', 'label': 'Female'}]} />
                <InputField label="BMI" name="bmi" type="number" step="0.1" value={formData.bmi} onChange={handleChange} />
                <InputField label="Systolic Blood Pressure" name="bloodPressure" type="number" value={formData.bloodPressure} onChange={handleChange} />
                <InputField label="Glucose (mg/dL)" name="glucose" type="number" value={formData.glucose} onChange={handleChange} />
                <InputField label="Cholesterol (mg/dL)" name="cholesterol" type="number" value={formData.cholesterol} onChange={handleChange} />
                <SelectField label="Smoking" name="smoking" value={formData.smoking} onChange={handleChange} options={[{value: 'no', label: 'No'}, {value: 'yes', 'label': 'Yes'}]} />
                <SelectField label="Alcohol Consumption" name="alcohol" value={formData.alcohol} onChange={handleChange} options={[{value: 'no', label: 'No'}, {value: 'yes', 'label': 'Yes'}]} />
            </div>
            {error && <p className="text-red-500 text-sm mt-4">{error}</p>}
            <button type="submit" disabled={loading} className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">
                {loading ? 'Analyzing...' : 'Predict All Risks'}
            </button>
        </form>
    </div>
);

const InputField = ({ label, name, type, value, onChange, step }) => (
    <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
        <input name={name} type={type} value={value} onChange={onChange} step={step} className="w-full px-3 py-2 border border-gray-300 rounded-lg" />
    </div>
);

const SelectField = ({ label, name, value, onChange, options }) => (
    <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
        <select name={name} value={value} onChange={onChange} className="w-full px-3 py-2 border border-gray-300 rounded-lg">
            {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
    </div>
);

const LoadingSpinner = () => <div className="flex justify-center items-center h-full"><div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-600"></div></div>;

const WelcomeMessage = () => (
    <div className="bg-white p-8 rounded-lg shadow-lg text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome to the Health Predictor</h2>
        <p className="text-gray-600">Enter patient data on the left to get a real-time risk prediction.</p>
    </div>
);

const PredictionResults = ({ prediction }) => {
    const riskData = [
        { name: 'Diabetes', risk: parseFloat(prediction.diabetes.risk), fill: '#EF4444' },
        { name: 'Heart Disease', risk: parseFloat(prediction.heartDisease.risk), fill: '#3B82F6' },
        { name: 'Cancer', risk: parseFloat(prediction.cancer.risk), fill: '#F59E0B' },
    ];
    return (
        <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Overall Risk Analysis</h2>
            <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={riskData} layout="vertical">
                        <XAxis type="number" domain={[0, 100]} tickFormatter={(tick) => `${tick}%`} />
                        <YAxis type="category" dataKey="name" width={100} />
                        <Tooltip formatter={(value) => `${value}%`} />
                        <Legend />
                        <Bar dataKey="risk" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

const Footer = () => (
    <footer className="bg-white mt-8 py-4">
        <div className="container mx-auto px-4 text-center text-gray-600">
            <p>&copy; {new Date().getFullYear()} Chronic Disease Predictor. For educational purposes only.</p>
        </div>
    </footer>
);

export default App;