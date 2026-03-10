use tauri::AppHandle;
use serde::{Serialize, Deserialize};
use std::time::SystemTime;
use std::fs::{OpenOptions, create_dir_all};
use std::io::Write;
use walkdir::WalkDir;

#[derive(Serialize, Deserialize, Clone)]
pub struct FileResult {
    name: String,
    path: String,
    size: u64,
}

#[derive(Serialize, Deserialize)]
pub struct ForensicLog {
    timestamp: String,
    action: String,
    details: String,
}

// --- Commands ---

#[tauri::command]
async fn search_files(query: String, path: String) -> Result<Vec<FileResult>, String> {
    let mut results = Vec::new();
    for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
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

#[tauri::command]
fn log_forensic_event(app: AppHandle, action: String, details: String) -> Result<(), String> {
    let log_dir = app.path().app_data_dir().unwrap_or_default().join(".gstore/logs");
    create_dir_all(&log_dir).map_err(|e| e.to_string())?;
    
    let log_file = log_dir.join("audit.log");
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_file)
        .map_err(|e| e.to_string())?;

    let log_entry = ForensicLog {
        timestamp: chrono::Local::now().to_rfc3339(),
        action,
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
