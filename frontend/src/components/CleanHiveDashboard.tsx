import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './CleanHiveDashboard.css';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const CleanHiveDashboard = () => {
    const [selectedHiveId, setSelectedHiveId] = useState(1);
    const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
    const [currentTime, setCurrentTime] = useState(new Date());
    const [hiveData, setHiveData] = useState(null);
    const [historicalData, setHistoricalData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [colonyStatus, setColonyStatus] = useState('Established_Colony');
    const [colonyNotes, setColonyNotes] = useState('');
    const [darkMode, setDarkMode] = useState(false);

    // Update time every second
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    // Fetch hive data from synchronized_data table
    useEffect(() => {
        const fetchHiveData = async () => {
            try {
                setLoading(true);
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/latest?hive_id=${selectedHiveId}`);
                const data = await response.json();
                
                if (data.success && data.data) {
                    setHiveData(data.data);
                } else {
                    console.log('No synchronized data available');
                    setHiveData(null);
                }
            } catch (error) {
                console.error('Error fetching hive data:', error);
                setHiveData(null);
            } finally {
                setLoading(false);
            }
        };

        fetchHiveData();
        const interval = setInterval(fetchHiveData, 30000); // Update every 30 seconds
        return () => clearInterval(interval);
    }, [selectedHiveId]);

    // Fetch historical data for trends
    useEffect(() => {
        const fetchHistoricalData = async () => {
            try {
                const hours = selectedTimeRange === '24h' ? 24 : selectedTimeRange === '1w' ? 168 : 720; // 1 month = 720 hours
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/historical?hive_id=${selectedHiveId}&hours=${hours}`);
                const data = await response.json();
                
                if (data.success && data.data) {
                    setHistoricalData(data.data);
                } else {
                    setHistoricalData([]);
                }
            } catch (error) {
                console.error('Error fetching historical data:', error);
                setHistoricalData([]);
            }
        };

        fetchHistoricalData();
    }, [selectedHiveId, selectedTimeRange]);

    const formatTime = (date) => {
        return date.toLocaleTimeString('en-US', { 
            hour12: true, 
            hour: '2-digit', 
            minute: '2-digit',
            second: '2-digit'
        });
    };

    const formatDate = (date) => {
        return date.toLocaleDateString('en-US', { 
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const getPerformanceStatus = () => {
        if (!hiveData) return { status: 'Unknown', score: 0, color: 'gray' };
        
        // Performance calculation based on synchronized data
        const tempDiff = Math.abs((hiveData.sensors?.temperature || 0) - (hiveData.weather?.temperature || 0));
        const humidity = hiveData.sensors?.humidity || 0;
        const sound = hiveData.sensors?.sound || 0;
        const weight = hiveData.sensors?.weight || 0;
        
        let score = 100;
        
        // Temperature differential scoring
        if (tempDiff > 5) score -= 20;
        if (tempDiff > 10) score -= 30;
        
        // Humidity scoring
        if (humidity < 40 || humidity > 80) score -= 15;
        
        // Sound level scoring (normal range 40-60 dB)
        if (sound < 30 || sound > 70) score -= 10;
        
        // Weight scoring (should be reasonable)
        if (weight < 20 || weight > 100) score -= 10;
        
        if (score >= 85) return { status: 'Excellent', score, color: 'green' };
        if (score >= 70) return { status: 'Good', score, color: 'blue' };
        if (score >= 50) return { status: 'Fair', score, color: 'yellow' };
        return { status: 'Poor', score, color: 'red' };
    };

    const performance = getPerformanceStatus();

    // Process data for charts
    const processChartData = () => {
        if (!historicalData || historicalData.length === 0) {
            return {
                temperature: { labels: [], datasets: [] },
                humidity: { labels: [], datasets: [] },
                weight: { labels: [], datasets: [] },
                sound: { labels: [], datasets: [] }
            };
        }

        // Sort data by timestamp
        const sortedData = [...historicalData].sort((a, b) => 
            new Date(a.collection_timestamp) - new Date(b.collection_timestamp)
        );

        const labels = sortedData.map(item => {
            const date = new Date(item.collection_timestamp);
            return date.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
            });
        });

        // Temperature data
        const tempData = {
            labels,
            datasets: [
                {
                    label: 'Internal Temperature',
                    data: sortedData.map(item => item.sensors?.temperature || null),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'External Temperature',
                    data: sortedData.map(item => item.weather?.temperature || null),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        };

        // Humidity data
        const humidityData = {
            labels,
            datasets: [
                {
                    label: 'Internal Humidity',
                    data: sortedData.map(item => item.sensors?.humidity || null),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'External Humidity',
                    data: sortedData.map(item => item.weather?.humidity || null),
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        };

        // Weight data
        const weightData = {
            labels,
            datasets: [
                {
                    label: 'Weight (kg)',
                    data: sortedData.map(item => item.sensors?.weight || null),
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        };

        // Sound data
        const soundData = {
            labels,
            datasets: [
                {
                    label: 'Sound Level (dB)',
                    data: sortedData.map(item => item.sensors?.sound || null),
                    borderColor: '#ec4899',
                    backgroundColor: 'rgba(236, 72, 153, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        };

        return {
            temperature: tempData,
            humidity: humidityData,
            weight: weightData,
            sound: soundData
        };
    };

    const chartData = processChartData();

    // Chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    usePointStyle: true,
                    padding: 20
                }
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#e2e8f0',
                borderWidth: 1
            }
        },
        scales: {
            x: {
                display: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            },
            y: {
                display: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            }
        },
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        }
    };

    if (loading) {
        return (
            <div className={`clean-dashboard ${darkMode ? 'dark' : ''}`}>
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading hive data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className={`clean-dashboard ${darkMode ? 'dark' : ''}`}>
            {/* Header */}
            <header className="dashboard-header">
                <div className="header-left">
                    <h1>🐝 Hive Monitoring Dashboard</h1>
                    <div className="hive-selector">
                        <label htmlFor="hive-select">Hive:</label>
                        <select 
                            id="hive-select" 
                            value={selectedHiveId} 
                            onChange={(e) => setSelectedHiveId(parseInt(e.target.value))}
                        >
                            <option value={1}>Hive #1</option>
                            <option value={2}>Hive #2</option>
                            <option value={3}>Hive #3</option>
                        </select>
                    </div>
                </div>
                <div className="header-right">
                    <div className="datetime">
                        <div className="time">{formatTime(currentTime)}</div>
                        <div className="date">{formatDate(currentTime)}</div>
                    </div>
                    <button 
                        className="dark-mode-toggle"
                        onClick={() => setDarkMode(!darkMode)}
                    >
                        {darkMode ? '☀️' : '🌙'}
                    </button>
                </div>
            </header>

            {/* Real-Time Metrics Cards Grid */}
            <section className="metrics-grid">
                <div className="metrics-row">
                    <div className="metric-card internal">
                        <div className="metric-header">
                            <h3>🌡️ Internal Temperature</h3>
                            <div className="metric-value">
                                {hiveData?.sensors?.temperature ? `${hiveData.sensors.temperature.toFixed(1)}°C` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card internal">
                        <div className="metric-header">
                            <h3>💧 Humidity</h3>
                            <div className="metric-value">
                                {hiveData?.sensors?.humidity ? `${hiveData.sensors.humidity.toFixed(1)}%` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card internal">
                        <div className="metric-header">
                            <h3>🔊 Sound</h3>
                            <div className="metric-value">
                                {hiveData?.sensors?.sound ? `${hiveData.sensors.sound.toFixed(1)} dB` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card internal">
                        <div className="metric-header">
                            <h3>⚖️ Weight</h3>
                            <div className="metric-value">
                                {hiveData?.sensors?.weight ? `${hiveData.sensors.weight.toFixed(1)} kg` : 'N/A'}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="metrics-row">
                    <div className="metric-card external">
                        <div className="metric-header">
                            <h3>🌡️ External Temperature</h3>
                            <div className="metric-value">
                                {hiveData?.weather?.temperature ? `${hiveData.weather.temperature.toFixed(1)}°C` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card external">
                        <div className="metric-header">
                            <h3>💧 External Humidity</h3>
                            <div className="metric-value">
                                {hiveData?.weather?.humidity ? `${hiveData.weather.humidity.toFixed(1)}%` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card external">
                        <div className="metric-header">
                            <h3>💨 Wind Speed</h3>
                            <div className="metric-value">
                                {hiveData?.weather?.wind_speed ? `${hiveData.weather.wind_speed.toFixed(1)} km/h` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card external">
                        <div className="metric-header">
                            <h3>☀️ Light</h3>
                            <div className="metric-value">
                                {hiveData?.weather?.light_intensity ? `${hiveData.weather.light_intensity.toFixed(0)} lux` : 'N/A'}
                            </div>
                        </div>
                    </div>
                    <div className="metric-card external">
                        <div className="metric-header">
                            <h3>🌧️ Rain</h3>
                            <div className="metric-value">
                                {hiveData?.weather?.rainfall ? `${hiveData.weather.rainfall.toFixed(1)} mm/h` : '0.0 mm/h'}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Trends Section */}
            <section className="trends-section">
                <div className="trends-header">
                    <h2>📈 Trends</h2>
                    <div className="time-range-selector">
                        <button 
                            className={selectedTimeRange === '24h' ? 'active' : ''}
                            onClick={() => setSelectedTimeRange('24h')}
                        >
                            24h
                        </button>
                        <button 
                            className={selectedTimeRange === '1w' ? 'active' : ''}
                            onClick={() => setSelectedTimeRange('1w')}
                        >
                            1w
                        </button>
                        <button 
                            className={selectedTimeRange === '1m' ? 'active' : ''}
                            onClick={() => setSelectedTimeRange('1m')}
                        >
                            1m
                        </button>
                    </div>
                </div>
                <div className="charts-grid">
                    <div className="chart-container">
                        <h4>🌡️ Temperature Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Internal: {hiveData?.sensors?.temperature?.toFixed(1) || 'N/A'}°C</span>
                                <span>External: {hiveData?.weather?.temperature?.toFixed(1) || 'N/A'}°C</span>
                            </div>
                            <div className="chart-wrapper">
                                <Line data={chartData.temperature} options={chartOptions} />
                            </div>
                        </div>
                    </div>
                    <div className="chart-container">
                        <h4>💧 Humidity Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Internal: {hiveData?.sensors?.humidity?.toFixed(1) || 'N/A'}%</span>
                                <span>External: {hiveData?.weather?.humidity?.toFixed(1) || 'N/A'}%</span>
                            </div>
                            <div className="chart-wrapper">
                                <Line data={chartData.humidity} options={chartOptions} />
                            </div>
                        </div>
                    </div>
                    <div className="chart-container">
                        <h4>⚖️ Weight Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Current: {hiveData?.sensors?.weight?.toFixed(1) || 'N/A'} kg</span>
                                <span>Data Points: {historicalData.length}</span>
                            </div>
                            <div className="chart-wrapper">
                                <Line data={chartData.weight} options={chartOptions} />
                            </div>
                        </div>
                    </div>
                    <div className="chart-container">
                        <h4>🔊 Sound Level Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Current: {hiveData?.sensors?.sound?.toFixed(1) || 'N/A'} dB</span>
                                <span>Data Points: {historicalData.length}</span>
                            </div>
                            <div className="chart-wrapper">
                                <Line data={chartData.sound} options={chartOptions} />
                            </div>
                        </div>
                    </div>
                </div>
            </section>


            {/* Predictive Hive Performance Card */}
            <section className="performance-section">
                <div className="performance-card">
                    <div className="performance-header">
                        <h2>🔮 Predictive Hive Performance</h2>
                    </div>
                    <div className="performance-content">
                        <div className="performance-score">
                            <div className="score-circle" style={{ borderColor: performance.color }}>
                                <div className="score-value">{performance.score}%</div>
                                <div className="score-label">Performance</div>
                            </div>
                            <div className="performance-details">
                                <div className="status-badge" style={{ backgroundColor: performance.color }}>
                                    {performance.status}
                                </div>
                                <div className="forecast">📈 Forecast: upward trend</div>
                                <div className="alert">⚠️ Alert: Advisory – Monitor Hive</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Colony Status Input */}
            <section className="colony-status-section">
                <h2>🏛️ Colony Status</h2>
                <div className="colony-controls">
                    <div className="status-input">
                        <label htmlFor="colony-status">Status:</label>
                        <select 
                            id="colony-status"
                            value={colonyStatus}
                            onChange={(e) => setColonyStatus(e.target.value)}
                        >
                            <option value="New_Colony">New Colony</option>
                            <option value="Established_Colony">Established Colony</option>
                            <option value="Preparing_to_Swarm">Preparing to Swarm</option>
                        </select>
                    </div>
                    <div className="notes-input">
                        <label htmlFor="colony-notes">Notes:</label>
                        <textarea 
                            id="colony-notes"
                            value={colonyNotes}
                            onChange={(e) => setColonyNotes(e.target.value)}
                            placeholder="Add notes about colony status..."
                            rows="3"
                        />
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="dashboard-footer">
                <div className="footer-left">
                    <button className="export-btn">📊 Export Data</button>
                </div>
                <div className="footer-right">
                    <button 
                        className="dark-mode-toggle"
                        onClick={() => setDarkMode(!darkMode)}
                    >
                        {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
                    </button>
                </div>
            </footer>
        </div>
    );
};

export default CleanHiveDashboard;
