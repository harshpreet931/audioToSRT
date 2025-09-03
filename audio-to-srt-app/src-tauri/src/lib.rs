use std::path::Path;
use std::process::Command;
use tauri::Manager;

#[tauri::command]
async fn convert_audio_to_srt(
    file_path: String,
    model_size: String,
    max_chars: i32,
    max_duration: f64,
    app_handle: tauri::AppHandle,
) -> Result<String, String> {
    // Get the path to our Python script
    let resource_path = app_handle
        .path()
        .resource_dir()
        .map_err(|e| format!("Failed to get resource directory: {}", e))?;
    
    let script_path = resource_path.join("audio_to_srt.py");
    
    // Create output path (same directory as input, but with .srt extension)
    let input_path = Path::new(&file_path);
    let output_path = input_path.with_extension("srt");
    let output_str = output_path.to_string_lossy().to_string();
    
    // Execute Python script
    let output = Command::new("python3")
        .arg(script_path)
        .arg(&file_path)
        .arg("-o")
        .arg(&output_str)
        .arg("-m")
        .arg(&model_size)
        .arg("--max-chars")
        .arg(max_chars.to_string())
        .arg("--max-duration")
        .arg(max_duration.to_string())
        .output()
        .map_err(|e| format!("Failed to execute Python script: {}", e))?;
    
    if output.status.success() {
        Ok(output_str)
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr);
        Err(format!("Python script failed: {}", stderr))
    }
}

#[tauri::command]
async fn reveal_in_finder(path: String) -> Result<(), String> {
    #[cfg(target_os = "macos")]
    {
        Command::new("open")
            .args(["-R", &path])
            .spawn()
            .map_err(|e| format!("Failed to reveal file: {}", e))?;
    }
    
    #[cfg(target_os = "windows")]
    {
        Command::new("explorer")
            .args(["/select,", &path])
            .spawn()
            .map_err(|e| format!("Failed to reveal file: {}", e))?;
    }
    
    #[cfg(target_os = "linux")]
    {
        Command::new("xdg-open")
            .arg(std::path::Path::new(&path).parent().unwrap_or(std::path::Path::new(&path)))
            .spawn()
            .map_err(|e| format!("Failed to reveal file: {}", e))?;
    }
    
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            convert_audio_to_srt,
            reveal_in_finder
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
