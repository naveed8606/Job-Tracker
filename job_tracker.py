import sqlite3
from datetime import datetime
from prettytable import PrettyTable

# -------------------- DATABASE SETUP --------------------
def initialize_database():
    """Create database and table if not exists."""
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL,
        date_applied TEXT,
        recruiter_reply_date TEXT,
        status TEXT,
        stage TEXT,
        job_source TEXT,
        notes TEXT,
        last_updated TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database and table are ready!")


# -------------------- ADD APPLICATION --------------------
def add_application():
    """Add a new job application."""
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()

    print("\n=== Add New Job Application ===")
    company = input("Company name: ")
    position = input("Position title: ")
    salary = input("Salary (leave blank if unknown): ")
    date_applied = input("Date applied (YYYY-MM-DD): ")
    job_source = input("Job source (LinkedIn, Indeed, etc.): ")
    notes = input("Any notes (optional): ")

    # Default values
    recruiter_reply_date = None
    status = "Applied"
    stage = None
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO applications 
        (company_name, position, salary, date_applied, recruiter_reply_date, status, stage, job_source, notes, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, position, salary if salary else None, date_applied,
          recruiter_reply_date, status, stage, job_source, notes, last_updated))

    conn.commit()
    conn.close()
    print(f"\n✅ Application for {position} at {company} added successfully!\n")


# -------------------- VIEW APPLICATIONS --------------------
def view_applications():
    """Display all job applications."""
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\n📭 No job applications found.\n")
        return

    table = PrettyTable()
    table.field_names = [
        "ID", "Company", "Position", "Salary", "Date Applied",
        "Reply Date", "Status", "Stage", "Source", "Notes", "Last Updated"
    ]

    for row in rows:
        table.add_row(row)

    print("\n=== Job Applications Tracker ===")
    print(table)
    print()

def delete_application():
    """Delete a job application by its ID."""
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()

    view_applications()  # Show the table first so user can see IDs
    app_id = input("Enter the ID of the application to delete: ")

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete application ID {app_id}? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Deletion cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("⚠️ No application found with that ID.")
    else:
        print(f"✅ Application ID {app_id} deleted successfully!")

    conn.close()

def update_application():
    """Update status or stage of a job application."""
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()

    view_applications()  # Show all records
    app_id = input("Enter the ID of the application to update: ")

    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    record = cursor.fetchone()

    if not record:
        print("⚠️ No application found with that ID.")
        conn.close()
        return

    print(f"\nCurrent status: {record[6]}")
    print("Available statuses: Applied / Interview / Selected / Rejected")

    new_status = input("Enter new status: ").capitalize()

    # Optional stage update if interview or selected
    new_stage = None
    if new_status in ["Interview", "Selected"]:
        new_stage = input("Enter stage (e.g., Technical, HR, Final): ")

    # Optional recruiter reply date
    recruiter_reply = input("Enter recruiter reply date (YYYY-MM-DD or leave blank): ") or None

    from datetime import datetime
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE applications 
        SET status = ?, stage = ?, recruiter_reply_date = ?, last_updated = ?
        WHERE id = ?
    """, (new_status, new_stage, recruiter_reply, last_updated, app_id))

    conn.commit()
    conn.close()
    print(f"✅ Application ID {app_id} updated successfully!\n")




# -------------------- MAIN MENU --------------------
if __name__ == "__main__":
    initialize_database()

    while True:
        print("\n1️⃣ Add new application")
        print("2️⃣ View all applications")
        print("3️⃣ Update application status")
        print("4️⃣ Delete an application")
        print("5️⃣ Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_application()
        elif choice == "4":
            delete_application()
        elif choice == "5":
            print("\n👋 Exiting... Goodbye!")
            break
        else:
            print("\n❌ Invalid choice, try again.")
