import { useState } from "react";
import { analyzeText } from "../services/api";

const TextAnalyzer = ({ setResult, selectedModel, setSelectedModel }) => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setErrorMsg("");

    try {
      const res = await analyzeText(text, selectedModel);
      setResult(res);
    } catch (error) {
      console.error(error);
      setErrorMsg("Unable to connect to backend server. Make sure FastAPI server is running on http://127.0.0.1:8000.");
    }

    setLoading(false);
  };

  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3 style={{ margin: 0, fontSize: "16px", fontWeight: "700" }}>Analysis Workspace</h3>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          style={{
            padding: "6px 12px",
            borderRadius: "6px",
            background: "var(--bg-inner)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
            fontSize: "13px",
            fontWeight: "500",
            cursor: "pointer"
          }}
        >
          <option value="all">✨ All 3 Models (Blended Ensemble)</option>
          <option value="model_1">🤖 Model 1: BERT Transformer</option>
          <option value="model_2">📊 Model 2: Logistic Regression + SGD</option>
          <option value="model_3">⚡ Model 3: Dual TF-IDF Hybrid Ensemble</option>
        </select>
      </div>

      <textarea
        placeholder="Paste or type your essay / text sample here to run AI detection across all 3 models..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={7}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "8px",
          background: "var(--bg-inner)",
          color: "var(--text-primary)",
          border: "1px solid var(--border-color)",
          fontFamily: "inherit",
          resize: "vertical"
        }}
      />

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: "13px", color: "var(--text-muted)" }}>
          Word Count: <strong style={{ color: "var(--text-primary)" }}>{text.split(/\s+/).filter(Boolean).length}</strong>
        </span>
        <button
          onClick={handleAnalyze}
          disabled={loading || !text.trim()}
          style={{
            padding: "8px 20px",
            borderRadius: "6px",
            background: loading ? "var(--text-muted)" : "var(--accent-gradient)",
            color: "#ffffff",
            fontWeight: "600",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            marginTop: 0
          }}
        >
          {loading ? "Evaluating Models..." : `Analyze (${selectedModel === 'all' ? 'All 3 Models' : selectedModel.toUpperCase()})`}
        </button>
      </div>

      {errorMsg && (
        <div style={{ color: "#ef4444", fontSize: "13px", background: "rgba(239, 68, 68, 0.1)", padding: "8px", borderRadius: "6px" }}>
          {errorMsg}
        </div>
      )}
    </div>
  );
};

export default TextAnalyzer;