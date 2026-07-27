import { Sun, Moon } from "lucide-react";

const Header = ({ darkMode, setDarkMode }) => {
  return (
    <div className="header">
      <div>
        <h2 style={{ fontSize: "20px", fontWeight: "700" }}>AI Text Analytics Dashboard</h2>
        <span style={{ fontSize: "12px", color: "var(--text-muted)" }}>Multi-Model AI Text Detection & Stylometric Engine</span>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <span style={{ fontSize: "13px", fontWeight: "600", color: "#10b981", background: "rgba(16, 185, 129, 0.1)", padding: "6px 12px", borderRadius: "20px" }}>
          🟢 Status: Operational
        </span>

        <button
          onClick={() => setDarkMode && setDarkMode(!darkMode)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "8px 14px",
            borderRadius: "8px",
            background: "var(--bg-inner)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
            fontWeight: "600",
            cursor: "pointer",
            fontSize: "13px",
            marginTop: 0
          }}
        >
          {darkMode ? (
            <>
              <Sun size={16} color="#f59e0b" /> Light Mode
            </>
          ) : (
            <>
              <Moon size={16} color="#6366f1" /> Dark Mode
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default Header;