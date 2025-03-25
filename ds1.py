import sqlite3
from datetime import datetime


def create_test_results_db(db_name="test_results.db"):
    """Create a SQLite database for storing recurrent test results."""

    # Connect to SQLite database (will create if doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the test_results table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_date DATE NOT NULL,
        test_time TIME NOT NULL,
        test_number TEXT NOT NULL,
        lower_spec_limit REAL,
        upper_spec_limit REAL,
        measurement_value REAL NOT NULL,
        pass_fail TEXT NOT NULL CHECK (pass_fail IN ('PASS', 'FAIL')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(test_date, test_time, test_number)
    )
    """
    )

    # Create an index for faster queries by test number and date
    cursor.execute(
        """
    CREATE INDEX IF NOT EXISTS idx_test_number_date ON test_results (test_number, test_date)
    """
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Successfully created SQLite database '{db_name}' with test_results table.")


def generate_sample_data(db_name="test_results.db"):
    """Insert sample test data into the database."""

    sample_tests = [
        ("2023-05-01", "08:30:00", "TEST-001", 10.0, 20.0, 15.5, "PASS"),
        ("2023-05-01", "09:15:00", "TEST-002", 5.0, 15.0, 12.3, "PASS"),
        ("2023-05-02", "10:00:00", "TEST-001", 10.0, 20.0, 21.2, "FAIL"),
        ("2023-05-02", "11:30:00", "TEST-003", 100.0, 200.0, 150.0, "PASS"),
        ("2023-05-03", "14:45:00", "TEST-002", 5.0, 15.0, 4.9, "FAIL"),
    ]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.executemany(
        """
    INSERT INTO test_results 
    (test_date, test_time, test_number, lower_spec_limit, upper_spec_limit, measurement_value, pass_fail)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        sample_tests,
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(sample_tests)} sample test records.")


def generate_sql_code(db_name="test_results.db"):
    """Generate the SQL code that would create this database schema."""

    sql_code = """-- SQL Code to create test results database
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_date DATE NOT NULL,
    test_time TIME NOT NULL,
    test_number TEXT NOT NULL,
    lower_spec_limit REAL,
    upper_spec_limit REAL,
    measurement_value REAL NOT NULL,
    pass_fail TEXT NOT NULL CHECK (pass_fail IN ('PASS', 'FAIL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(test_date, test_time, test_number)
);

CREATE INDEX idx_test_number_date ON test_results (test_number, test_date);
"""
    return sql_code


if __name__ == "__main__":
    # Create the database and table
    create_test_results_db()

    # Insert some sample data
    generate_sample_data()

    # Generate and display the SQL code
    print("\nGenerated SQL Code:")
    print(generate_sql_code())
