import { useState } from 'react'
import URLInput from './components/URLInput'
import ResultsDisplay from './components/ResultsDisplay'
import './App.css'

function App() {
  const [modules, setModules] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleExtract = async (urls) => {
    setLoading(true)
    setError(null)
    setModules(null)

    try {
      const response = await fetch('/api/extract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to extract modules')
      }

      const data = await response.json()
      // Backend returns {modules: [...]}, extract the modules array
      const extractedModules = data.modules || data
      
      if (extractedModules && extractedModules.length > 0) {
        setModules(extractedModules)
      } else {
        setError('No modules found in the documentation. The URLs may not contain extractable module information.')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Module Extraction AI</h1>
        <p className="subtitle">Extract product modules from documentation</p>
      </header>

      <main className="app-main">
        <URLInput onExtract={handleExtract} loading={loading} />
        
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
            {error.includes('quota') || error.includes('429') ? (
              <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#fff3cd', borderRadius: '4px', fontSize: '0.9rem' }}>
                <strong>💡 Solution:</strong> Your OpenAI API quota has been exceeded. 
                <ul style={{ marginTop: '0.5rem', marginLeft: '1.5rem' }}>
                  <li>Check your usage at <a href="https://platform.openai.com/usage" target="_blank" rel="noopener noreferrer">platform.openai.com/usage</a></li>
                  <li>Add a payment method at <a href="https://platform.openai.com/account/billing" target="_blank" rel="noopener noreferrer">platform.openai.com/account/billing</a></li>
                  <li>Or use an alternative API provider (see TROUBLESHOOTING.md)</li>
                </ul>
              </div>
            ) : null}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            <div className="spinner"></div>
            <p>Extracting modules from documentation...</p>
            <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
              Processing multiple URLs, this may take a moment...
            </p>
          </div>
        )}

        {modules && <ResultsDisplay modules={modules} />}
      </main>
    </div>
  )
}

export default App

