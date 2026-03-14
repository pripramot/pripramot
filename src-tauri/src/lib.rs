use tauri::AppHandle;
use serde::{Serialize, Deserialize};
use std::fs::{OpenOptions, create_dir_all};
use std::io::Write;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize, Clone)]
pub struct FileResult {
    name: String,
    path: String,
    size: u64,
}

/// Forensic log entry.  Every field is required per GEMINI.md §Security & Integrity.
#[derive(Serialize, Deserialize)]
pub struct ForensicLog {
    /// ISO-8601 timestamp of the event
    timestamp: String,
    /// User / process that triggered the action
    actor: String,
    /// Canonical name for the action (e.g. SEARCH, INSTALL, SCAN)
    action: String,
    /// SHA-256 of the input data / query
    input_hash: String,
    /// SHA-256 of the result / output data
    result_hash: String,
    /// Unique identifier for this node / machine
    node_id: String,
    /// Human-readable description of the event
    details: String,
}

/// Compute a hex-encoded SHA-256 digest of any string.
fn sha256_hex(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    format!("{:x}", hasher.finalize())
}

// --- Commands ---

#[tauri::command]
async fn search_files(query: String, path: String) -> Result<Vec<FileResult>, String> {
    let mut results = Vec::new();
    for entry in WalkDir::new(&path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let name = entry.file_name().to_string_lossy().to_string();
            if name.to_lowercase().contains(&query.to_lowercase()) {
                results.push(FileResult {
                    name,
                    path: entry.path().to_string_lossy().to_string(),
                    size: entry.metadata().map(|m| m.len()).unwrap_or(0),
                });
            }
        }
        if results.len() > 100 { break; } // Limit for UI performance
    }
    Ok(results)
}

/// Log an immutable forensic event to `.gstore/logs/audit.log`.
///
/// # Arguments
/// * `actor`   – Identity of the user or service performing the action.
/// * `action`  – Canonical action name (e.g. `SEARCH`, `INSTALL`, `SCAN`).
/// * `details` – Plain-text description of the event.
#[tauri::command]
fn log_forensic_event(
    app: AppHandle,
    actor: String,
    action: String,
    details: String,
) -> Result<(), String> {
    let log_dir = app.path().app_data_dir().unwrap_or_default().join(".gstore/logs");
    create_dir_all(&log_dir).map_err(|e| e.to_string())?;

    let log_file = log_dir.join("audit.log");
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_file)
        .map_err(|e| e.to_string())?;

    // Derive deterministic hashes so every entry is self-verifiable.
    let input_data = format!("{action}:{details}");
    let input_hash = sha256_hex(&input_data);

    // node_id: sha256 of the machine hostname.
    // NOTE: This is a best-effort identifier. For a fully stable and collision-free
    // node identity consider persisting a UUID on first run to `.gstore/node_id`.
    // TODO: Implement stable persistent UUID — see GEMINI.md §7 (Open TODOs, Low priority).
    let hostname = std::env::var("COMPUTERNAME")
        .or_else(|_| std::env::var("HOSTNAME"))
        .unwrap_or_else(|_| "unknown".to_string());
    let node_id = sha256_hex(&hostname);

    let result_data = format!("{input_hash}:{actor}:{node_id}");
    let result_hash = sha256_hex(&result_data);

    let log_entry = ForensicLog {
        timestamp: chrono::Local::now().to_rfc3339(),
        actor,
        action,
        input_hash,
        result_hash,
        node_id,
        details,
    };

    let json = serde_json::to_string(&log_entry).map_err(|e| e.to_string())?;
    writeln!(file, "{}", json).map_err(|e| e.to_string())?;

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![search_files, log_forensic_event])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
