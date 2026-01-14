import sqlite3

# Connecting to your existing database
conn = sqlite3.connect("job_applications.db")
cursor = conn.cursor()

# List of new columns to add
new_columns = {
    "job_source": "TEXT",
    "notes": "TEXT",
    "last_updated": "TEXT"
}

# Adding each column only if it doesn’t already exist
for column_name, column_type in new_columns.items():
    try:
        cursor.execute(f"ALTER TABLE applications ADD COLUMN {column_name} {column_type}")
        print(f"✅ Added column: {column_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"⚠️ Column '{column_name}' already exists. Skipping.")
        else:
            print(f"❌ Error adding column {column_name}: {e}")

# Commit and close
conn.commit()
conn.close()

print("\n🎉 Table updated successfully!")
