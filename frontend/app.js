const { useState } = React;

function MobilePredictionForm() {
    const [formData, setFormData] = useState({
        "Mobile Weight": "",
        "RAM": "",
        "Front Camera": "",
        "Back Camera": "",
        "Processor": "",
        "Battery Capacity": "",
        "Screen Size": "",
        "Launched Year": ""
    });
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setPrediction(null);

        try {
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (response.ok) {
                setPrediction(data.prediction);
            } else {
                setError(data.error || 'An error occurred while making the prediction');
            }
        } catch (err) {
            setError('Failed to connect to the prediction server');
        }
    };

    return (
        <div className="container">
            <h1>Mobile Price Prediction</h1>
            <form onSubmit={handleSubmit}>
                <div className="row">
                    <div className="col-md-6">
                        <div className="form-group">
                            <label>Mobile Weight (g)</label>
                            <input
                                type="number"
                                className="form-control"
                                name="Mobile Weight"
                                value={formData["Mobile Weight"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>RAM (GB)</label>
                            <input
                                type="number"
                                className="form-control"
                                name="RAM"
                                value={formData["RAM"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Front Camera (MP)</label>
                            <input
                                type="number"
                                className="form-control"
                                name="Front Camera"
                                value={formData["Front Camera"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Back Camera (MP)</label>
                            <input
                                type="number"
                                className="form-control"
                                name="Back Camera"
                                value={formData["Back Camera"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <div className="col-md-6">
                        <div className="form-group">
                            <label>Processor (GHz)</label>
                            <input
                                type="number"
                                step="0.1"
                                className="form-control"
                                name="Processor"
                                value={formData["Processor"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Battery Capacity (mAh)</label>
                            <input
                                type="number"
                                className="form-control"
                                name="Battery Capacity"
                                value={formData["Battery Capacity"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Screen Size (inches)</label>
                            <input
                                type="number"
                                step="0.1"
                                className="form-control"
                                name="Screen Size"
                                value={formData["Screen Size"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Launched Year</label>
                            <input
                                type="number"
                                className="form-control"
                                name="Launched Year"
                                value={formData["Launched Year"]}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                </div>
                <button type="submit" className="btn btn-primary">Predict Price</button>
            </form>

            {error && (
                <div className="alert alert-danger mt-3" role="alert">
                    {error}
                </div>
            )}

            {prediction && (
                <div className="prediction-result">
                    <h3>Predicted Price: ₹{prediction[0].toFixed(2)}</h3>
                </div>
            )}
        </div>
    );
}

ReactDOM.render(<MobilePredictionForm />, document.getElementById('root')); 