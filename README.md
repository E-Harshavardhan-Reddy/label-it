---
title: LabelIt!
emoji: 🏷️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.47.1"
app_file: app.py
pinned: false
---

# 🏷️ LabelIt! – Multilingual Image Labeling Platform

LabelIt! is a modern, multilingual image labeling platform...
---

# ✨ Features

* 🌍 Support for **13 Indian languages + English**
* 📷 Image upload with validation and compression
* 🏷️ Image categorization and labeling
* 📍 Automatic geolocation capture (Browser GPS & IP fallback)
* 👥 User authentication and profile management
* 📊 Interactive analytics dashboard
* 📈 Category, language, activity, and contribution statistics
* 💾 SQLite database for persistent storage
* 📦 Export labeled datasets
* 🎨 Responsive professional UI built with Streamlit

---

# 🛠️ Tech Stack

| Technology   | Purpose            |
| ------------ | ------------------ |
| Python 3.11+ | Backend            |
| Streamlit    | Web Application    |
| SQLite       | Database           |
| Pillow       | Image Processing   |
| Pandas       | Data Analysis      |
| Plotly       | Interactive Charts |
| Requests     | Geolocation APIs   |
| OpenPyXL     | Excel Export       |

---

# 📂 Project Structure

```
Label-It/
│
├── app.py                  # Main Streamlit application
├── backend.py              # Database operations
├── geolocation.py          # GPS & IP location services
├── translations.py         # Multilingual support
├── visualization.py        # Analytics dashboard
├── styles.py               # UI styling
├── utils.py                # Image processing utilities
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Dependency lock file
├── LICENSE
├── README.md
└── data/
    └── images/
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Label-It.git

cd Label-It
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv sync
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

The application will start at:

```
http://localhost:8501
```

---

# 🌐 Supported Languages

* English
* Hindi
* Telugu
* Tamil
* Kannada
* Malayalam
* Bengali
* Marathi
* Gujarati
* Punjabi
* Odia
* Assamese
* Urdu
* Sanskrit

---

# 📝 Image Labeling Workflow

1. Register or log in.
2. Select your preferred language.
3. Upload an image.
4. Choose an image category.
5. Enter labels in your language.
6. Capture geolocation (optional).
7. Save the annotation.
8. View analytics and statistics.

---

# 📊 Analytics Dashboard

The dashboard provides insights such as:

* Total labeled images
* Images by category
* Language usage
* User contributions
* Daily annotation activity
* Geographic distribution of labels

---

# 🗄️ Database

The application uses SQLite for storage.

Typical data includes:

* User accounts
* Uploaded images
* Image metadata
* Labels
* Language preferences
* Geolocation
* Analytics

---

# 🔒 Authentication

The platform includes:

* User registration
* Secure login
* Session management
* Personalized language preferences

---

# 📍 Geolocation

LabelIt! supports two methods:

* Browser GPS (preferred)
* IP-based fallback using public geolocation services

This enables location-aware image datasets for AI applications.

---

# 🎯 Use Cases

* Computer Vision Dataset Creation
* AI Model Training
* Object Detection
* Agricultural Image Annotation
* Wildlife Monitoring
* Medical Image Classification
* Educational Projects
* Research and Data Collection

---

# 📦 Dependencies

* Streamlit
* Pillow
* Pandas
* Plotly
* Requests
* OpenPyXL

---

# 📄 License

This project is distributed under the MIT License.

See the `LICENSE` file for details.

---

# 👨‍💻 Future Improvements

* Cloud storage integration
* Team collaboration
* Role-based access control
* Image segmentation tools
* AI-assisted labeling
* REST API
* Dark mode
* Bulk image upload
* Dataset versioning
* YOLO/COCO export support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📧 Contact

For questions, suggestions, or contributions, feel free to open an issue or submit a pull request.

---

## ⭐ If you find this project useful, consider giving it a star on GitHub!
