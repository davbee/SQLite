import sqlite3
import csv
# from datetime import datetime


def create_test_results_db(db_name="test_results.db"):
    """Create a SQLite database for storing recurrent test results."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

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

    cursor.execute(
        """
    CREATE INDEX IF NOT EXISTS idx_test_number_date ON test_results (test_number, test_date)
    """
    )

    conn.commit()
    conn.close()

    print(f"Database '{db_name}' with test_results table is ready.")


def import_from_csv(csv_file, db_name="test_results.db"):
    """
    Import test results from a CSV file into the database.

    CSV format expected:
    test_date,test_time,test_number,lower_spec_limit,upper_spec_limit,measurement_value,pass_fail
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        with open(csv_file, "r") as file:
            # Read CSV file
            csv_reader = csv.DictReader(file)

            # Prepare data for insertion
            records = []
            for row in csv_reader:
                records.append(
                    (
                        row["test_date"],
                        row["test_time"],
                        row["test_number"],
                        (
                            float(row["lower_spec_limit"])
                            if row["lower_spec_limit"]
                            else None
                        ),
                        (
                            float(row["upper_spec_limit"])
                            if row["upper_spec_limit"]
                            else None
                        ),
                        float(row["measurement_value"]),
                        row["pass_fail"].upper(),
                    )
                )

            # Insert data in bulk
            cursor.executemany(
                """
            INSERT OR IGNORE INTO test_results 
            (test_date, test_time, test_number, lower_spec_limit, upper_spec_limit, 
             measurement_value, pass_fail)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                records,
            )

            conn.commit()
            print(f"Successfully imported {len(records)} test records from {csv_file}")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except KeyError as e:
        print(f"Error: Missing required column in CSV file - {e}")
    except ValueError as e:
        print(f"Error: Invalid data format in CSV file - {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def export_to_csv(csv_file, db_name="test_results.db"):
    """Export all test results from database to a CSV file."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
        SELECT test_date, test_time, test_number, lower_spec_limit, 
               upper_spec_limit, measurement_value, pass_fail
        FROM test_results
        ORDER BY test_date, test_time
        """
        )

        with open(csv_file, "w", newline="") as file:
            csv_writer = csv.writer(file)

            # Write header
            csv_writer.writerow(
                [
                    "test_date",
                    "test_time",
                    "test_number",
                    "lower_spec_limit",
                    "upper_spec_limit",
                    "measurement_value",
                    "pass_fail",
                ]
            )

            # Write data
            csv_writer.writerows(cursor.fetchall())

        print(f"Successfully exported data to {csv_file}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def generate_sample_csv(csv_file="sample_test_results.csv"):
    """Generate a sample CSV file with test data."""
    sample_data = [
        [
            "test_date",
            "test_time",
            "test_number",
            "lower_spec_limit",
            "upper_spec_limit",
            "measurement_value",
            "pass_fail",
        ],
        ["2023-05-01", "08:30:00", "TEST-001", "10.0", "20.0", "15.5", "PASS"],
        ["2023-05-01", "09:15:00", "TEST-002", "5.0", "15.0", "12.3", "PASS"],
        ["2023-05-02", "10:00:00", "TEST-001", "10.0", "20.0", "21.2", "FAIL"],
        ["2023-05-02", "11:30:00", "TEST-003", "100.0", "200.0", "150.0", "PASS"],
        ["2023-05-03", "14:45:00", "TEST-002", "5.0", "15.0", "4.9", "FAIL"],
    ]

    with open(csv_file, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(sample_data)

    print(f"Sample CSV file '{csv_file}' created.")


if __name__ == "__main__":
    # Create the database
    create_test_results_db()

    # Generate a sample CSV file (for demonstration)
    sample_csv = "sample_test_results.csv"
    generate_sample_csv(sample_csv)

    # Import from CSV
    import_from_csv(sample_csv)

    # Export to CSV (to verify)
    export_csv = "exported_test_results.csv"
    export_to_csv(export_csv)

    print("\nYou can now:")
    print(f"1. Edit '{sample_csv}' with your actual test data")
    print(f"2. Run this script again to import your data")
    print(f"3. Or use the import_from_csv() function with your own CSV file")
