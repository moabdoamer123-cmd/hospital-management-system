# Hospital Management System (HMS)

A comprehensive, database-driven desktop application designed to streamline hospital operations, manage patient records, coordinate doctor appointments, and handle billing processes efficiently. 

This project integrates a robust relational database backend with an interactive Python-based graphical user interface (GUI).

---

## 🏛️ Project Architecture & Components

The system is built using a modern decoupled architecture to ensure data integrity and user authorization control:

### 1. Database Layer (PostgreSQL Backend)
A fully normalized relational database schema comprising core operational entities:
* **Users & Role-based Access Control:** Unified `Users` table with a string-based `Role` check constraint (`Admin`, `Doctor`, `Nurse`, `Receptionist`) to handle system authentication securely without redundant lookup tables.
* **Medical & Administrative Data:** Independent transactional tables for `Patient`, `Doctor`, `Department`, `Appointment`, `Medical_Record`, `Bill`, and `Schedule`.
* **Data Integrity & Constraints:** Strict enforcement of foreign keys, domain constraints (e.g., proper email formatting, positive billing amounts, phone number length validation), and a dynamic `Patient_Billing_Summary` database view for real-time reporting.

### 2. Application Layer (Python & Tkinter UI)
An interactive graphical interface built using Python's `tkinter` and `psycopg2` database adapter:
* **Dynamic Role-based Dashboards:** Upon custom login validation, the interface dynamically morphs to present authorized actions depending on the logged-in user's role.
* **Smart Appointment Scheduling Workflow:** A real-world feature implemented within the *Receptionist* and *Admin* panels. Instead of relying on rigid system IDs, the clerk can insert appointments using patient and doctor names. The Python backend dynamically executes validation logic:
    * It queries the doctor’s record to confirm deployment.
    * It cross-references patient demographics; if the patient is a newcomer, it registers them on the fly using a transactional `RETURNING patient_id` clause, mapping the entire pipeline seamlessly into the `Appointment` table.

---

**Prepared by:**
- Mohamed Abdelhameed Mohamed Amer (ID: 24030144)
- Mostfa abdelkader ibrahim   24030097
- Mostafa Ahmed Mohammed   24030229
- Eman abdelmaboud Mohamed 24030222
- Rawan Omar Elsaid 25030065

