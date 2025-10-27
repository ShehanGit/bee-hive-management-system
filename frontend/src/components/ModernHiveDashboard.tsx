import { useState, useEffect, useMemo, memo } from 'react';
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
import { 
    FiThermometer, 
    FiDroplet, 
    FiVolume2, 
    FiActivity, 
    FiSun, 
    FiWind, 
    FiTrendingUp,
    FiBarChart,
    FiCloudRain,
    FiAlertCircle,
    FiCheckCircle,
    FiInfo
} from 'react-icons/fi';
import './ModernHiveDashboard.css';

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

// Modern Circular Gauge Component
const ModernGauge = ({ value, min, max, unit, label, color, icon: IconComponent, size = 'large' }: {
    value: number | null;
    min: number;
    max: number;
    unit: string;
    label: string;
    color: string;
    icon: React.ComponentType<{ className?: string }>;
    size?: 'small' | 'large';
}) => {
    const percentage = value !== null ? Math.min(Math.max(((value - min) / (max - min)) * 100, 0), 100) : 0;
    const rotation = (percentage / 100) * 180 - 90;
    const gaugeSize = size === 'large' ? 200 : 120;

    return (
        <div className={`modern-gauge ${size}`}>
            <div className="gauge-header">
                <IconComponent className="gauge-icon" />
                <h3>{label}</h3>
            </div>
            <div className="gauge-container">
                <svg viewBox={`0 0 ${gaugeSize} ${gaugeSize/2 + 40}`} className="gauge-svg">
                    <defs>
                        <linearGradient id={`gradient-${color}`} x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor={color} stopOpacity="0.8" />
                            <stop offset="100%" stopColor={color} stopOpacity="1" />
                        </linearGradient>
                    </defs>
                    <path 
                        d={`M 30 ${gaugeSize/2 + 20} A ${gaugeSize/2 - 20} ${gaugeSize/2 - 20} 0 0 1 ${gaugeSize - 30} ${gaugeSize/2 + 20}`} 
                        fill="none" 
                        stroke="rgba(255,255,255,0.1)" 
                        strokeWidth="8" 
                        strokeLinecap="round" 
                    />
                    <path 
                        d={`M 30 ${gaugeSize/2 + 20} A ${gaugeSize/2 - 20} ${gaugeSize/2 - 20} 0 0 1 ${gaugeSize - 30} ${gaugeSize/2 + 20}`} 
                        fill="none" 
                        stroke={`url(#gradient-${color})`} 
                        strokeWidth="8" 
                        strokeLinecap="round" 
                        strokeDasharray={`${(percentage / 100) * 220} 220`} 
                        className="gauge-arc"
                    />
                    <g transform={`rotate(${rotation} ${gaugeSize/2} ${gaugeSize/2 + 20})`}>
                        <line 
                            x1={gaugeSize/2} 
                            y1={gaugeSize/2 + 20} 
                            x2={gaugeSize/2} 
                            y2="40" 
                            stroke={color} 
                            strokeWidth="4" 
                            strokeLinecap="round"
                        />
                        <circle cx={gaugeSize/2} cy={gaugeSize/2 + 20} r="8" fill={color} />
                    </g>
                    <circle 
                        cx={gaugeSize/2} 
                        cy={gaugeSize/2 + 20} 
                        r="12" 
                        fill="white" 
                        stroke={color} 
                        strokeWidth="3"
                    />
                </svg>
            </div>
            <div className="gauge-value-container">
                <div className="gauge-value" style={{ color }}>{value !== null ? value.toFixed(1) : 'N/A'}</div>
                <div className="gauge-unit">{unit}</div>
            </div>
            <div className="gauge-range">
                <span className="range-min">{min}{unit}</span>
                <span className="range-max">{max}{unit}</span>
            </div>
        </div>
    );
};

// Modern Metric Card Component
const MetricCard = ({ title, value, unit, icon: IconComponent, trend, color = '#ff6b35', isSelected = false, onClick }: {
    title: string;
    value: number | string | null;
    unit: string;
    icon: React.ComponentType<{ className?: string }>;
    trend?: string;
    color?: string;
    isSelected?: boolean;
    onClick?: () => void;
}) => {
    return (
        <div 
            className={`metric-card ${isSelected ? 'selected' : ''}`} 
            onClick={onClick}
            style={{ cursor: 'pointer' }}
        >
            <div className="metric-header">
                <IconComponent className="metric-icon" />
            </div>
            <div className="metric-content">
                <div className="metric-value" style={{ color }}>
                    {value !== null ? value : 'N/A'}
                    <span className="metric-unit">{unit}</span>
                </div>
                <h4 className="metric-title">{title}</h4>
                {trend && <div className="metric-trend">{trend}</div>}
            </div>
        </div>
    );
};

