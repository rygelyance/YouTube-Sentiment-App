import React, { useState } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeSentiment = async () => {
    setLoading(true);
    setError('');
    setData(null);
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (!response.ok) throw new Error('Failed to analyze video');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-4 text-red-500">YouTube Sentiment Lens</h1>
        <p className="mb-8 text-gray-400">Enter a video link to see what the internet really thinks.</p>
        
        <div className="flex gap-4 mb-8">
          <input 
            type="text" 
            className="flex-1 p-3 rounded bg-gray-800 border border-gray-700 outline-none focus:border-red-500"
            placeholder="Paste YouTube URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button 
            onClick={analyzeSentiment}
            disabled={loading}
            className="bg-red-600 px-6 py-3 rounded font-bold hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        {error && <div className="p-4 bg-red-900/50 text-red-200 rounded mb-4">{error}</div>}

        {data && (
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h2 className="text-2xl font-bold mb-2">Overall: <span className="text-green-400">{data.overall_sentiment}</span></h2>
            <p className="text-gray-400 mb-6">Analyzed {data.total_analyzed} comments</p>
            
            <h3 className="text-lg font-semibold mb-3">Representative Comments:</h3>
            <div className="space-y-3">
              {data.representative_comments.map((comment, i) => (
                <div key={i} className="p-3 bg-gray-900 rounded italic border-l-4 border-red-500">
                  "{comment}"
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;