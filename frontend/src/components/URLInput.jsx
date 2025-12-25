import { useState } from 'react'
import './URLInput.css'

function URLInput({ onExtract, loading }) {
  const [urls, setUrls] = useState([''])
  const [urlErrors, setUrlErrors] = useState({})

  const validateURL = (url) => {
    if (!url.trim()) return false
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  }

  const handleUrlChange = (index, value) => {
    const newUrls = [...urls]
    newUrls[index] = value
    setUrls(newUrls)

    // Clear error for this URL
    if (urlErrors[index]) {
      const newErrors = { ...urlErrors }
      delete newErrors[index]
      setUrlErrors(newErrors)
    }
  }

  const handleAddUrl = () => {
    setUrls([...urls, ''])
  }

  const handleRemoveUrl = (index) => {
    if (urls.length === 1) return
    const newUrls = urls.filter((_, i) => i !== index)
    setUrls(newUrls)
    
    const newErrors = { ...urlErrors }
    delete newErrors[index]
    // Reindex errors
    const reindexedErrors = {}
    Object.keys(newErrors).forEach(key => {
      const oldIndex = parseInt(key)
      if (oldIndex > index) {
        reindexedErrors[oldIndex - 1] = newErrors[key]
      } else if (oldIndex < index) {
        reindexedErrors[oldIndex] = newErrors[key]
      }
    })
    setUrlErrors(reindexedErrors)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const errors = {}
    const validUrls = []
    
    urls.forEach((url, index) => {
      if (!url.trim()) {
        if (urls.length === 1) {
          errors[index] = 'Please enter at least one URL'
        }
      } else if (!validateURL(url)) {
        errors[index] = 'Please enter a valid URL'
      } else {
        validUrls.push(url.trim())
      }
    })

    if (Object.keys(errors).length > 0) {
      setUrlErrors(errors)
      return
    }

    if (validUrls.length === 0) {
      setUrlErrors({ 0: 'Please enter at least one URL' })
      return
    }

    onExtract(validUrls)
  }

  return (
    <form className="url-input-form" onSubmit={handleSubmit}>
      <div className="url-input-container">
        <label className="form-label">
          Documentation URLs
          <span className="label-hint">Enter one or more URLs to analyze</span>
        </label>
        
        {urls.map((url, index) => (
          <div key={index} className="url-input-row">
            <input
              type="text"
              value={url}
              onChange={(e) => handleUrlChange(index, e.target.value)}
              placeholder="https://example.com/docs"
              className={`url-input ${urlErrors[index] ? 'error' : ''}`}
              disabled={loading}
            />
            {urls.length > 1 && (
              <button
                type="button"
                onClick={() => handleRemoveUrl(index)}
                className="remove-button"
                disabled={loading}
                aria-label="Remove URL"
              >
                ×
              </button>
            )}
            {urlErrors[index] && (
              <span className="error-text">{urlErrors[index]}</span>
            )}
          </div>
        ))}
      </div>

      <div className="form-actions">
        <button
          type="button"
          onClick={handleAddUrl}
          className="add-url-button"
          disabled={loading}
        >
          + Add Another URL
        </button>
        
        <button
          type="submit"
          className="extract-button"
          disabled={loading}
        >
          {loading ? 'Extracting...' : 'Extract Modules'}
        </button>
      </div>
    </form>
  )
}

export default URLInput


