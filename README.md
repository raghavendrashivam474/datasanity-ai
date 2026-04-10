# 🧹 DataSanity AI

**Intelligent CSV Data Cleaning for Medicine Datasets**

Transform messy medicine inventory data into clean, validated datasets in seconds.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🌐 **[🚀 TRY IT LIVE](https://datasanity-ai.onrender.com)** ← Click here!

> ⚠️ **Note:** Free tier may take 30 seconds to wake up after inactivity.

---

## ✨ Features

- 🧠 **Smart Column Detection** — Automatically identifies medicine names, prices, quantities, expiry dates
- ✨ **Typo Correction** — Fixes medicine name typos with 90%+ accuracy using fuzzy matching
- 💰 **Price Normalization** — Removes currency symbols, converts to numeric
- 🔄 **Duplicate Removal** — Identifies and removes exact duplicates
- ⚠️ **Data Validation** — Flags expired medicines, negative prices, missing fields
- 📊 **Quality Scoring** — Instant 0-100% data quality assessment
- 📑 **Excel Reports** — Comprehensive multi-sheet reports with before/after comparison
- 🎯 **Confidence Scores** — Shows match confidence for all automated corrections

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/datasanity-ai.git
cd datasanity-ai
Install dependencies
Bash

pip install -r requirements.txt
Run the server
Bash

python -m app.main
Open in browser
text

http://localhost:8001
📖 Usage
Web Interface
Upload your CSV file via drag-and-drop or file browser
Click "Clean My Data"
Review the changes and validation issues
Download cleaned CSV or full Excel report
API Usage
Clean Data:

Bash

curl -X POST "http://localhost:8001/clean-data" \
  -F "file=@your_data.csv"
Download Cleaned CSV:

Bash

curl -X POST "http://localhost:8001/clean-data/download" \
  -F "file=@your_data.csv" \
  --output cleaned_data.csv
Generate Excel Report:

Bash

curl -X POST "http://localhost:8001/clean-data/report" \
  -F "file=@your_data.csv" \
  --output report.xlsx
📊 Example
Input CSV:

csv

Medicine Name, Price, Quantity, Expiry Date
Paracetmol , ₹20, 100, 2025-06-01
crocin, 30, 50, 2024-12-15
, 50, 200, 2025-01-10
amoxicilin, abc, , 2025-08-14
Output:

✅ Fixed typo: Paracetmol → paracetamol
✅ Fixed typo: amoxicilin → amoxicillin
✅ Normalized price: ₹20 → 20
⚠️ Warning: Invalid price abc
⚠️ Warning: Missing medicine name (Row 3)
⚠️ Warning: Missing quantity (Row 4)
Quality Score: 85%

🏗️ Project Structure
text

datasanity-ai/
│
├── app/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   └── clean.py            # API endpoints
│   ├── services/
│   │   ├── cleaner.py          # Data cleaning logic
│   │   ├── validator.py        # Validation rules
│   │   ├── suggester.py        # Typo correction
│   │   ├── column_detector.py  # Smart column detection
│   │   └── report_generator.py # Excel report generation
│   └── utils/
│       └── file_handler.py     # CSV file handling
│
├── templates/
│   └── index.html              # Web interface
│
├── data/
│   └── sample.csv              # Sample test data
│
├── requirements.txt
├── .gitignore
└── README.md
🛠️ Technology Stack
Backend: FastAPI
Data Processing: Pandas
Fuzzy Matching: RapidFuzz
Excel Generation: OpenPyXL
Frontend: HTML5 + Vanilla JavaScript
📈 Roadmap
 User authentication and history
 Custom medicine dictionaries
 Batch file processing
 API rate limiting
 Docker deployment
 Cloud storage integration
 Scheduled cleaning jobs
 ML-based anomaly detection
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Raghavendra Singh

GitHub: @raghavendrashivam474
LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/raghavendra-singh-2335292ab/)
🙏 Acknowledgments
Medicine dictionary compiled from FDA and WHO databases
Inspired by real-world pharmacy data challenges
Built with ❤️ for healthcare professionals
📞 Support
For support, email raghavendrashivam474@gmail.com or open an issue on GitHub.

⭐ Show Your Support
Give a ⭐️ if this project helped you!

Made with ❤️ by Raghu
