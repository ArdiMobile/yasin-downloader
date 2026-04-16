"use client";
import { useState } from 'react';
import { Download, Link, Loader2 } from 'lucide-react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleDownload = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('/api/download', {
        method: 'POST',
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Error fetching video");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center py-12 px-4">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-4xl font-bold text-blue-600 mb-2">FB Video Downloader</h1>
        <p className="text-slate-600 mb-8">Download Facebook videos in HD or SD quality for free.</p>
        
        <div className="flex gap-2 bg-white p-2 rounded-xl shadow-lg border border-slate-200">
          <div className="flex-1 flex items-center px-3">
            <Link className="text-slate-400 mr-2" size={20} />
            <input 
              className="w-full outline-none text-slate-700"
              placeholder="Paste Facebook video URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>
          <button 
            onClick={handleDownload}
            disabled={loading || !url}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition disabled:bg-slate-400"
          >
            {loading ? <Loader2 className="animate-spin" /> : "Extract"}
          </button>
        </div>

        {result && (
          <div className="mt-8 bg-white p-6 rounded-xl shadow-md border border-slate-100 animate-in fade-in zoom-in duration-300">
            <img src={result.thumbnail} className="w-full rounded-lg mb-4" alt="Preview" />
            <h3 className="font-semibold text-slate-800 mb-4">{result.title}</h3>
            <div className="grid grid-cols-2 gap-4">
              <a href={result.hd} target="_blank" className="bg-green-600 text-white py-2 rounded-lg flex items-center justify-center gap-2">
                <Download size={18}/> HD Quality
              </a>
              <a href={result.sd} target="_blank" className="bg-slate-800 text-white py-2 rounded-lg flex items-center justify-center gap-2">
                <Download size={18}/> SD Quality
              </a>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
