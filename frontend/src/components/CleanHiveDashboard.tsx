// CleanHiveDashboard.tsx - COMPLETE FILE
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
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
import './CleanHiveDashboard.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

interface PerformancePrediction {
    predicted_level: number;
    interpretation: string;
    confidence: number;
    risk_assessment: string;
    all_probabilities: { [level: string]: number };
    timestamp: string;
}

interface HiveData {
    id: number;
    collection_timestamp: string;
    hive_id: number;
    weather: {
        temperature: number | null;
        humidity: number | null;
        wind_speed: number | null;
        light_intensity: number | null;
        rainfall: number | null;
    };
    sensors: {
        temperature: number | null;
        humidity: number | null;
        sound: number | null;
        weight: number | null;
    };
    metadata: any;
}

interface HistoricalPerformance {
    predicted_level: number;
    interpretation: string;
    confidence: number;
    risk_assessment: string;
    all_probabilities: { [level: string]: number };
    timestamp: string;
    collection_timestamp: string;
}

const GaugeChart = ({ value, min, max, unit, label, color, icon }: {
    value: number | null;
    min: number;
    max: number;
    unit: string;
    label: string;
    color: string;
    icon: string;
}) => {
    const percentage = value !== null ? Math.min(Math.max(((value - min) / (max - min)) * 100, 0), 100) : 0;
    const rotation = (percentage / 100) * 180 - 90;

    return (
        <div className="gauge-card">
            <div className="gauge-header">
                <span className="gauge-icon">{icon}</span>
                <h3>{label}</h3>
            </div>
            <div className="gauge-container">
                <svg viewBox="0 0 200 120" className="gauge-svg">
                    <path d="M 30 100 A 70 70 0 0 1 170 100" fill="none" stroke="#e2e8f0" strokeWidth="12" strokeLinecap="round" />
                    <path d="M 30 100 A 70 70 0 0 1 170 100" fill="none" stroke={color} strokeWidth="12" strokeLinecap="round" strokeDasharray={`${(percentage / 100) * 220} 220`} className="gauge-arc" />
                    <g transform={`rotate(${rotation} 100 100)`}>
                        <line x1="100" y1="100" x2="100" y2="40" stroke={color} strokeWidth="3" strokeLinecap="round" />
                        <circle cx="100" cy="100" r="6" fill={color} />
                    </g>
                    <circle cx="100" cy="100" r="8" fill="white" stroke={color} strokeWidth="2" />
                </svg>
                <div className="gauge-value-container">
                    <div className="gauge-value" style={{ color }}>{value !== null ? value.toFixed(1) : 'N/A'}</div>
                    <div className="gauge-unit">{unit}</div>
                </div>
            </div>
            <div className="gauge-range">
                <span className="range-min">{min}{unit}</span>
                <span className="range-max">{max}{unit}</span>
            </div>
        </div>
    );
};

