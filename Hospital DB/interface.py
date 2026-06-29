import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

# --- إعدادات قاعدة البيانات ---
DB_PARAMS = {
    "host": "localhost",
    "database": "HOSP_MS",  
    "user": "postgres",
    "password": "MY_DB_PASSWORD",
    "port": "5432"
}

# دالة تنفيذ الاستعلامات بعد تعديلها لتستقبل الـ RETURNING بنجاح
def execute_query(query, params=None, fetch=False):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(query, params)
        
        # ذكاء إضافي: لو الاستعلام يحتوي على RETURNING أو تم طلب fetch صراحة
        if fetch or "returning" in query.lower():
            result = cur.fetchall()
            conn.commit() # الحفظ مهم جداً حتى مع جلب البيانات في الـ Insert
        else:
            conn.commit()
            result = None
            
        cur.close()
        conn.close()
        return result
    except Exception as e:
        messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
        return None

class HospitalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System - Mohamed Amer & Team")
        self.root.geometry("1000x700")
        self.current_user = None
        self.show_login()
        self.root.mainloop()

    def show_login(self):
        for widget in self.root.winfo_children(): widget.destroy()
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="تسجيل الدخول", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(frame, text="البريد الإلكتروني:").pack()
        self.email_entry = tk.Entry(frame, width=35)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "mo.amer@hospital.com")

        tk.Label(frame, text="كلمة المرور:").pack()
        self.pass_entry = tk.Entry(frame, width=35, show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "hashed_pass_123")

        tk.Button(frame, text="دخول", bg='#27ae60', fg='white', width=15, command=self.login).pack(pady=20)

    def login(self):
        email = self.email_entry.get().strip()
        pw = self.pass_entry.get().strip()
        
        query = """
            SELECT user_id, name, role
            FROM users
            WHERE email = %s AND password = %s
        """
        res = execute_query(query, (email, pw), fetch=True)
        
        if res:
            self.current_user = {
                'id': res[0][0], 
                'name': res[0][1], 
                'role': res[0][2]
            }
            self.show_main()
        else:
            messagebox.showerror("خطأ", "بيانات الدخول غير صحيحة")

    def show_main(self):
        for widget in self.root.winfo_children(): widget.destroy()
        
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill='x')
        
        user_info = f"مرحباً: {self.current_user['name']} | الرتبة: {self.current_user['role']}"
        tk.Label(header, text=user_info, fg='white', bg='#2c3e50', font=("Arial", 12)).pack(side='right', padx=20)
        
        tk.Button(header, text="تسجيل خروج", command=self.show_login, bg='#e74c3c', fg='white').pack(side='left', padx=20, pady=15)

        self.content = tk.Frame(self.root)
        self.content.pack(pady=30)

        role = self.current_user['role']

        if role == 'Admin':
            self.add_menu_button("إدارة المرضى (Patients)", self.view_patients)
            self.add_menu_button("إدارة الأطباء (Doctors)", self.view_doctors)
            self.add_menu_button("عرض الفواتير (Bills)", self.view_bills)
            self.add_menu_button("سجل المواعيد (Appointments)", self.view_appointments)
            self.add_menu_button("إضافة موعد جديد", self.add_appointment)
            self.add_menu_button("أقسام المستشفى (Departments)", self.view_departments)

        elif role == 'Doctor':
            self.add_menu_button("مواعيدي اليوم", self.view_doctor_appointments)
            self.add_menu_button("إضافة سجل طبي", self.add_medical_record)
            self.add_menu_button("قائمة المرضى", self.view_patients)

        elif role == 'Nurse':
            self.add_menu_button("عرض قائمة المرضى", self.view_patients)
            self.add_menu_button("عرض المواعيد اليومية", self.view_appointments)
            self.add_menu_button("أماكن الأقسام", self.view_departments)

        elif role == 'Receptionist':
            self.add_menu_button("عرض المواعيد", self.view_appointments)
            self.add_menu_button("إضافة موعد جديد", self.add_appointment)
            self.add_menu_button("عرض المرضى", self.view_patients)
            self.add_menu_button("عرض الفواتير", self.view_bills)

    def add_menu_button(self, text, command):
        tk.Button(self.content, text=text, width=35, height=2, font=("Arial", 11), command=command).pack(pady=10)

    def view_patients(self):
        rows = execute_query('SELECT patient_id, first_name, last_name, phone_number FROM patient', fetch=True)
        self.show_table_window(["ID", "First Name", "Last Name", "Phone"], rows)

    def view_doctors(self):
        rows = execute_query('SELECT doctor_id, name, specialization FROM doctor', fetch=True)
        self.show_table_window(["ID", "Name", "Specialization"], rows)

    def view_bills(self):
        rows = execute_query('SELECT bill_id, total_amount, payment_data, patient_id FROM bill', fetch=True)
        self.show_table_window(["Bill ID", "Amount", "Date", "Patient ID"], rows)

    def view_appointments(self):
        query = """
            SELECT a.appointment_id, p.first_name, d.name, a.date, a.time
            FROM appointment a
            JOIN patient p ON a.patient_id = p.patient_id
            JOIN doctor d ON a.doctor_id = d.doctor_id
        """
        rows = execute_query(query, fetch=True)
        self.show_table_window(["ID", "Patient", "Doctor", "Date", "Time"], rows)

    def view_departments(self):
        rows = execute_query('SELECT dept_id, dept_name, location FROM department', fetch=True)
        self.show_table_window(["ID", "Dept Name", "Location"], rows)

    def view_doctor_appointments(self):
        query = """
            SELECT a.time, p.first_name, p.last_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.patient_id
            JOIN doctor d ON a.doctor_id = d.doctor_id
            WHERE d.user_id = %s
        """
        rows = execute_query(query, (self.current_user['id'],), fetch=True)
        self.show_table_window(["Time", "Patient First Name", "Last Name"], rows)

    def add_medical_record(self):
        pid = simpledialog.askinteger("إضافة", "أدخل رقم المريض (Patient ID):")
        diag = simpledialog.askstring("إضافة", "التشخيص (Diagnosis):")
        treat = simpledialog.askstring("إضافة", "العلاج (Treatment):")
        
        if pid and diag:
            query = 'INSERT INTO medical_record (diagnosis, treatment, record_date, patient_id) VALUES (%s, %s, CURRENT_DATE, %s)'
            execute_query(query, (diag, treat, pid))
            messagebox.showinfo("نجاح", "تمت إضافة السجل الطبي")

    def add_appointment(self):
        p_first = simpledialog.askstring("حجز موعد", "اسم المريض الأول (First Name):")
        p_last = simpledialog.askstring("حجز موعد", "اسم المريض الأخير (Last Name):")
        p_phone = simpledialog.askstring("حجز موعد", "رقم تليفون المريض (Phone Number):")
        
        d_name = simpledialog.askstring("حجز موعد", "اسم الطبيب (Doctor Name):")
        a_date = simpledialog.askstring("حجز موعد", "التاريخ (YYYY-MM-DD):")
        a_time = simpledialog.askstring("حجز موعد", "الوقت (HH:MM:SS):")
        
        if p_first and p_last and p_phone and d_name and a_date and a_time:
            
            # 1. التحقق من الطبيب
            d_query = "SELECT doctor_id FROM doctor WHERE LOWER(name) = LOWER(%s) LIMIT 1"
            d_res = execute_query(d_query, (d_name.strip(),), fetch=True)
            
            if not d_res:
                messagebox.showerror("خطأ", f"الطبيب '{d_name}' غير مسجل في النظام!")
                return
            doctor_id = d_res[0][0]

            # 2. البحث عن المريض ببيانات مؤكدة
            p_query = """
                SELECT patient_id FROM patient 
                WHERE LOWER(first_name) = LOWER(%s) AND LOWER(last_name) = LOWER(%s) AND phone_number = %s
                LIMIT 1
            """
            p_res = execute_query(p_query, (p_first.strip(), p_last.strip(), p_phone.strip()), fetch=True)
            
            is_new_patient = False
            
            if p_res:
                patient_id = p_res[0][0]
            else:
                # مريض جديد - هنا الـ RETURNING هتشتغل صح جداً بسبب تعديل دالة execute_query فوق
                insert_patient_query = """
                    INSERT INTO patient (first_name, last_name, phone_number, date_of_birth) 
                    VALUES (%s, %s, %s, '2000-01-01') 
                    RETURNING patient_id
                """
                new_p_res = execute_query(insert_patient_query, (p_first.strip(), p_last.strip(), p_phone.strip()))
                
                if new_p_res:
                    patient_id = new_p_res[0][0]
                    is_new_patient = True
                else:
                    messagebox.showerror("خطأ", "فشل تسجيل المريض الجديد في قاعدة البيانات.")
                    return

            # 3. تسجيل الموعد النهائي
            insert_app_query = """
                INSERT INTO appointment (date, time, patient_id, doctor_id) 
                VALUES (%s, %s, %s, %s)
            """
            execute_query(insert_app_query, (a_date, a_time, patient_id, doctor_id))
            
            if is_new_patient:
                messagebox.showinfo("نجاح", f"تم تسجيل المريض الجديد '{p_first} {p_last}' وحجز موعده بكفاءة!")
            else:
                messagebox.showinfo("نجاح", f"تم حجز الموعد بنجاح للمريض الحالي '{p_first} {p_last}'.")

    def show_table_window(self, cols, rows):
        win = tk.Toplevel(self.root)
        win.title("بيانات النظام")
        win.geometry("800x400")
        tree = ttk.Treeview(win, columns=cols, show='headings')
        for c in cols: 
            tree.heading(c, text=c)
            tree.column(c, width=150)
        if rows:
            for r in rows: tree.insert('', 'end', values=r)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    HospitalApp()
