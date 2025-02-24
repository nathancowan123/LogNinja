# LogNinja
# LogNinja (VEV Version)

## 📌 Overview
LogNinja is a powerful NLP-based log analysis tool designed to help developers and system administrators monitor, analyze, and extract meaningful insights from log files using AI-driven models. This version runs in a **Python Virtual Environment (VEV)** instead of Docker.

## 🚀 Features
- **AI-Powered Log Parsing**: Uses NLP to categorize and analyze logs.
- **Custom Model Training**: Train your own models for log classification.
- **Interactive API**: Provides an API to interact with the log analysis engine.
- **Lightweight Setup**: Runs in a Python virtual environment (no need for Docker).

---

## 🔧 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nathancowan123/LogNinja.git
cd LogNinja
```

### **2️⃣ Set Up a Virtual Environment**
```bash
python -m venv venv
```

### **3️⃣ Activate the Virtual Environment**
- **Windows (PowerShell)**:
  ```powershell
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### **4️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### **Running the Application**
```bash
python run.py
```
This will start LogNinja’s API for processing logs.

### **Testing Log Analysis**
To generate test log analysis results, run:
```bash
python generate_ninja_logs.py
```

### **Training the NLP Model**
If you want to train a custom log analysis model, run:
```bash
python train_ninja_model.py
```
Ensure you have the necessary training data stored in:
```
app/data/
```

---

## 📂 Project Structure
```
LogNinja/
├── app/
│   ├── model/ninja_model/ (Contains AI model and tokenizer)
│   ├── routes/ (API blueprints)
│   ├── services/ (Log processing logic)
├── config/ (Configuration files)
├── logs/ (Generated logs)
├── venv/ (Virtual environment - ignored in Git)
├── .gitignore (Excludes unnecessary files)
├── requirements.txt (Dependencies)
├── run.py (Main entry point)
├── train_ninja_model.py (NLP model training script)
└── README.md
```

---

## 🔧 Troubleshooting

### **1️⃣ Virtual Environment Issues**
If you get a command not found error when activating the virtual environment:
```bash
source venv/bin/activate
```
Make sure you're in the **LogNinja** directory.

### **2️⃣ Missing Dependencies**
If dependencies fail to install, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **3️⃣ Model Not Found**
If LogNinja fails to load the model, ensure the trained model files exist in:
```
app/model/ninja_model/
```
If missing, retrain the model using:
```bash
python train_ninja_model.py
```

---

## 🤝 Contributing
Feel free to fork the project, submit issues, or contribute improvements!

---

## 📜 License
MIT License - You are free to use, modify, and distribute this software.