const CleanHiveDashboard = () => {
    const [selectedHiveId, setSelectedHiveId] = useState(1);
    const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
    const [currentTime, setCurrentTime] = useState(new Date());
    const [hiveData, setHiveData] = useState<HiveData | null>(null);
    const [historicalData, setHistoricalData] = useState<HiveData[]>([]);
    const [loading, setLoading] = useState(true);
    const [darkMode, setDarkMode] = useState(false);
    const [performancePrediction, setPerformancePrediction] = useState<PerformancePrediction | null>(null);
    const [performanceLoading, setPerformanceLoading] = useState(true);
    const [historicalPerformance, setHistoricalPerformance] = useState<HistoricalPerformance[]>([]);
    const [historicalPerfLoading, setHistoricalPerfLoading] = useState(true);

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        const fetchHiveData = async () => {
            try {
                setLoading(true);
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/latest?hive_id=${selectedHiveId}`);
                const data = await response.json();
                setHiveData(data.success && data.data ? data.data : null);
            } catch (error) {
                setHiveData(null);
            } finally {
                setLoading(false);
            }
        };
        fetchHiveData();
        const interval = setInterval(fetchHiveData, 30000);
        return () => clearInterval(interval);
    }, [selectedHiveId]);

    useEffect(() => {
        const fetchPerformancePrediction = async () => {
            try {
                setPerformanceLoading(true);
                const response = await fetch(`http://127.0.0.1:5000/api/performance/predict?hive_id=${selectedHiveId}`);
                const data = await response.json();
                setPerformancePrediction(data.success && data.prediction ? data.prediction : null);
            } catch (error) {
                setPerformancePrediction(null);
            } finally {
                setPerformanceLoading(false);
            }
        };
        fetchPerformancePrediction();
        const interval = setInterval(fetchPerformancePrediction, 30000);
        return () => clearInterval(interval);
    }, [selectedHiveId]);

    useEffect(() => {
        const fetchHistoricalData = async () => {
            try {
                const hours = selectedTimeRange === '24h' ? 24 : selectedTimeRange === '1w' ? 168 : 720;
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/historical?hive_id=${selectedHiveId}&hours=${hours}`);
                const data = await response.json();
                setHistoricalData(data.success && data.data ? data.data : []);
            } catch (error) {
                setHistoricalData([]);
            }
        };
        fetchHistoricalData();
    }, [selectedHiveId, selectedTimeRange]);

    useEffect(() => {
        const fetchHistoricalPerformance = async () => {
            try {
                setHistoricalPerfLoading(true);
                const hours = selectedTimeRange === '24h' ? 24 : selectedTimeRange === '1w' ? 168 : 720;
                const response = await fetch(`http://127.0.0.1:5000/api/performance/history?hive_id=${selectedHiveId}&hours=${hours}`);
                const data = await response.json();
                setHistoricalPerformance(data.success && data.history ? data.history : []);
            } catch (error) {
                setHistoricalPerformance([]);
            } finally {
                setHistoricalPerfLoading(false);
            }
        };
        fetchHistoricalPerformance();
    }, [selectedHiveId, selectedTimeRange]);

    const formatTime = (date: Date) => date.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const formatDate = (date: Date) => date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    const getPerformanceStatus = () => {
        if (performanceLoading) return { predicted_level: '-', interpretation: 'Loading...', confidence: '-', risk_assessment: '', all_probabilities: {}, color: 'gray', timestamp: '' };
        if (!performancePrediction) return { predicted_level: '-', interpretation: 'Unknown', confidence: '-', risk_assessment: '', all_probabilities: {}, color: 'gray', timestamp: '' };
        return {
            ...performancePrediction,
            color: performancePrediction.predicted_level === 1 ? '#22c55e' : performancePrediction.predicted_level === 2 ? '#3b82f6' : performancePrediction.predicted_level === 3 ? '#facc15' : performancePrediction.predicted_level === 4 ? '#f59e42' : '#ef4444'
        };
    };
    const performance = getPerformanceStatus();

    const processChartData = () => {
        if (!historicalData || historicalData.length === 0) return { temperature: { labels: [], datasets: [] }, humidity: { labels: [], datasets: [] }, weight: { labels: [], datasets: [] }, sound: { labels: [], datasets: [] } };
        const sortedData = [...historicalData].sort((a, b) => new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime());
        const labels = sortedData.map(item => new Date(item.collection_timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }));
        return {
            temperature: { labels, datasets: [{ label: 'Internal Temperature', data: sortedData.map(item => item.sensors?.temperature || null), borderColor: '#ef4444', backgroundColor: 'rgba(239, 68, 68, 0.1)', fill: true, tension: 0.4 }, { label: 'External Temperature', data: sortedData.map(item => item.weather?.temperature || null), borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: true, tension: 0.4 }] },
            humidity: { labels, datasets: [{ label: 'Internal Humidity', data: sortedData.map(item => item.sensors?.humidity || null), borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.4 }, { label: 'External Humidity', data: sortedData.map(item => item.weather?.humidity || null), borderColor: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.1)', fill: true, tension: 0.4 }] },
            weight: { labels, datasets: [{ label: 'Weight (kg)', data: sortedData.map(item => item.sensors?.weight || null), borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)', fill: true, tension: 0.4 }] },
            sound: { labels, datasets: [{ label: 'Sound Level (dB)', data: sortedData.map(item => item.sensors?.sound || null), borderColor: '#ec4899', backgroundColor: 'rgba(236, 72, 153, 0.1)', fill: true, tension: 0.4 }] }
        };
    };
    const chartData = processChartData();

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' as const, labels: { usePointStyle: true, padding: 20 } }, tooltip: { mode: 'index' as const, intersect: false, backgroundColor: 'rgba(0, 0, 0, 0.8)', titleColor: '#fff', bodyColor: '#fff', borderColor: '#e2e8f0', borderWidth: 1 } },
        scales: { x: { display: true, grid: { color: 'rgba(0, 0, 0, 0.1)' } }, y: { display: true, grid: { color: 'rgba(0, 0, 0, 0.1)' } } },
        interaction: { mode: 'nearest' as const, axis: 'x' as const, intersect: false }
    };

    const getPerformanceChartData = () => {
        if (!historicalPerformance || historicalPerformance.length === 0) return { labels: [], datasets: [] };
        const sorted = [...historicalPerformance].sort((a, b) => new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime());
        return {
            labels: sorted.map(item => new Date(item.collection_timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })),
            datasets: [{ label: 'Performance Level', data: sorted.map(item => item.predicted_level), borderColor: '#6366f1', backgroundColor: 'rgba(99,102,241,0.1)', fill: true, tension: 0.4, pointRadius: 2 }]
        };
    };
    const performanceChartData = getPerformanceChartData();

    const performanceChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { mode: 'index' as const, intersect: false, backgroundColor: 'rgba(0,0,0,0.8)', titleColor: '#fff', bodyColor: '#fff', borderColor: '#e2e8f0', borderWidth: 1 } },
        scales: { x: { display: true, grid: { color: 'rgba(0,0,0,0.07)' } }, y: { display: true, grid: { color: 'rgba(0,0,0,0.07)' }, min: 1, max: 5, ticks: { stepSize: 1, callback: function(tickValue: string | number) { const value = typeof tickValue === 'number' ? tickValue : parseInt(tickValue as string, 10); return value === 1 ? 'Excellent' : value === 2 ? 'Good' : value === 3 ? 'Moderate' : value === 4 ? 'Poor' : value === 5 ? 'Critical' : value; } } } },
        interaction: { mode: 'nearest' as const, axis: 'x' as const, intersect: false }
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
            <header className="dashboard-header">
                <div className="header-left">
                    <h1>🐝 Hive Monitoring Dashboard</h1>
                    <div className="hive-selector">
                        <label htmlFor="hive-select">Hive:</label>
                        <select id="hive-select" value={selectedHiveId} onChange={(e) => setSelectedHiveId(parseInt(e.target.value))}>
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
                    <button className="dark-mode-toggle" onClick={() => setDarkMode(!darkMode)}>{darkMode ? '☀️' : '🌙'}</button>
                </div>
            </header>

            <section className="sensors-section">
                <h2 className="section-title">📊 Live Sensor Readings</h2>
                <div className="gauges-grid">
                    <GaugeChart value={hiveData?.sensors?.temperature || null} min={0} max={50} unit="°C" label="Internal Temperature" color="#ef4444" icon="🌡️" />
                    <GaugeChart value={hiveData?.sensors?.humidity || null} min={0} max={100} unit="%" label="Internal Humidity" color="#10b981" icon="💧" />
                    <GaugeChart value={hiveData?.sensors?.sound || null} min={0} max={100} unit="dB" label="Sound Level" color="#8b5cf6" icon="🔊" />
                </div>
            </section>

            <section className="weather-section">
                <div className="weather-card">
                    <div className="weather-header">
                        <div className="weather-title">
                            <span className="weather-icon">🌤️</span>
                            <h2>Environmental Conditions</h2>
                        </div>
                        <div className="weather-status">
                            <span className="status-indicator"></span>
                            <span className="status-text">Live Data</span>
                        </div>
                    </div>
                    <div className="weather-grid">
                        <div className="weather-item temperature">
                            <div className="weather-item-icon">🌡️</div>
                            <div className="weather-item-content">
                                <div className="weather-item-label">Temperature</div>
                                <div className="weather-item-value">{hiveData?.weather?.temperature ? `${hiveData.weather.temperature.toFixed(1)}°C` : 'N/A'}</div>
                                <div className="weather-item-description">External ambient</div>
                            </div>
                        </div>
                        <div className="weather-item humidity">
                            <div className="weather-item-icon">💧</div>
                            <div className="weather-item-content">
                                <div className="weather-item-label">Humidity</div>
                                <div className="weather-item-value">{hiveData?.weather?.humidity ? `${hiveData.weather.humidity.toFixed(1)}%` : 'N/A'}</div>
                                <div className="weather-item-description">Relative humidity</div>
                            </div>
                        </div>
                        <div className="weather-item wind">
                            <div className="weather-item-icon">💨</div>
                            <div className="weather-item-content">
                                <div className="weather-item-label">Wind Speed</div>
                                <div className="weather-item-value">{hiveData?.weather?.wind_speed ? `${hiveData.weather.wind_speed.toFixed(1)} km/h` : 'N/A'}</div>
                                <div className="weather-item-description">Current wind</div>
                            </div>
                        </div>
                        <div className="weather-item light">
                            <div className="weather-item-icon">☀️</div>
                            <div className="weather-item-content">
                                <div className="weather-item-label">Light Intensity</div>
                                <div className="weather-item-value">{hiveData?.weather?.light_intensity ? `${hiveData.weather.light_intensity.toFixed(0)} lux` : 'N/A'}</div>
                                <div className="weather-item-description">Solar radiation</div>
                            </div>
                        </div>
                        <div className="weather-item rain">
                            <div className="weather-item-icon">🌧️</div>
                            <div className="weather-item-content">
                                <div className="weather-item-label">Rainfall</div>
                                <div className="weather-item-value">{hiveData?.weather?.rainfall ? `${hiveData.weather.rainfall.toFixed(1)} mm/h` : '0.0 mm/h'}</div>
                                <div className="weather-item-description">Precipitation rate</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="trends-section">
                <div className="trends-header">
                    <h2>📈 Trends</h2>
                    <div className="time-range-selector">
                        <button className={selectedTimeRange === '24h' ? 'active' : ''} onClick={() => setSelectedTimeRange('24h')}>24h</button>
                        <button className={selectedTimeRange === '1w' ? 'active' : ''} onClick={() => setSelectedTimeRange('1w')}>1w</button>
                        <button className={selectedTimeRange === '1m' ? 'active' : ''} onClick={() => setSelectedTimeRange('1m')}>1m</button>
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
                            <div className="chart-wrapper"><Line data={chartData.temperature} options={chartOptions} /></div>
                        </div>
                    </div>
                    <div className="chart-container">
                        <h4>💧 Humidity Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Internal: {hiveData?.sensors?.humidity?.toFixed(1) || 'N/A'}%</span>
                                <span>External: {hiveData?.weather?.humidity?.toFixed(1) || 'N/A'}%</span>
                            </div>
                            <div className="chart-wrapper"><Line data={chartData.humidity} options={chartOptions} /></div>
                        </div>
                    </div>
                    <div className="chart-container">
                        <h4>🔊 Sound Level Trend</h4>
                        <div className="chart-data">
                            <div className="trend-info">
                                <span>Current: {hiveData?.sensors?.sound?.toFixed(1) || 'N/A'} dB</span>
                                <span>Data Points: {historicalData.length}</span>
                            </div>
                            <div className="chart-wrapper"><Line data={chartData.sound} options={chartOptions} /></div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="performance-section">
                <div className="performance-card" style={{ background: 'linear-gradient(135deg, #f0fdfa 0%, #e0e7ff 100%)', borderRadius: 20, boxShadow: '0 4px 24px 0 rgba(59,130,246,0.10)', padding: '2rem 2.5rem', margin: '1.5rem 0', maxWidth: 900, marginLeft: 'auto', marginRight: 'auto', border: `2.5px solid ${performance.color}`, display: 'flex', flexDirection: 'row', alignItems: 'stretch', gap: 32 }}>
                    <div style={{ flex: 1, minWidth: 320 }}>
                        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 18 }}>
                            <span style={{ fontSize: 32, marginRight: 12 }}>🔮</span>
                            <h2 style={{ fontWeight: 700, fontSize: 26, margin: 0, color: '#1e293b', letterSpacing: 0.5 }}>Predictive Hive Performance</h2>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <div style={{ border: `5px solid ${performance.color}`, borderRadius: '50%', width: 120, height: 120, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#fff', marginBottom: 18, boxShadow: '0 2px 12px 0 rgba(59,130,246,0.08)' }}>
                                <div style={{ fontSize: 38, fontWeight: 800, color: performance.color }}>{performance.predicted_level}</div>
                                <div style={{ fontSize: 15, color: '#64748b', fontWeight: 600, marginTop: 2 }}>Performance Level</div>
                            </div>
                            <div style={{ fontSize: 18, fontWeight: 700, color: '#0f172a', marginBottom: 8, textAlign: 'center' }}>{performance.interpretation}</div>
                            <div style={{ width: '100%', marginTop: 8 }}>
                                <div style={{ background: performance.color, color: '#fff', fontWeight: 700, borderRadius: 8, padding: '6px 16px', display: 'inline-block', fontSize: 15, marginBottom: 8 }}>{performance.risk_assessment}</div>
                                <div style={{ fontSize: 15, color: '#334155', marginBottom: 2 }}>Confidence: <b>{typeof performance.confidence === 'number' ? (performance.confidence * 100).toFixed(1) : performance.confidence}%</b></div>
                                <div style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>Prediction Time: {performance.timestamp ? new Date(performance.timestamp).toLocaleString() : '-'}</div>
                                <div style={{ fontSize: 14, color: '#334155', marginBottom: 0 }}>
                                    <b>Probabilities:</b>
                                    <ul style={{ margin: 0, paddingLeft: 18 }}>
                                        {performance.all_probabilities && Object.entries(performance.all_probabilities).map(([level, prob]) => (
                                            <li key={level}>{level}: {(prob as number * 100).toFixed(2)}%</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style={{ flex: 1, minWidth: 320, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                        <h4 style={{ marginBottom: 12, color: '#334155', fontWeight: 700 }}>Historical Performance Level</h4>
                        <div style={{ height: 220, width: '100%' }}><Line data={performanceChartData} options={performanceChartOptions} /></div>
                        {historicalPerfLoading && <div style={{ marginTop: 10, color: '#64748b' }}>Loading...</div>}
                        {!historicalPerfLoading && historicalPerformance.length === 0 && <div style={{ marginTop: 10, color: '#64748b' }}>No historical performance data.</div>}
                    </div>
                </div>
            </section>

            <footer className="dashboard-footer">
                <div className="footer-left"><button className="export-btn">📊 Export Data</button></div>
                <div className="footer-right"><button className="dark-mode-toggle" onClick={() => setDarkMode(!darkMode)}>{darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}</button></div>
            </footer>
        </div>
    );
};

export default CleanHiveDashboard;