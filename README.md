# 📌 Python Task API  

A simple **Task Management Application** that provides REST API endpoints to **create, edit, and delete tasks**.  

This project was built primarily to practice **CI/CD workflows** and **cloud deployment**.  

---

## 🔧 Features  
- REST API for managing tasks (CRUD operations)  
- Automated tests integrated into the pipeline  
- CI/CD pipeline using **GitHub Actions**  
- Secure deployment with environment secrets  
- Deployed on **Google Cloud Platform (GCP)**  

---

## 🚀 Tech Stack  
- **Python** (FastAPI / Flask / Django – specify which one you used)  
- **GitHub Actions** (CI/CD)  
- **Google Cloud Platform (GCP)** (deployment)  
- **Pytest** (testing)  

---

## 📌 Highlights  
- Implemented **CI/CD pipeline** with GitHub Actions  
- Automated tests run before deployment to ensure reliability  
- Secrets are securely stored and injected at runtime  
- Application successfully deployed on **GCP**  

---

## ▶️ Usage (API Examples)  

Here are some example API requests to interact with the Task API:  

### Create a Task  
```bash
curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn CI/CD", "description": "Practice GitHub Actions"}'
