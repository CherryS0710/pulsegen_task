import './ResultsDisplay.css'

function ResultsDisplay({ modules }) {
  if (!modules || modules.length === 0) {
    return (
      <div className="results-container">
        <div className="no-results">
          <p>No modules found in the documentation.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Extracted Modules</h2>
        <span className="module-count">{modules.length} module{modules.length !== 1 ? 's' : ''} found</span>
      </div>
      
      <div style={{ 
        marginBottom: '1.5rem', 
        padding: '0.75rem', 
        background: '#f0f0f0', 
        borderRadius: '6px',
        fontSize: '0.9rem',
        color: '#555'
      }}>
        <strong>Note:</strong> Modules have been extracted and merged from all provided documentation URLs.
      </div>

      <div className="modules-list">
        {modules.map((module, index) => (
          <div key={index} className="module-card">
            <div className="module-header">
              <h3 className="module-name">{module.module}</h3>
            </div>
            
            {module.description && (
              <p className="module-description">{module.description}</p>
            )}

            {module.submodules && Object.keys(module.submodules).length > 0 && (
              <div className="submodules-section">
                <h4 className="submodules-title">Submodules</h4>
                <ul className="submodules-list">
                  {Object.entries(module.submodules).map(([name, description], subIndex) => (
                    <li key={subIndex} className="submodule-item">
                      <span className="submodule-name">{name}</span>
                      {description && (
                        <span className="submodule-description">— {description}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="results-footer">
        <button
          onClick={() => {
            const json = JSON.stringify(modules, null, 2)
            navigator.clipboard.writeText(json)
            alert('JSON copied to clipboard!')
          }}
          className="copy-json-button"
        >
          Copy JSON to Clipboard
        </button>
      </div>
    </div>
  )
}

export default ResultsDisplay


