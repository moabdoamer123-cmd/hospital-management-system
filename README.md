# 🏥 Hospital Management System (HMS)

A comprehensive **database-driven desktop application** that streamlines hospital operations — managing patient records, doctor appointments, medical records, and billing — built with a fully normalized PostgreSQL backend and an interactive Python GUI.

> University Database Course Project — Innovation University, 2026.

---

## 📌 Project Overview

The system simulates a real hospital environment where different staff roles (Admin, Doctor, Nurse, Receptionist) each have their own dashboard with authorized actions. The architecture cleanly separates the database layer from the application layer for maintainability and data integrity.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **PostgreSQL** | Relational database backend |
| **Python** | Application logic |
| **Tkinter** | Desktop GUI framework |
| **psycopg2** | Python-PostgreSQL database adapter |

---

## 🗄️ Database Schema

The system is built on **8 fully normalized tables**:

```
Users              — Authentication + Role-based access control
├── Doctor         — Doctor profiles linked to Users and Departments  
├── Department     — Hospital departments with locations
├── Patient        — Patient demographics and contact info
│   ├── Appointment    — Links Patient ↔ Doctor with date/time
│   ├── Medical_Record — Diagnosis and treatment history per patient
│   └── Bill           — Billing records with payment tracking
└── Schedule       — Doctor availability by day and time
```

### Key Design Decisions
- **Unified Users table** with a `Role` check constraint (`Admin`, `Doctor`, `Nurse`, `Receptionist`) — avoids redundant lookup tables
- **Strict foreign key enforcement** with `ON DELETE CASCADE` and `ON DELETE SET NULL` where appropriate
- **Domain constraints** on email format, positive billing amounts, phone number length, and valid work days
- **`Patient_Billing_Summary` VIEW** for real-time reporting without repeated JOINs

---

## ✨ Features

### 🔐 Role-Based Access Control
Each user logs in and gets a dynamic dashboard based on their role:

| Role | Authorized Actions |
|------|--------------------|
| **Admin** | Full access — patients, doctors, appointments, bills, departments |
| **Doctor** | Own appointments, add medical records, view patients |
| **Nurse** | View patients, daily appointments, department locations |
| **Receptionist** | Book appointments, view patients and bills |

### 📅 Smart Appointment Scheduling
The most advanced feature in the system — instead of requiring rigid system IDs, the receptionist enters patient and doctor **names**:

1. System validates the doctor exists in the database
2. System searches for the patient by name + phone number
3. **If patient is new** → automatically registers them on the fly using a transactional `RETURNING patient_id` clause
4. Appointment is booked seamlessly in one workflow

### 📊 SQL Features Implemented
- `JOIN` queries across multiple tables (Patient, Doctor, Department, Appointment)
- `GROUP BY` + `HAVING` for spending analysis
- `Subquery` for filtered lookups (e.g., Cardiology patients)
- `ORDER BY` + `LIMIT` for top-performing doctors
- `CREATE VIEW` for Patient Billing Summary
- `ALTER TABLE` with `CHECK` constraints for data integrity
- `DML` operations: INSERT, UPDATE, DELETE with validation

---

## 🗂️ ERD

![ERD](https://github.com/user-attachments/assets/3104206a-233d-493b-a9d7-9db6608869e8)

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install psycopg2-binary
```

### Database Setup
```bash
# 1. Create the database
psql -U postgres -c "CREATE DATABASE HOSP_MS;"

# 2. Run the SQL schema and seed data
psql -U postgres -d HOSP_MS -f sql/Final_Hosp_MS_Sql.sql
```

### Run the Application
```bash
python interface.py
```

### Default Login (Admin)
```
Email:    mo.amer@hospital.com
Password: hashed_pass_123
```

> ⚠️ **Note:** Update `DB_PARAMS` in `interface.py` with your local PostgreSQL credentials before running.

---

## 📁 Project Structure

```
hospital-management-system/
│
├── interface.py                  # Python Tkinter GUI application
│
├── sql/
│   └── Final_Hosp_MS_Sql.sql    # Full schema + seed data + queries
│
├── docs/
│   ├── Final_ERD.png            # Entity Relationship Diagram
│   ├── Final_Schema_HOSP_MS.pdf # Relational schema
│   └── Database_Project_Proposal.docx
│
└── README.md
```

---

## 💡 What I Learned

- Designing a fully normalized relational database from scratch (ERD → Schema → SQL)
- Implementing role-based access control at the database and application level
- Writing advanced SQL: JOINs, subqueries, GROUP BY, HAVING, Views, and CHECK constraints
- Building a Python desktop GUI with Tkinter connected to a live PostgreSQL database
- Handling transactional logic (`RETURNING` clause for auto-registering new patients)

---

## 👥 Team

Developed as a university team project.

| Name | ID | Role |
|------|----|------|
| **Mohamed Abdelhameed Mohamed Amer** | 24030144 | Database Design, SQL, Python GUI |
| Mostafa Abdelkader Ibrahim | 24030097 | Team Member |
| Mostafa Ahmed Mohammed | 24030229 | Team Member |
| Eman Abdelmaboud Mohamed | 24030222 | Team Member |
| Rawan Omar Elsaid | 25030065 | Team Member |

---

## 📬 Contact

**Mohamed Amer**
- 📧 mo.abdo.amer123@gmail.com
- 💼 [LinkedIn](https://www.linkedin.com/in/mohamed-amer-217342376)
- 🐙 [GitHub](https://github.com/moabdoamer123-cmd)