// Performance Status Card
const PerformanceCard = ({ performance }: { performance: any }) => {
    const getStatusColor = (level: number) => {
        switch (level) {
            case 1: return '#22c55e';
            case 2: return '#3b82f6';
            case 3: return '#facc15';
            case 4: return '#f59e42';
            case 5: return '#ef4444';
            default: return '#6b7280';
        }
    };

    const statusColor = getStatusColor(performance.predicted_level);
    const progressPercentage = (performance.predicted_level / 5) * 100;

    return (
        <div className="performance-card-modern">
            <div className="performance-circle-container">
                <svg className="performance-circle-svg" viewBox="0 0 200 200">
                    {/* Background circle */}
                    <circle
                        cx="100"
                        cy="100"
                        r="90"
                        fill="none"
                        stroke="rgba(255, 255, 255, 0.1)"
                        strokeWidth="8"
                    />
                    {/* Progress circle - Orange color */}
                    <circle
                        cx="100"
                        cy="100"
                        r="90"
                        fill="none"
                        stroke="#ff6b35"
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={`${(progressPercentage / 100) * 565} 565`}
                        transform="rotate(-90 100 100)"
                        className="performance-progress"
                    />
                    {/* Level markers */}
                    {[1, 2, 3, 4, 5].map((level) => {
                        const angle = (level / 5) * 360 - 90;
                        const x = 100 + 90 * Math.cos((angle * Math.PI) / 180);
                        const y = 100 + 90 * Math.sin((angle * Math.PI) / 180);
                        return (
                            <circle
                                key={level}
                                cx={x}
                                cy={y}
                                r="4"
                                fill={level <= performance.predicted_level ? '#ff6b35' : 'rgba(255, 255, 255, 0.2)'}
                                className="level-marker"
                            />
                        );
                    })}
                    {/* Level text inside circle */}
                    <text x="100" y="100" textAnchor="middle" className="level-number">
                        {performance.predicted_level}
                    </text>
                    <text x="100" y="130" textAnchor="middle" className="level-text">
                        Level
                    </text>
                </svg>
            </div>
            <div className="performance-text-container">
                <div className="performance-label">{performance.interpretation}</div>
                <div className="performance-confidence">
                    Confidence: {typeof performance.confidence === 'number' ? (performance.confidence * 100).toFixed(1) : performance.confidence}%
                </div>
                <div className="performance-risk" style={{ color: statusColor }}>
                    {performance.risk_assessment}
                </div>
            </div>
        </div>
    );
};

// Memoized Header Component - only re-renders when props change
const DashboardHeader = memo(({ selectedHiveId, setSelectedHiveId, currentTime }: {
    selectedHiveId: number;
    setSelectedHiveId: (id: number) => void;
    currentTime: Date;
}) => {
    const formatTime = (date: Date) => {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };
    
    const formatDate = (date: Date) => {
        return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    };

    return (
        <header className="dashboard-header">
            <div className="header-left">
                <div className="dashboard-title">
                    <div className="title-content">
                        <h1>Real-Time Dashboard</h1>
                        <p className="title-subtitle">Live Hive Monitoring & Analytics</p>
                    </div>
                </div>
                <div className="hive-selector-modern">
                    <div className="selector-label">Active Hive</div>
                    <div className="selector-wrapper">
                        <select id="hive-select" value={selectedHiveId} onChange={(e) => setSelectedHiveId(parseInt(e.target.value))}>
                            <option value={1}>Hive #1</option>
                            <option value={2}>Hive #2</option>
                            <option value={3}>Hive #3</option>
                        </select>
                        <div className="selector-indicator"></div>
                    </div>
                </div>
            </div>
            <div className="header-right">
                <div className="datetime-modern">
                    <div className="time-modern">{formatTime(currentTime)}</div>
                    <div className="date-modern">{formatDate(currentTime)}</div>
                </div>
            </div>
        </header>
    );
});

DashboardHeader.displayName = 'DashboardHeader';

