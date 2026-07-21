# LabelIt! Local Setup Guide

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Git (optional, for cloning)**
   ```bash
   git --version
   ```

## Installation Steps

### Option 1: Quick Setup (Recommended)

1. **Download or clone the project**
   ```bash
   # If using git
   git clone <your-repo-url>
   cd labelit

   # Or download and extract the ZIP file
   ```

2. **Install Python dependencies**
   ```bash
   # Install required packages
   pip install streamlit pandas pillow plotly requests openpyxl

   # Or if you have requirements.txt
   pip install -r requirements.txt
   ```

3. **Create data directory**
   ```bash
   mkdir -p data/images
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Open in browser**
   - The app will automatically open at: http://localhost:5000
   - Or manually visit: http://127.0.0.1:5000

### Option 2: Using Virtual Environment (Best Practice)

1. **Create virtual environment**
   ```bash
   python -m venv labelit_env
   
   # Activate (Windows)
   labelit_env\Scripts\activate
   
   # Activate (Mac/Linux)
   source labelit_env/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas pillow plotly requests openpyxl
   ```

3. **Create data directory**
   ```bash
   mkdir -p data/images
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Configuration

### Custom Port
```bash
streamlit run app.py --server.port 8080
```

### Custom Configuration
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8501
   ```

2. **Module not found errors**
   ```bash
   pip install --upgrade streamlit pandas pillow plotly requests openpyxl
   ```

3. **Permission errors on data directory**
   ```bash
   chmod 755 data
   chmod 755 data/images
   ```

4. **Database issues**
   - Delete `data/labelit.db` to reset
   - The app will recreate it automatically

### System Requirements

- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: 1GB free space for images and database
- **Network**: Internet connection for geolocation features
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## Features Available Locally

✅ **Full functionality available:**
- User registration and authentication
- Image upload with compression
- Geolocation capture (IP-based)
- Multilingual support (14 languages)
- Real-time analytics dashboard
- Data export (Excel, ZIP)
- Professional UI with custom styling

✅ **Persistent data storage:**
- SQLite database for all user data
- Local filesystem for image storage
- Session state for user preferences

## Development Mode

For development with auto-reload:
```bash
streamlit run app.py --server.runOnSave true
```

## Production Deployment

For production use, consider:
- Using a reverse proxy (nginx)
- Setting up SSL/TLS certificates
- Configuring proper backup systems
- Monitoring and logging setup

## Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. Verify all dependencies are installed
3. Ensure the data directory has proper permissions
4. Check if the port is available