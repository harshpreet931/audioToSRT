import { useState, useCallback } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from '@tauri-apps/plugin-dialog';
import "./App.css";

interface ConversionJob {
  id: string;
  fileName: string;
  filePath: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: string;
  outputPath?: string;
  error?: string;
}

function App() {
  const [jobs, setJobs] = useState<ConversionJob[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [modelSize, setModelSize] = useState('base');
  const [maxChars, setMaxChars] = useState(50);
  const [maxDuration, setMaxDuration] = useState(5.0);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    const audioFiles = files.filter(file => 
      file.type.startsWith('audio/') || 
      file.name.toLowerCase().endsWith('.mp3') ||
      file.name.toLowerCase().endsWith('.wav') ||
      file.name.toLowerCase().endsWith('.m4a') ||
      file.name.toLowerCase().endsWith('.flac')
    );

    for (const file of audioFiles) {
      const job: ConversionJob = {
        id: Date.now().toString() + Math.random().toString(36),
        fileName: file.name,
        filePath: file.path || '',
        status: 'pending',
        progress: 'Queued'
      };
      
      setJobs(prev => [...prev, job]);
      await processFile(job);
    }
  }, []);

  const handleFileSelect = async () => {
    try {
      const selected = await open({
        multiple: true,
        filters: [{
          name: 'Audio Files',
          extensions: ['mp3', 'wav', 'm4a', 'flac', 'ogg']
        }]
      });

      if (selected && Array.isArray(selected)) {
        for (const filePath of selected) {
          const fileName = filePath.split('/').pop() || filePath;
          const job: ConversionJob = {
            id: Date.now().toString() + Math.random().toString(36),
            fileName,
            filePath: filePath as string,
            status: 'pending',
            progress: 'Queued'
          };
          
          setJobs(prev => [...prev, job]);
          await processFile(job);
        }
      }
    } catch (error) {
      console.error('Error selecting files:', error);
    }
  };

  const processFile = async (job: ConversionJob) => {
    try {
      setJobs(prev => prev.map(j => 
        j.id === job.id 
          ? { ...j, status: 'processing', progress: 'Processing...' }
          : j
      ));

      const result = await invoke('convert_audio_to_srt', {
        filePath: job.filePath,
        modelSize,
        maxChars,
        maxDuration
      });

      setJobs(prev => prev.map(j => 
        j.id === job.id 
          ? { 
              ...j, 
              status: 'completed', 
              progress: 'Complete',
              outputPath: result as string
            }
          : j
      ));
    } catch (error) {
      setJobs(prev => prev.map(j => 
        j.id === job.id 
          ? { 
              ...j, 
              status: 'error', 
              progress: 'Failed',
              error: error as string
            }
          : j
      ));
    }
  };

  const clearCompleted = () => {
    setJobs(prev => prev.filter(job => job.status !== 'completed'));
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <img src="logo.png" alt="Audio to SRT" className="app-logo" />
          <h1>Audio to SRT</h1>
        </div>
        <div className="header-controls">
          <div className="status-indicator">
            <div className="status-dot"></div>
            Ready
          </div>
        </div>
      </header>

      <div className="settings-panel">
        <div className="setting-group">
          <label>Model</label>
          <select value={modelSize} onChange={(e) => setModelSize(e.target.value)}>
            <option value="tiny">Tiny</option>
            <option value="base">Base</option>
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="large">Large</option>
          </select>
        </div>
        
        <div className="setting-group">
          <label>Max chars</label>
          <input 
            type="number" 
            value={maxChars} 
            onChange={(e) => setMaxChars(Number(e.target.value))}
            min="20" 
            max="100"
          />
        </div>
        
        <div className="setting-group">
          <label>Duration</label>
          <input 
            type="number" 
            value={maxDuration} 
            onChange={(e) => setMaxDuration(Number(e.target.value))}
            min="1" 
            max="10" 
            step="0.5"
          />
        </div>
      </div>

      <div className="main-content">
        <div 
          className={`drop-zone ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleFileSelect}
        >
          <div className="drop-content">
            <div className="drop-icon">+</div>
            <h3>Drop audio files here</h3>
            <p>MP3, WAV, M4A, FLAC, OGG</p>
            <button className="browse-button">Browse</button>
          </div>
        </div>
      </div>

      {jobs.length > 0 && (
        <div className="jobs-section">
          <div className="jobs-header">
            <h3>Jobs ({jobs.length})</h3>
            <button onClick={clearCompleted} className="clear-button">
              Clear
            </button>
          </div>
          
          <div className="jobs-list">
            {jobs.map(job => (
              <div key={job.id} className={`job-item ${job.status}`}>
                <div className="job-status">
                  {job.status === 'processing' && <div className="spinner"></div>}
                  {job.status === 'completed' && <span className="status-icon">✓</span>}
                  {job.status === 'error' && <span className="status-icon">✗</span>}
                  {job.status === 'pending' && <span className="status-icon">-</span>}
                </div>
                <div className="job-info">
                  <div className="job-name">{job.fileName}</div>
                  <div className="job-progress">{job.progress}</div>
                  {job.error && <div className="job-error">{job.error}</div>}
                  {job.outputPath && (
                    <div className="job-output">
                      <span>Saved - </span>
                      <button 
                        onClick={() => invoke('reveal_in_finder', { path: job.outputPath })}
                        className="reveal-button"
                      >
                        Show
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {jobs.length === 0 && (
        <div className="empty-state">
          Perfect for DaVinci Resolve
        </div>
      )}
    </div>
  );
}

export default App;