const ModernHiveDashboard = () => {
    const [selectedHiveId, setSelectedHiveId] = useState(1);
    const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
    const [currentTime, setCurrentTime] = useState(new Date());
    const [hiveData, setHiveData] = useState<HiveData | null>(null);
    const [historicalData, setHistoricalData] = useState<HiveData[]>([]);
    const [loading, setLoading] = useState(true);
    const [performancePrediction, setPerformancePrediction] = useState<PerformancePrediction | null>(null);
    const [performanceLoading, setPerformanceLoading] = useState(false);
    const [historicalPerformance, setHistoricalPerformance] = useState<HistoricalPerformance[]>([]);
    const [isManualPredicting, setIsManualPredicting] = useState(false);
    const [selectedSensor, setSelectedSensor] = useState<'temperature' | 'humidity' | 'weight' | 'sound'>('temperature');
    const [showAnalysis, setShowAnalysis] = useState(false);
    const [analysisData, setAnalysisData] = useState<any>(null);

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        // Show loading only when hive changes or initial load
        setLoading(true);
        
        const fetchHiveData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/latest?hive_id=${selectedHiveId}`);
                const data = await response.json();
                setHiveData(data.success && data.data ? data.data : null);
                setLoading(false);
            } catch (error) {
                setHiveData(null);
                setLoading(false);
            }
        };
        
        // Initial fetch
        fetchHiveData();
        
        // Periodic background updates (only fetch, no loading state)
        const interval = setInterval(() => {
            fetch(`http://127.0.0.1:5000/api/synchronized/latest?hive_id=${selectedHiveId}`)
                .then(res => res.json())
                .then(data => {
                    setHiveData(data.success && data.data ? data.data : null);
                })
                .catch(() => {
                    // Silent fail on background updates
                });
        }, 30000);
        
        return () => clearInterval(interval);
    }, [selectedHiveId]);

    // Analyzation function - triggers prediction and generates insights
    const analyzeHivePerformance = async () => {
        try {
            setShowAnalysis(true);
            setIsManualPredicting(true);
            setPerformanceLoading(true);
            
            console.log('Analyzing hive performance for hive:', selectedHiveId);
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 120000);
            
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/performance/predict`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ hive_id: selectedHiveId }),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.error || 'Unknown error'}`);
                }
                
                const data = await response.json();
                
                if (data.success && data.prediction) {
                    setPerformancePrediction(data.prediction);
                    
                    // Generate simple analysis for beekeeper
                    const analysis = generateAnalysis(data.prediction, hiveData);
                    setAnalysisData(analysis);
                } else {
                    throw new Error(data.error || 'Failed to generate prediction');
                }
            } catch (fetchError) {
                if (fetchError instanceof Error && fetchError.name === 'AbortError') {
                    throw new Error('Analysis is taking too long. Please try again.');
                }
                throw fetchError;
            }
        } catch (error) {
            console.error('Error analyzing performance:', error);
            alert('Error analyzing performance: ' + (error instanceof Error ? error.message : String(error)));
        } finally {
            setPerformanceLoading(false);
            setIsManualPredicting(false);
        }
    };

    // Generate simple, easy-to-understand analysis
    const generateAnalysis = (prediction: any, currentData: any) => {
        const level = prediction.predicted_level;
        const confidence = prediction.confidence;
        const riskAssessment = prediction.risk_assessment;
        
        // Determine overall status
        let overallStatus = 'Unknown';
        let statusColor = '#64748b';
        let statusIcon = <FiInfo />;
        
        if (level <= 2) {
            overallStatus = 'Healthy';
            statusColor = '#22c55e';
            statusIcon = <FiCheckCircle />;
        } else if (level === 3) {
            overallStatus = 'Monitor';
            statusColor = '#facc15';
            statusIcon = <FiInfo />;
        } else {
            overallStatus = 'Attention Needed';
            statusColor = '#ef4444';
            statusIcon = <FiAlertCircle />;
        }
        
        // Key insights
        const insights = [];
        const features = [];
        
        // Temperature insight
        if (currentData?.sensors?.temperature && currentData?.weather?.temperature) {
            const tempDiff = currentData.sensors.temperature - currentData.weather.temperature;
            if (tempDiff > 5) {
                insights.push({
                    type: 'temperature',
                    status: 'good',
                    message: 'Hive is maintaining temperature well above external temperature',
                    recommendation: 'Hive is active and generating heat'
                });
            } else if (tempDiff < 2) {
                insights.push({
                    type: 'temperature',
                    status: 'warning',
                    message: 'Hive temperature is close to external temperature',
                    recommendation: 'Monitor closely - colony may be struggling to maintain heat'
                });
            }
            
            // Add feature analysis
            features.push({
                name: 'Temperature Stability',
                value: `${Math.abs(tempDiff).toFixed(1)}°C difference`,
                impact: tempDiff > 5 ? 'High - Good colony activity' : tempDiff > 2 ? 'Medium - Normal' : 'Low - Needs attention',
                icon: 'temperature',
                color: '#ef4444'
            });
        }
        
        // Humidity insight
        if (currentData?.sensors?.humidity) {
            const humidity = currentData.sensors.humidity;
            if (humidity < 40) {
                insights.push({
                    type: 'humidity',
                    status: 'warning',
                    message: 'Hive humidity is low',
                    recommendation: 'Consider adding a water source nearby'
                });
            } else if (humidity > 70) {
                insights.push({
                    type: 'humidity',
                    status: 'warning',
                    message: 'Hive humidity is high',
                    recommendation: 'Check ventilation - ensure proper airflow'
                });
            }
            
            // Add feature analysis
            features.push({
                name: 'Humidity Level',
                value: `${humidity.toFixed(1)}%`,
                impact: humidity >= 40 && humidity <= 70 ? 'High - Optimal for bees' : 'Medium - Monitor closely',
                icon: 'humidity',
                color: '#3b82f6'
            });
        }
        
        // Sound/Activity insight
        if (currentData?.sensors?.sound) {
            const sound = currentData.sensors.sound;
            if (sound > 70) {
                insights.push({
                    type: 'activity',
                    status: 'good',
                    message: 'High bee activity detected',
                    recommendation: 'Colony is very active'
                });
            } else if (sound < 40) {
                insights.push({
                    type: 'activity',
                    status: 'warning',
                    message: 'Low bee activity',
                    recommendation: 'Monitor closely - may indicate colony stress'
                });
            }
            
            // Add feature analysis
            features.push({
                name: 'Colony Activity',
                value: `${sound.toFixed(1)} dB`,
                impact: sound > 60 ? 'High - Active colony' : sound > 40 ? 'Medium - Normal activity' : 'Low - Reduced activity',
                icon: 'activity',
                color: '#10b981'
            });
        }
        
        // Weight insight
        if (currentData?.sensors?.weight && historicalData.length > 10) {
            const sortedData = [...historicalData].sort((a, b) => 
                new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime()
            );
            const lastWeight = sortedData[sortedData.length - 1]?.sensors?.weight;
            const firstWeight = sortedData[0]?.sensors?.weight;
            const weightChange = lastWeight && firstWeight ? lastWeight - firstWeight : 0;
            if (weightChange > 1) {
                insights.push({
                    type: 'weight',
                    status: 'good',
                    message: 'Hive weight is increasing',
                    recommendation: 'Good sign - bees are collecting resources'
                });
            } else if (weightChange < -1) {
                insights.push({
                    type: 'weight',
                    status: 'warning',
                    message: 'Hive weight is decreasing',
                    recommendation: 'Monitor consumption - may need supplementary feeding'
                });
            }
            
            // Removed Hive Weight Change feature
        }
        
        // Weather conditions impact
        if (currentData?.weather) {
            const weather = currentData.weather;
            let weatherImpact = 'Good';
            
            // Check if weather is favorable for foraging
            const isGoodForForaging = weather.temperature && weather.temperature > 15 && 
                                      weather.temperature && weather.temperature < 35 && 
                                      weather.rainfall === 0 && 
                                      weather.wind_speed && weather.wind_speed < 25 &&
                                      weather.light_intensity && weather.light_intensity > 1000;
            
            if (!isGoodForForaging) {
                if (weather.temperature && (weather.temperature > 35 || weather.temperature < 10)) {
                    weatherImpact = 'Poor - Extreme temperature';
                } else if (weather.rainfall && weather.rainfall > 0) {
                    weatherImpact = 'Poor - Rain';
                } else if (weather.wind_speed && weather.wind_speed > 25) {
                    weatherImpact = 'Fair - High wind';
                }
            }
            
            features.push({
                name: 'Weather Conditions',
                value: `${weather.temperature ? weather.temperature.toFixed(1) : 'N/A'}°C, ${weather.humidity ? weather.humidity.toFixed(0) : 'N/A'}%`,
                impact: weatherImpact,
                icon: weather.rainfall && weather.rainfall > 0 ? 'rain' : weather.temperature && weather.temperature > 30 ? 'sun' : 'cloud',
                color: '#f59e0b'
            });
        }
        
        // Removed Data Quality feature
        
        // Historical data availability
        if (historicalData.length > 0) {
            features.push({
                name: 'Historical Data',
                value: `${historicalData.length} records`,
                impact: historicalData.length > 100 ? 'High - Good trend analysis' : historicalData.length > 50 ? 'Medium - Basic trends' : 'Low - Limited history',
                icon: 'trend',
                color: '#8b5cf6'
            });
        }
        
        return {
            overallStatus,
            statusColor,
            statusIcon,
            confidence: (confidence * 100).toFixed(1),
            level,
            interpretation: prediction.interpretation,
            riskAssessment,
            insights,
            features,
            probabilities: prediction.all_probabilities || {}
        };
    };

    useEffect(() => {
        const fetchHistoricalData = async () => {
            try {
                const validTimeRange = ['24h', '1w', '1m'].includes(selectedTimeRange) ? selectedTimeRange : '24h';
                const hours = validTimeRange === '24h' ? 24 : validTimeRange === '1w' ? 168 : 720;
                const response = await fetch(`http://127.0.0.1:5000/api/synchronized/historical?hive_id=${selectedHiveId}&hours=${hours}`);
                const data = await response.json();
                setHistoricalData(data.success && data.data ? data.data : []);
            } catch (error) {
                console.error('Error fetching historical data:', error);
                setHistoricalData([]);
            }
        };
        fetchHistoricalData();
    }, [selectedHiveId, selectedTimeRange]);

    const getPerformanceStatus = () => {
        if (performanceLoading) return { predicted_level: '-', interpretation: 'Loading...', confidence: '-', risk_assessment: '', all_probabilities: {}, color: 'gray', timestamp: '' };
        if (!performancePrediction) return { predicted_level: '-', interpretation: 'Unknown', confidence: '-', risk_assessment: '', all_probabilities: {}, color: 'gray', timestamp: '' };
        return {
            ...performancePrediction,
            color: performancePrediction.predicted_level === 1 ? '#22c55e' : performancePrediction.predicted_level === 2 ? '#3b82f6' : performancePrediction.predicted_level === 3 ? '#facc15' : performancePrediction.predicted_level === 4 ? '#f59e42' : '#ef4444'
        };
    };
    const performance = getPerformanceStatus();

    const chartData = useMemo(() => {
        if (!historicalData || historicalData.length === 0) return { temperature: { labels: [], datasets: [] }, humidity: { labels: [], datasets: [] }, weight: { labels: [], datasets: [] }, sound: { labels: [], datasets: [] } };
        const sortedData = [...historicalData].sort((a, b) => new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime());
        const labels = sortedData.map(item => new Date(item.collection_timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }));
        return {
            temperature: { 
                labels, 
                datasets: [
                    { 
                        label: 'Internal Temperature', 
                        data: sortedData.map(item => item.sensors?.temperature || null), 
                        borderColor: '#ff6b35', 
                        backgroundColor: 'rgba(255, 107, 53, 0.1)', 
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
            },
            humidity: { 
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
            },
            weight: { 
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
            },
            sound: { 
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
            }
        };
    }, [historicalData]);

    const getSelectedSensorConfig = () => {
        const configs = {
            temperature: {
                value: hiveData?.sensors?.temperature || null,
                min: 0,
                max: 50,
                unit: '°C',
                label: 'Temperature',
                color: '#ff6b35',
                icon: FiThermometer,
                chartData: chartData.temperature
            },
            humidity: {
                value: hiveData?.sensors?.humidity || null,
                min: 0,
                max: 100,
                unit: '%',
                label: 'Humidity',
                color: '#10b981',
                icon: FiDroplet,
                chartData: chartData.humidity
            },
            weight: {
                value: hiveData?.sensors?.weight || null,
                min: 0,
                max: 100,
                unit: 'kg',
                label: 'Weight',
                color: '#f59e0b',
                icon: FiActivity,
                chartData: chartData.weight
            },
            sound: {
                value: hiveData?.sensors?.sound || null,
                min: 0,
                max: 100,
                unit: 'dB',
                label: 'Sound Level',
                color: '#8b5cf6',
                icon: FiVolume2,
                chartData: chartData.sound
            }
        };
        return configs[selectedSensor];
    };
    const selectedSensorConfig = getSelectedSensorConfig();

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { 
                position: 'top' as const, 
                labels: { 
                    usePointStyle: true, 
                    padding: 20,
                    color: '#1e293b',
                    font: { size: 12 }
                } 
            }, 
            tooltip: { 
                mode: 'index' as const, 
                intersect: false, 
                backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                titleColor: '#1e293b', 
                bodyColor: '#1e293b', 
                borderColor: '#ff6b35', 
                borderWidth: 2,
                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
            } 
        },
        scales: { 
            x: { 
                display: true, 
                grid: { color: 'rgba(100, 116, 139, 0.2)' },
                ticks: { color: '#64748b' }
            }, 
            y: { 
                display: true, 
                grid: { color: 'rgba(100, 116, 139, 0.2)' },
                ticks: { color: '#64748b' }
            } 
        },
        interaction: { mode: 'nearest' as const, axis: 'x' as const, intersect: false }
    };

    if (loading) {
        return (
            <div className="modern-dashboard">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading hive data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="modern-dashboard">
            <DashboardHeader 
                selectedHiveId={selectedHiveId} 
                setSelectedHiveId={setSelectedHiveId} 
                currentTime={currentTime} 
            />

            <div className="dashboard-grid">
                <div className="main-metrics-row">
                    <div className="main-gauge-container">
                        <ModernGauge 
                            value={selectedSensorConfig.value} 
                            min={selectedSensorConfig.min} 
                            max={selectedSensorConfig.max} 
                            unit={selectedSensorConfig.unit} 
                            label={selectedSensorConfig.label} 
                            color={selectedSensorConfig.color} 
                            icon={selectedSensorConfig.icon}
                            size="large"
                        />
                    </div>
                    <div className="main-chart-container">
                        <div className="chart-header">
                            <h3><FiTrendingUp className="chart-icon" /> {selectedSensorConfig.label} Trends</h3>
                            <div className="time-range-selector">
                                <button className={selectedTimeRange === '24h' ? 'active' : ''} onClick={() => setSelectedTimeRange('24h')}>24h</button>
                                <button className={selectedTimeRange === '1w' ? 'active' : ''} onClick={() => setSelectedTimeRange('1w')}>1w</button>
                                <button className={selectedTimeRange === '1m' ? 'active' : ''} onClick={() => setSelectedTimeRange('1m')}>1m</button>
                            </div>
                        </div>
                        <div className="chart-wrapper">
                            <Line data={selectedSensorConfig.chartData} options={chartOptions} />
                        </div>
                    </div>
                </div>

                <div className="sensor-cards-row">
                    <MetricCard 
                        title="Temperature" 
                        value={hiveData?.sensors?.temperature?.toFixed(1) || null} 
                        unit="°C" 
                        icon={FiThermometer} 
                        color="#ff6b35"
                        isSelected={selectedSensor === 'temperature'}
                        onClick={() => setSelectedSensor('temperature')}
                    />
                    <MetricCard 
                        title="Humidity" 
                        value={hiveData?.sensors?.humidity?.toFixed(1) || null} 
                        unit="%" 
                        icon={FiDroplet} 
                        color="#10b981"
                        isSelected={selectedSensor === 'humidity'}
                        onClick={() => setSelectedSensor('humidity')}
                    />
                    <MetricCard 
                        title="Weight" 
                        value={hiveData?.sensors?.weight?.toFixed(1) || null} 
                        unit="kg" 
                        icon={FiActivity} 
                        color="#f59e0b"
                        isSelected={selectedSensor === 'weight'}
                        onClick={() => setSelectedSensor('weight')}
                    />
                    <MetricCard 
                        title="Sound Level" 
                        value={hiveData?.sensors?.sound?.toFixed(1) || null} 
                        unit="dB" 
                        icon={FiVolume2} 
                        color="#8b5cf6"
                        isSelected={selectedSensor === 'sound'}
                        onClick={() => setSelectedSensor('sound')}
                    />
                </div>

                <div className="bottom-row">
                    <div className="performance-section">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
                            <PerformanceCard performance={performance} />
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <button 
                                    onClick={analyzeHivePerformance} 
                                    disabled={isManualPredicting || performanceLoading}
                                    style={{
                                        padding: '12px 24px',
                                        fontSize: '16px',
                                        fontWeight: 'bold',
                                        backgroundColor: isManualPredicting || performanceLoading ? '#94a3b8' : '#ff6b35',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '8px',
                                        cursor: isManualPredicting || performanceLoading ? 'not-allowed' : 'pointer',
                                        transition: 'all 0.3s ease',
                                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                                        opacity: isManualPredicting || performanceLoading ? 0.6 : 1
                                    }}
                                    onMouseEnter={(e) => !isManualPredicting && !performanceLoading && (e.currentTarget.style.backgroundColor = '#e55a26')}
                                    onMouseLeave={(e) => !isManualPredicting && !performanceLoading && (e.currentTarget.style.backgroundColor = '#ff6b35')}
                                >
                                    {isManualPredicting || performanceLoading ? 'Analyzing...' : 'Analyze Hive Performance'}
                                </button>
                                {!performancePrediction && !isManualPredicting && !performanceLoading && (
                                    <div style={{ fontSize: '12px', color: '#64748b', fontStyle: 'italic' }}>
                                        Click to get detailed analysis
                                    </div>
                                )}
                            </div>
                        </div>

                        {showAnalysis && analysisData && (
                            <div className="analysis-section">
                                <div className="analysis-header">
                                    <h3><FiBarChart className="analysis-icon" /> Hive Performance Analysis</h3>
                                </div>
                                
                                <div className="analysis-summary">
                                    <div className="summary-card" style={{ borderLeft: `4px solid ${analysisData.statusColor}` }}>
                                        <div className="summary-status">
                                            {analysisData.statusIcon}
                                            <span style={{ color: analysisData.statusColor, fontWeight: 'bold' }}>
                                                {analysisData.overallStatus}
                                            </span>
                                        </div>
                                        <div className="summary-level">Level {analysisData.level} Performance</div>
                                        <div className="summary-confidence">{analysisData.confidence}% Confidence</div>
                                    </div>
                                    
                                    <div className="summary-description">
                                        <p><strong>Status:</strong> {analysisData.interpretation}</p>
                                        <p><strong>Risk Assessment:</strong> {analysisData.riskAssessment}</p>
                                    </div>
                                </div>

                                <div className="analysis-insights">
                                    <h4>Key Insights</h4>
                                    {analysisData.insights.length > 0 ? (
                                        <div className="insights-list">
                                            {analysisData.insights.map((insight: any, index: number) => (
                                                <div key={index} className={`insight-item ${insight.status}`}>
                                                    <div className="insight-header">
                                                        <span className="insight-type">{insight.type}</span>
                                                        <span className="insight-badge" style={{ 
                                                            backgroundColor: insight.status === 'good' ? '#22c55e' : '#f59e42',
                                                            color: 'white',
                                                            padding: '2px 8px',
                                                            borderRadius: '4px',
                                                            fontSize: '11px',
                                                            fontWeight: 'bold'
                                                        }}>
                                                            {insight.status === 'good' ? 'Good' : 'Monitor'}
                                                        </span>
                                                    </div>
                                                    <div className="insight-message">{insight.message}</div>
                                                    <div className="insight-recommendation">
                                                        <FiInfo /> {insight.recommendation}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <div className="no-insights">No specific insights available at this time.</div>
                                    )}
                                </div>

                                <div className="analysis-features">
                                    <h4>Key Features Used for Prediction</h4>
                                    <div className="features-grid">
                                        {analysisData.features && analysisData.features.map((feature: any, index: number) => {
                                            // Map icon names to React Icons components
                                            const IconComponent = 
                                                feature.icon === 'temperature' ? FiThermometer :
                                                feature.icon === 'humidity' ? FiDroplet :
                                                feature.icon === 'activity' ? FiActivity :
                                                feature.icon === 'rain' ? FiCloudRain :
                                                feature.icon === 'sun' ? FiSun :
                                                feature.icon === 'cloud' ? FiWind :
                                                FiTrendingUp;
                                            
                                            return (
                                                <div key={index} className="feature-card" style={{ borderTop: `3px solid ${feature.color}` }}>
                                                    <div className="feature-header">
                                                        <div className="feature-icon-wrapper" style={{ backgroundColor: `${feature.color}15`, color: feature.color }}>
                                                            <IconComponent />
                                                        </div>
                                                        <span className="feature-name">{feature.name}</span>
                                                    </div>
                                                    <div className="feature-value" style={{ color: feature.color }}>{feature.value}</div>
                                                    <div className="feature-impact">{feature.impact}</div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>

                                <div className="analysis-probabilities">
                                    <h4>Performance Level Probabilities</h4>
                                    <div className="probabilities-grid">
                                        <div className="prob-item">
                                            <div className="prob-label">Excellent</div>
                                            <div className="prob-bar">
                                                <div 
                                                    className="prob-fill" 
                                                    style={{ 
                                                        width: `${(analysisData.probabilities['Level_1'] || 0) * 100}%`,
                                                        backgroundColor: '#22c55e'
                                                    }}
                                                />
                                            </div>
                                            <div className="prob-value">{(analysisData.probabilities['Level_1'] || 0) * 100}%</div>
                                        </div>
                                        <div className="prob-item">
                                            <div className="prob-label">Good</div>
                                            <div className="prob-bar">
                                                <div 
                                                    className="prob-fill" 
                                                    style={{ 
                                                        width: `${(analysisData.probabilities['Level_2'] || 0) * 100}%`,
                                                        backgroundColor: '#3b82f6'
                                                    }}
                                                />
                                            </div>
                                            <div className="prob-value">{(analysisData.probabilities['Level_2'] || 0) * 100}%</div>
                                        </div>
                                        <div className="prob-item">
                                            <div className="prob-label">Moderate</div>
                                            <div className="prob-bar">
                                                <div 
                                                    className="prob-fill" 
                                                    style={{ 
                                                        width: `${(analysisData.probabilities['Level_3'] || 0) * 100}%`,
                                                        backgroundColor: '#facc15'
                                                    }}
                                                />
                                            </div>
                                            <div className="prob-value">{(analysisData.probabilities['Level_3'] || 0) * 100}%</div>
                                        </div>
                                        <div className="prob-item">
                                            <div className="prob-label">Poor</div>
                                            <div className="prob-bar">
                                                <div 
                                                    className="prob-fill" 
                                                    style={{ 
                                                        width: `${(analysisData.probabilities['Level_4'] || 0) * 100}%`,
                                                        backgroundColor: '#f59e42'
                                                    }}
                                                />
                                            </div>
                                            <div className="prob-value">{(analysisData.probabilities['Level_4'] || 0) * 100}%</div>
                                        </div>
                                        <div className="prob-item">
                                            <div className="prob-label">Critical</div>
                                            <div className="prob-bar">
                                                <div 
                                                    className="prob-fill" 
                                                    style={{ 
                                                        width: `${(analysisData.probabilities['Level_5'] || 0) * 100}%`,
                                                        backgroundColor: '#ef4444'
                                                    }}
                                                />
                                            </div>
                                            <div className="prob-value">{(analysisData.probabilities['Level_5'] || 0) * 100}%</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className="weather-section">
                        <div className="weather-card">
                            <div className="weather-header">
                                <FiSun className="weather-icon" />
                                <h3>Environmental</h3>
                            </div>
                            <div className="weather-grid">
                                <div className="weather-item">
                                    <FiThermometer className="weather-item-icon" />
                                    <div className="weather-item-content">
                                        <div className="weather-item-label">External Temp</div>
                                        <div className="weather-item-value">{hiveData?.weather?.temperature?.toFixed(1) || 'N/A'}°C</div>
                                    </div>
                                </div>
                                <div className="weather-item">
                                    <FiDroplet className="weather-item-icon" />
                                    <div className="weather-item-content">
                                        <div className="weather-item-label">Humidity</div>
                                        <div className="weather-item-value">{hiveData?.weather?.humidity?.toFixed(1) || 'N/A'}%</div>
                                    </div>
                                </div>
                                <div className="weather-item">
                                    <FiWind className="weather-item-icon" />
                                    <div className="weather-item-content">
                                        <div className="weather-item-label">Wind Speed</div>
                                        <div className="weather-item-value">{hiveData?.weather?.wind_speed?.toFixed(1) || 'N/A'} km/h</div>
                                    </div>
                                </div>
                                <div className="weather-item">
                                    <FiSun className="weather-item-icon" />
                                    <div className="weather-item-content">
                                        <div className="weather-item-label">Light</div>
                                        <div className="weather-item-value">{hiveData?.weather?.light_intensity?.toFixed(0) || 'N/A'} lux</div>
                                    </div>
                                </div>
                                <div className="weather-item">
                                    <FiCloudRain className="weather-item-icon" />
                                    <div className="weather-item-content">
                                        <div className="weather-item-label">Rainfall</div>
                                        <div className="weather-item-value">{hiveData?.weather?.rainfall?.toFixed(1) || 'N/A'} mm</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModernHiveDashboard;
