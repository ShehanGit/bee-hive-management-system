import { useState, useEffect } from 'react';
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
    FiEye,
    FiEyeOff,
    FiMaximize2,
    FiMinimize2
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

const ModernHiveDashboard = () => {
    const [selectedHiveId, setSelectedHiveId] = useState(1);
    const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
    const [currentTime, setCurrentTime] = useState(new Date());
    const [hiveData, setHiveData] = useState<HiveData | null>(null);
    const [historicalData, setHistoricalData] = useState<HiveData[]>([]);
    const [loading, setLoading] = useState(true);
    const [performancePrediction, setPerformancePrediction] = useState<PerformancePrediction | null>(null);
    const [performanceLoading, setPerformanceLoading] = useState(true);
    const [historicalPerformance, setHistoricalPerformance] = useState<HistoricalPerformance[]>([]);
    const [, setHistoricalPerfLoading] = useState(true);
    const [selectedSensor, setSelectedSensor] = useState<'temperature' | 'humidity' | 'weight' | 'sound'>('temperature');
    
    // Advanced Analytics State
    const [selectedChartType, setSelectedChartType] = useState<'line' | 'bar' | 'scatter'>('line');
    const [showPerformanceOverlay, setShowPerformanceOverlay] = useState(true);
    const [selectedMetrics, setSelectedMetrics] = useState({
        temperature: true,
        humidity: true,
        weight: true,
        sound: true,
        wind: true,
        rainfall: true,
        light: true
    });
    const [chartViewMode, setChartViewMode] = useState<'overview' | 'detailed'>('overview');
    const [isFullscreen, setIsFullscreen] = useState(false);

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
                // Ensure selectedTimeRange is valid
                const validTimeRange = ['24h', '1w', '1m'].includes(selectedTimeRange) ? selectedTimeRange : '24h';
                const hours = validTimeRange === '24h' ? 24 : validTimeRange === '1w' ? 168 : 720;
                console.log('Historical data request:', { selectedTimeRange, validTimeRange, hours });
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

    useEffect(() => {
        const fetchHistoricalPerformance = async () => {
            try {
                setHistoricalPerfLoading(true);
                // Ensure selectedTimeRange is valid
                const validTimeRange = ['24h', '1w', '1m'].includes(selectedTimeRange) ? selectedTimeRange : '24h';
                const hours = validTimeRange === '24h' ? 24 : validTimeRange === '1w' ? 168 : 720;
                console.log('Performance history request:', { selectedTimeRange, validTimeRange, hours });
                const response = await fetch(`http://127.0.0.1:5000/api/performance/history?hive_id=${selectedHiveId}&hours=${hours}`);
                const data = await response.json();
                setHistoricalPerformance(data.success && data.history ? data.history : []);
            } catch (error) {
                console.error('Error fetching performance history:', error);
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
    };
    const chartData = processChartData();

    // Advanced Analytics Data Processing
    const processAdvancedAnalytics = () => {
        if (!historicalData || historicalData.length === 0) return { labels: [], datasets: [] };
        
        const sortedData = [...historicalData].sort((a, b) => new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime());
        const labels = sortedData.map(item => new Date(item.collection_timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }));
        
        const datasets = [];
        
        // Temperature metrics
        if (selectedMetrics.temperature) {
            datasets.push({
                label: 'Internal Temp',
                data: sortedData.map(item => item.sensors?.temperature || null),
                borderColor: '#ff6b35',
                backgroundColor: 'rgba(255, 107, 53, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
            datasets.push({
                label: 'External Temp',
                data: sortedData.map(item => item.weather?.temperature || null),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
        }
        
        // Humidity metrics
        if (selectedMetrics.humidity) {
            datasets.push({
                label: 'Internal Humidity',
                data: sortedData.map(item => item.sensors?.humidity || null),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
            datasets.push({
                label: 'External Humidity',
                data: sortedData.map(item => item.weather?.humidity || null),
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(6, 182, 212, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
        }
        
        // Weight metric
        if (selectedMetrics.weight) {
            datasets.push({
                label: 'Hive Weight',
                data: sortedData.map(item => item.sensors?.weight || null),
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y1'
            });
        }
        
        // Sound metric
        if (selectedMetrics.sound) {
            datasets.push({
                label: 'Sound Level',
                data: sortedData.map(item => item.sensors?.sound || null),
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
        }
        
        // Wind metric
        if (selectedMetrics.wind) {
            datasets.push({
                label: 'Wind Speed',
                data: sortedData.map(item => item.weather?.wind_speed || null),
                borderColor: '#84cc16',
                backgroundColor: 'rgba(132, 204, 22, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y'
            });
        }
        
        // Rainfall metric
        if (selectedMetrics.rainfall) {
            datasets.push({
                label: 'Rainfall',
                data: sortedData.map(item => item.weather?.rainfall || null),
                borderColor: '#0ea5e9',
                backgroundColor: 'rgba(14, 165, 233, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y1'
            });
        }
        
        // Light metric
        if (selectedMetrics.light) {
            datasets.push({
                label: 'Light Intensity',
                data: sortedData.map(item => item.weather?.light_intensity || null),
                borderColor: '#f97316',
                backgroundColor: 'rgba(249, 115, 22, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y1'
            });
        }
        
        // Performance overlay
        if (showPerformanceOverlay && historicalPerformance.length > 0) {
            const perfData = historicalPerformance.map(perf => {
                const level = perf.predicted_level;
                return level === 1 ? 100 : level === 2 ? 80 : level === 3 ? 60 : level === 4 ? 40 : 20;
            });
            
            datasets.push({
                label: 'Performance Level',
                data: perfData,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: false,
                tension: 0.4,
                yAxisID: 'y2',
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            });
        }
        
        return { labels, datasets };
    };
    
    const advancedChartData = processAdvancedAnalytics();

    // Advanced Analytics Chart Configuration
    const advancedChartConfig = {
        type: selectedChartType,
        data: advancedChartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index' as const,
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Advanced Analytics Dashboard',
                    font: {
                        size: 18,
                        weight: 'bold' as const
                    },
                    color: '#1e293b'
                },
                legend: {
                    display: true,
                    position: 'top' as const,
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            weight: 'bold' as const
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    titleColor: '#1e293b',
                    bodyColor: '#64748b',
                    borderColor: '#e2e8f0',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        title: (context: any) => {
                            return `Time: ${context[0].label}`;
                        },
                        label: (context: any) => {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y;
                            let unit = '';
                            
                            if (label.includes('Temp')) unit = '°C';
                            else if (label.includes('Humidity')) unit = '%';
                            else if (label.includes('Weight')) unit = 'kg';
                            else if (label.includes('Sound')) unit = 'dB';
                            else if (label.includes('Wind')) unit = 'km/h';
                            else if (label.includes('Rainfall')) unit = 'mm';
                            else if (label.includes('Light')) unit = 'lux';
                            else if (label.includes('Performance')) unit = '%';
                            
                            return `${label}: ${value?.toFixed(1) || 'N/A'}${unit}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time',
                        font: {
                            size: 14,
                            weight: 'bold' as const
                        },
                        color: '#64748b'
                    },
                    grid: {
                        color: 'rgba(226, 232, 240, 0.5)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: {
                            size: 11
                        }
                    }
                },
                y: {
                    type: 'linear' as const,
                    display: true,
                    position: 'left' as const,
                    title: {
                        display: true,
                        text: 'Temperature, Humidity, Sound, Wind (°C, %, dB, km/h)',
                        font: {
                            size: 12,
                            weight: 'bold' as const
                        },
                        color: '#64748b'
                    },
                    grid: {
                        color: 'rgba(226, 232, 240, 0.5)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: {
                            size: 11
                        }
                    }
                },
                y1: {
                    type: 'linear' as const,
                    display: true,
                    position: 'right' as const,
                    title: {
                        display: true,
                        text: 'Weight, Rainfall, Light (kg, mm, lux)',
                        font: {
                            size: 12,
                            weight: 'bold' as const
                        },
                        color: '#64748b'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        color: '#64748b',
                        font: {
                            size: 11
                        }
                    }
                },
                y2: {
                    type: 'linear' as const,
                    display: showPerformanceOverlay,
                    position: 'right' as const,
                    min: 0,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Performance Level (%)',
                        font: {
                            size: 12,
                            weight: 'bold' as const
                        },
                        color: '#ef4444'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        color: '#ef4444',
                        font: {
                            size: 11
                        },
                        callback: function(value: any) {
                            const level = Math.round((100 - value) / 20) + 1;
                            return `Level ${level}`;
                        }
                    }
                }
            },
            elements: {
                point: {
                    radius: 3,
                    hoverRadius: 6,
                    borderWidth: 2
                },
                line: {
                    borderWidth: 2
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart' as const
            }
        }
    };

    // Get selected sensor configuration
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

    const getPerformanceChartData = () => {
        if (!historicalPerformance || historicalPerformance.length === 0) return { labels: [], datasets: [] };
        const sorted = [...historicalPerformance].sort((a, b) => new Date(a.collection_timestamp).getTime() - new Date(b.collection_timestamp).getTime());
        return {
            labels: sorted.map(item => new Date(item.collection_timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })),
            datasets: [{ 
                label: 'Performance Level', 
                data: sorted.map(item => item.predicted_level), 
                borderColor: '#ff6b35', 
                backgroundColor: 'rgba(255, 107, 53, 0.1)', 
                fill: true, 
                tension: 0.4, 
                pointRadius: 2 
            }]
        };
    };
    const performanceChartData = getPerformanceChartData();

    const performanceChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { display: false }, 
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
                ticks: { 
                    color: '#64748b',
                    stepSize: 1, 
                    callback: function(tickValue: string | number) { 
                        const value = typeof tickValue === 'number' ? tickValue : parseInt(tickValue as string, 10); 
                        return value === 1 ? 'Excellent' : value === 2 ? 'Good' : value === 3 ? 'Moderate' : value === 4 ? 'Poor' : value === 5 ? 'Critical' : value; 
                    } 
                } 
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
            {/* Header */}
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

            {/* Main Dashboard Grid */}
            <div className="dashboard-grid">
                {/* Top Row - Main Metrics */}
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

                {/* Middle Row - Sensor Cards */}
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

                {/* Bottom Row - Performance & Weather */}
                <div className="bottom-row">
                    <div className="performance-section">
                        <PerformanceCard performance={performance} />
                        <div className="performance-chart">
                            <h4><FiBarChart className="chart-icon" /> Performance History</h4>
                            <div className="chart-wrapper">
                                <Line data={performanceChartData} options={performanceChartOptions} />
                            </div>
                        </div>
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

                {/* Advanced Analytics Section - Bottom */}
                <div className="advanced-analytics-section">
                    <div className="analytics-header">
                        <div className="analytics-title">
                            <FiBarChart className="analytics-icon" />
                            <h2>Advanced Analytics</h2>
                            <span className="analytics-subtitle">Multi-dimensional data correlation analysis</span>
                        </div>
                        <div className="analytics-controls">
                            <div className="control-group">
                                <label>Chart Type:</label>
                                <select value={selectedChartType} onChange={(e) => setSelectedChartType(e.target.value as 'line' | 'bar' | 'scatter')}>
                                    <option value="line">Line Chart</option>
                                    <option value="bar">Bar Chart</option>
                                    <option value="scatter">Scatter Plot</option>
                                </select>
                            </div>
                            <div className="control-group">
                                <label>View Mode:</label>
                                <select value={chartViewMode} onChange={(e) => setChartViewMode(e.target.value as 'overview' | 'detailed')}>
                                    <option value="overview">Overview</option>
                                    <option value="detailed">Detailed</option>
                                </select>
                            </div>
                            <button 
                                className={`toggle-btn ${showPerformanceOverlay ? 'active' : ''}`}
                                onClick={() => setShowPerformanceOverlay(!showPerformanceOverlay)}
                            >
                                {showPerformanceOverlay ? <FiEye /> : <FiEyeOff />}
                                Performance Overlay
                            </button>
                            <button 
                                className="fullscreen-btn"
                                onClick={() => setIsFullscreen(!isFullscreen)}
                            >
                                {isFullscreen ? <FiMinimize2 /> : <FiMaximize2 />}
                            </button>
                        </div>
                    </div>
                    
                    <div className="metrics-selector">
                        <div className="selector-label">Select Metrics:</div>
                        <div className="metrics-grid">
                            {Object.entries(selectedMetrics).map(([key, value]) => (
                                <label key={key} className="metric-checkbox">
                                    <input
                                        type="checkbox"
                                        checked={value}
                                        onChange={(e) => setSelectedMetrics(prev => ({ ...prev, [key]: e.target.checked }))}
                                    />
                                    <span className="checkbox-label">
                                        {key === 'temperature' && <FiThermometer />}
                                        {key === 'humidity' && <FiDroplet />}
                                        {key === 'weight' && <FiActivity />}
                                        {key === 'sound' && <FiVolume2 />}
                                        {key === 'wind' && <FiWind />}
                                        {key === 'rainfall' && <FiCloudRain />}
                                        {key === 'light' && <FiSun />}
                                        {key.charAt(0).toUpperCase() + key.slice(1)}
                                    </span>
                                </label>
                            ))}
                        </div>
                    </div>
                    
                    <div className={`analytics-chart-container ${isFullscreen ? 'fullscreen' : ''}`}>
                        <div className="chart-wrapper">
                            <Line {...advancedChartConfig} />
                        </div>
                    </div>
                    
                    <div className="analytics-insights">
                        <div className="insights-header">
                            <FiTrendingUp className="insights-icon" />
                            <h3>Key Insights</h3>
                        </div>
                        <div className="insights-grid">
                            <div className="insight-card">
                                <div className="insight-title">Temperature Correlation</div>
                                <div className="insight-value">
                                    {hiveData?.sensors?.temperature && hiveData?.weather?.temperature 
                                        ? `${(hiveData.sensors.temperature - hiveData.weather.temperature).toFixed(1)}°C diff`
                                        : 'N/A'
                                    }
                                </div>
                                <div className="insight-description">Internal vs External temperature difference</div>
                            </div>
                            <div className="insight-card">
                                <div className="insight-title">Humidity Stability</div>
                                <div className="insight-value">
                                    {hiveData?.sensors?.humidity 
                                        ? `${hiveData.sensors.humidity.toFixed(1)}%`
                                        : 'N/A'
                                    }
                                </div>
                                <div className="insight-description">Current internal humidity level</div>
                            </div>
                            <div className="insight-card">
                                <div className="insight-title">Activity Level</div>
                                <div className="insight-value">
                                    {hiveData?.sensors?.sound 
                                        ? `${hiveData.sensors.sound.toFixed(1)} dB`
                                        : 'N/A'
                                    }
                                </div>
                                <div className="insight-description">Bee activity sound intensity</div>
                            </div>
                            <div className="insight-card">
                                <div className="insight-title">Performance Trend</div>
                                <div className="insight-value" style={{ color: performance.color }}>
                                    Level {performance.predicted_level}
                                </div>
                                <div className="insight-description">{performance.interpretation}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModernHiveDashboard;
