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

    // This function calls the comprehensive backend
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (!formData.age || !formData.bmi || !formData.bloodPressure || !formData.glucose || !formData.cholesterol) {
            setError('Please fill in all the required fields.');
            return;
        }

        setLoading(true);
        setPrediction(null);

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            
            const newPrediction = {
                diabetes: {
                    risk: result.diabetes.risk.toFixed(1),
                    recommendations: [
                        'Monitor your blood sugar levels regularly.',
                        'Follow a balanced diet with controlled carbohydrate intake.',
                        'Engage in regular physical activity for at least 30 minutes a day.',
                    ]
                },
                heartDisease: {
                    risk: result.heartDisease.risk.toFixed(1),
                    recommendations: [
                        'Adopt a heart-healthy diet low in sodium and saturated fats.',
                        'Incorporate aerobic exercises like brisk walking or swimming.',
                        'Manage stress through relaxation techniques like meditation or yoga.',
                    ]
                },
                cancer: {
                    risk: result.cancer.risk.toFixed(1),
                    recommendations: [
                        'If you smoke, seek help to quit.',
                        'Limit alcohol intake and maintain a healthy weight.',
                        'Eat a diet rich in fruits, vegetables, and whole grains.',
                    ]
                }
            };

            setPrediction(newPrediction);

        } catch (err) {
            setError('Failed to get a prediction. Is the backend server running?');
            console.error("Fetch error:", err);
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

// Header Component
const Header = () => (
    <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4 md:px-8 flex justify-between items-center">
            <div className="flex items-center">
                 <svg className="w-10 h-10 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <h1 className="text-2xl font-bold text-gray-800">Chronic Disease Predictor</h1>
            </div>
        </div>
    </header>
);

// Patient Data Form Component
const PatientDataForm = ({ formData, handleChange, handleSubmit, loading, error }) => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Enter Patient Health Data</h2>
        <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputField label="Age" name="age" type="number" value={formData.age} onChange={handleChange} required />
                <SelectField label="Gender" name="gender" value={formData.gender} onChange={handleChange} options={[{value: 'male', label: 'Male'}, {value: 'female', label: 'Female'}]} />
                <InputField label="BMI" name="bmi" type="number" step="0.1" value={formData.bmi} onChange={handleChange} required />
                <InputField label="Systolic Blood Pressure" name="bloodPressure" type="number" value={formData.bloodPressure} onChange={handleChange} required />
                <InputField label="Glucose (mg/dL)" name="glucose" type="number" value={formData.glucose} onChange={handleChange} required />
                <InputField label="Cholesterol (mg/dL)" name="cholesterol" type="number" value={formData.cholesterol} onChange={handleChange} required />
                <SelectField label="Smoking" name="smoking" value={formData.smoking} onChange={handleChange} options={[{value: 'no', label: 'No'}, {value: 'yes', label: 'Yes'}]} />
                <SelectField label="Alcohol Consumption" name="alcohol" value={formData.alcohol} onChange={handleChange} options={[{value: 'no', label: 'No'}, {value: 'yes', label: 'Yes'}]} />
            </div>
             <div className="mt-4">
                <SelectField label="Weekly Exercise" name="exercise" value={formData.exercise} onChange={handleChange} options={[{value: 'none', label: 'None'}, {value: 'light', label: 'Light'}, {value: 'moderate', label: 'Moderate'}, {value: 'heavy', label: 'Heavy'}]} />
            </div>
            {error && <p className="text-red-500 text-sm mt-4">{error}</p>}
            <button type="submit" disabled={loading} className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 disabled:bg-blue-300">
                {loading ? 'Analyzing...' : 'Predict All Risks'}
            </button>
        </form>
    </div>
);

const InputField = ({ label, name, type, value, onChange, required, step }) => (
    <div>
        <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
        <input id={name} name={name} type={type} value={value} onChange={onChange} required={required} step={step} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
    </div>
);

const SelectField = ({ label, name, value, onChange, options }) => (
    <div>
        <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
        <select id={name} name={name} value={value} onChange={onChange} className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            {options.map(option => (<option key={option.value} value={option.value}>{option.label}</option>))}
        </select>
    </div>
);

const LoadingSpinner = () => (
    <div className="flex justify-center items-center h-full"><div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-600"></div></div>
);

const WelcomeMessage = () => (
    <div className="bg-white p-8 rounded-lg shadow-lg text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome to the Health Predictor</h2>
        <p className="text-gray-600">Enter patient data on the left to get a real-time risk prediction from our AI models.</p>
    </div>
);

const PredictionResults = ({ prediction }) => {
    const riskData = [
        { name: 'Diabetes', risk: parseFloat(prediction.diabetes.risk), fill: '#EF4444' },
        { name: 'Heart Disease', risk: parseFloat(prediction.heartDisease.risk), fill: '#3B82F6' },
        { name: 'Cancer', risk: parseFloat(prediction.cancer.risk), fill: '#F59E0B' },
    ];

    return (
        <div className="space-y-8">
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold mb-4 text-gray-700">Overall Risk Analysis</h2>
                <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={riskData} layout="vertical" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <XAxis type="number" domain={[0, 100]} tickFormatter={(tick) => `${tick}%`} />
                            <YAxis type="category" dataKey="name" width={100} />
                            <Tooltip formatter={(value) => `${value}%`} />
                            <Legend />
                            <Bar dataKey="risk" fill="#8884d8" background={{ fill: '#eee' }} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
            <DiseaseRiskCard title="Diabetes" data={prediction.diabetes} color="red" />
            <DiseaseRiskCard title="Heart Disease" data={prediction.heartDisease} color="blue" />
            <DiseaseRiskCard title="Cancer" data={prediction.cancer} color="amber" />
        </div>
    );
};

const DiseaseRiskCard = ({ title, data, color }) => {
    const COLORS = {
        red: { bg: 'bg-red-50', border: 'border-red-500', text: 'text-red-600' },
        blue: { bg: 'bg-blue-50', border: 'border-blue-500', text: 'text-blue-600' },
        amber: { bg: 'bg-amber-50', border: 'border-amber-500', text: 'text-amber-600' },
    };
    const selectedColor = COLORS[color];

    return (
        <div className={`${selectedColor.bg} p-6 rounded-lg shadow-lg border-l-4 ${selectedColor.border}`}>
            <div className="flex justify-between items-center">
                <h3 className={`text-xl font-semibold ${selectedColor.text}`}>{title} Risk</h3>
                <div className="text-3xl font-bold text-gray-800">{data.risk}%</div>
            </div>
            <div className="mt-4">
                <h4 className="font-semibold text-gray-700 mb-2">Personalized Recommendations:</h4>
                <ul className="list-disc list-inside space-y-1 text-gray-600">
                    {data.recommendations.map((rec, index) => ( <li key={index}>{rec}</li> ))}
                </ul>
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
