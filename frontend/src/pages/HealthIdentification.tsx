import React, { useState, useRef, useCallback } from 'react';
import Navbar from "../components/Navbar";
import './HealthIdentification.css';

interface BeeDetection {
  is_bee: boolean;
  confidence: number;
}

interface DiseaseDetection {
  disease: string;
  confidence: number;
  recommendation: string;
}

interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
}

interface PredictionResult {
  bee_detection: BeeDetection;
  disease_detection: DiseaseDetection | null;
  bounding_boxes?: BoundingBox[];
}

function HealthIdentification() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  const handleFileSelect = useCallback((file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      setError('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setError('');
    setUploadProgress(0);
    
    // Create preview URL with progress simulation
    const reader = new FileReader();
    reader.onloadstart = () => setUploadProgress(10);
    reader.onprogress = (e) => {
      if (e.lengthComputable) {
        setUploadProgress(10 + (e.loaded / e.total) * 80);
      }
    };
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
      setUploadProgress(100);
      setTimeout(() => setUploadProgress(0), 1000);
    };
    reader.readAsDataURL(file);
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsLoading(true);
    setError('');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);

      // Health identification service runs on port 5000
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}. Please ensure the ML service is running.`);
      }

      const data: PredictionResult = await response.json();
      setResult(data);
      
      // Reset progress after showing results
      setTimeout(() => setUploadProgress(0), 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during analysis. Please check if the ML service is running on port 5000.');
      setUploadProgress(0);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    setResult(null);
    setError('');
    setUploadProgress(0);
    setIsDragOver(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleTryAnother = () => {
    setResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const getHealthStatusColor = (disease: string) => {
    switch (disease.toLowerCase()) {
      case 'healthy': return '#4CAF50';
      case 'varroa': return '#ff9800';
      case 'wax moth': return '#f44336';
      default: return '#9E9E9E';
    }
  };

  const getBoundingBoxColor = (label: string) => {
    if (label.includes('Varroa') || label.includes('Mite')) return '#ff9800';
    if (label.includes('Healthy') || label.includes('healthy')) return '#4CAF50';
    if (label.includes('Wax') || label.includes('Moth') || label.includes('Damage')) return '#f44336';
    return '#2196F3';
  };

  // Render bounding boxes on the image
  const renderBoundingBoxes = () => {
    if (!previewUrl || !result?.bounding_boxes) return null;
    
    return result.bounding_boxes.map((box, index) => (
      <div
        key={index}
        className="bounding-box"
        style={{
          position: 'absolute',
          left: `${box.x}%`,
          top: `${box.y}%`,
          width: `${box.width}%`,
          height: `${box.height}%`,
          border: `3px solid ${getBoundingBoxColor(box.label)}`,
          borderRadius: box.label.includes('Healthy') ? '50%' : '0',
          boxSizing: 'border-box',
          pointerEvents: 'none',
        }}
      >
        <div
          className="bounding-box-label"
          style={{
            position: 'absolute',
            top: '-20px',
            left: '0',
            background: getBoundingBoxColor(box.label),
            color: 'white',
            padding: '2px 6px',
            borderRadius: '3px',
            fontSize: '12px',
            fontWeight: 'bold',
            whiteSpace: 'nowrap',
          }}
        >
          {box.label}
        </div>
      </div>
    ));
  };

  return (
    <div className="health-identification">
      <Navbar />
      
      <div className="health-content">
        <header className="health-header">
          <div className="header-content">
            <div className="header-icon">🔬</div>
            <h1>Bee Health AI Analysis</h1>
            <p>Upload an image of a bee to get instant AI-powered health diagnostics and treatment recommendations</p>
            <div className="feature-badges">
              <span className="badge">✨ AI-Powered</span>
              <span className="badge">⚡ Instant Results</span>
              <span className="badge">🎯 High Accuracy</span>
            </div>
          </div>
        </header>

        <div className="health-main">
          <div className="upload-section">
            <div className="section-header">
              <h2>📷 Upload Image</h2>
              <p>Select a clear image of a bee for analysis</p>
            </div>
            
            <div 
              className={`upload-area ${isDragOver ? 'drag-over' : ''} ${previewUrl ? 'has-image' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {previewUrl ? (
                <div className="image-preview">
                  <div className="image-container" style={{ position: 'relative', display: 'inline-block' }}>
                    <img 
                      ref={imageRef}
                      src={previewUrl} 
                      alt="Selected bee" 
                      style={{ maxWidth: '100%', maxHeight: '400px' }}
                    />
                    {renderBoundingBoxes()}
                    <div className="image-overlay">
                      <button className="overlay-btn reset" onClick={handleReset}>
                        ✖ Remove
                      </button>
                      <button className="overlay-btn change" onClick={() => fileInputRef.current?.click()}>
                        🔄 Change
                      </button>
                    </div>
                  </div>
                  <div className="image-info">
                    <span className="file-name">{selectedFile?.name}</span>
                    <span className="file-size">{selectedFile ? (selectedFile.size / 1024 / 1024).toFixed(2) + ' MB' : ''}</span>
                  </div>
                </div>
              ) : (
                <div className="upload-placeholder">
                  <div className="upload-animation">
                    <div className="upload-icon">📷</div>
                    <div className="upload-ripple"></div>
                  </div>
                  <h3>Drag & Drop or Click to Upload</h3>
                  <p>Support for JPG, PNG, WEBP up to 10MB</p>
                  <div className="upload-features">
                    <span>✓ Instant processing</span>
                    <span>✓ Secure & private</span>
                    <span>✓ High accuracy</span>
                  </div>
                </div>
              )}
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleInputChange}
                className="file-input"
                id="file-input"
              />
              {!previewUrl && (
                <label htmlFor="file-input" className="upload-btn">
                  <span>📁</span> Select Image
                </label>
              )}
            </div>

            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="progress-container">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
                <span className="progress-text">{uploadProgress.toFixed(0)}% uploaded</span>
              </div>
            )}

            {selectedFile && (
              <div className="action-buttons">
                <button 
                  className={`analyze-btn ${isLoading ? 'loading' : ''}`}
                  onClick={handleAnalyze}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <div className="spinner"></div>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      <span>Analyze Health</span>
                    </>
                  )}
                </button>
              </div>
            )}
          </div>

          <div className="results-section">
            <div className="section-header">
              <h2>📈 Analysis Results</h2>
              <p>AI-powered health diagnostics and recommendations</p>
            </div>
            
            {error && (
              <div className="error-message animate-in">
                <div className="error-icon">⚠️</div>
                <div className="error-content">
                  <h3>Analysis Failed</h3>
                  <p>{error}</p>
                  <button className="retry-btn" onClick={() => setError('')}>
                    Try Again
                  </button>
                </div>
              </div>
            )}

            {!result && !error && !isLoading && (
              <div className="placeholder-message">
                <div className="placeholder-icon">🔬</div>
                <h3>Ready for Analysis</h3>
                <p>Upload a bee image to get started with AI health diagnostics</p>
                <div className="analysis-features">
                  <div className="feature">
                    <span className="feature-icon">🐝</span>
                    <span>Bee Detection</span>
                  </div>
                  <div className="feature">
                    <span className="feature-icon">🎯</span>
                    <span>Disease Classification</span>
                  </div>
                  <div className="feature">
                    <span className="feature-icon">💡</span>
                    <span>Treatment Recommendations</span>
                  </div>
                </div>
              </div>
            )}

            {isLoading && (
              <div className="loading-message animate-in">
                <div className="loading-animation">
                  <div className="loading-icon">🤖</div>
                  <div className="loading-waves">
                    <div className="wave"></div>
                    <div className="wave"></div>
                    <div className="wave"></div>
                  </div>
                </div>
                <h3>Analyzing Image...</h3>
                <p>Our AI is examining the bee for health indicators</p>
                {uploadProgress > 0 && (
                  <div className="analysis-progress">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                    <span>Processing: {uploadProgress.toFixed(0)}%</span>
                  </div>
                )}
              </div>
            )}

            {result && (
              <div className="results-container animate-in">
                <div className="result-summary">
                  <div className="summary-icon">
                    {result.bee_detection.is_bee ? '✅' : '❌'}
                  </div>
                  <div className="summary-text">
                    <h3>
                      {result.bee_detection.is_bee 
                        ? 'Bee Successfully Detected!' 
                        : 'No Bee Detected'}
                    </h3>
                    <p>
                      {result.bee_detection.is_bee 
                        ? 'Analysis completed with health diagnostics' 
                        : 'Please upload a clear image of a bee'}
                    </p>
                  </div>
                </div>

                <div className="result-cards">
                  <div className="result-card bee-detection">
                    <div className="card-header">
                      <h3>🐝 Bee Detection</h3>
                    </div>
                    <div className="detection-status">
                      <span className={`status-badge ${result.bee_detection.is_bee ? 'positive' : 'negative'}`}>
                        {result.bee_detection.is_bee ? '✓ Bee Detected' : '✗ No Bee Detected'}
                      </span>
                    </div>
                  </div>

                  {result.disease_detection && (
                    <div className="result-card disease-detection">
                      <div className="card-header">
                        <h3>🎯 Health Analysis</h3>
                      </div>
                      <div className="health-status">
                        <div 
                          className="health-badge"
                          style={{ backgroundColor: getHealthStatusColor(result.disease_detection.disease) }}
                        >
                          <span className="health-icon">
                            {result.disease_detection.disease === 'healthy' ? '🟢' : 
                             result.disease_detection.disease === 'varroa' ? '🟠' : '🔴'}
                          </span>
                          {result.disease_detection.disease.charAt(0).toUpperCase() + 
                           result.disease_detection.disease.slice(1)}
                        </div>
                      </div>
                      
                      <div className="recommendation">
                        <h4>💡 Treatment Recommendation</h4>
                        <div className="recommendation-content">
                          <p>{result.disease_detection.recommendation}</p>
                          {result.disease_detection.disease !== 'healthy' && (
                            <div className="urgency-indicator">
                              <span className="urgency-label">Action Required:</span>
                              <span className={`urgency-level ${result.disease_detection.disease === 'varroa' ? 'high' : 'medium'}`}>
                                {result.disease_detection.disease === 'varroa' ? 'Immediate' : 'Soon'}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {result.bee_detection.is_bee && !result.disease_detection && (
                    <div className="result-card info-card">
                      <div className="card-header">
                        <h3>ℹ️ Analysis Note</h3>
                      </div>
                      <p>Bee detected successfully, but health analysis is currently unavailable. Please ensure the image is clear and well-lit, then try again.</p>
                    </div>
                  )}
                </div>

                <div className="action-footer">
                  <button className="secondary-btn" onClick={handleTryAnother}>
                    <span>📷</span> Analyze Another
                  </button>
                  <button className="primary-btn" onClick={handleReset}>
                    <span>🔄</span> Start Over
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default HealthIdentification;