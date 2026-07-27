import {
  FileText,
  Cpu,
  KeyRound,
  ExternalLink
} from "lucide-react";

const Sidebar = ({ selectedModel = "all", setSelectedModel }) => {
  return (
    <div className="sidebar">
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingBottom: "12px" }}>
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/3/32/Cmrit.png"
          width="140"
          height="90"
          alt="CMRIT Logo"
          style={{ objectFit: "contain" }}
        />
      </div>

      <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", letterSpacing: "1px", margin: "12px 0 6px 12px" }}>
        Main Workspace
      </div>

      <ul>
        <li
          className={selectedModel !== "models_info" && selectedModel !== "api" ? "active" : ""}
          onClick={() => setSelectedModel && setSelectedModel("all")}
          style={{ cursor: "pointer" }}
        >
          <FileText size={18} /> Single Analysis Workspace
        </li>

        <li
          className={selectedModel === "models_info" ? "active" : ""}
          onClick={() => setSelectedModel && setSelectedModel("models_info")}
          style={{ cursor: "pointer" }}
        >
          <Cpu size={18} /> All Models Overview & Guide
        </li>

        <div style={{ fontSize: "11px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", letterSpacing: "1px", margin: "20px 0 6px 12px" }}>
          Developer & API
        </div>

        <li
          className={selectedModel === "api" ? "active" : ""}
          onClick={() => setSelectedModel && setSelectedModel("api")}
          style={{
            cursor: "pointer",
            background: selectedModel === "api" ? "rgba(16, 185, 129, 0.2)" : "transparent",
            color: selectedModel === "api" ? "#10b981" : "inherit",
            fontWeight: selectedModel === "api" ? "bold" : "normal"
          }}
        >
          <KeyRound size={18} color="#10b981" /> API Access & Docs
        </li>

        <li>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            style={{ color: "inherit", textDecoration: "none", display: "flex", alignItems: "center", gap: "10px", width: "100%" }}
          >
            <ExternalLink size={18} /> Swagger REST Docs ↗
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;