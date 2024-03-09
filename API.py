import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    conn_params = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        if (len(sys.argv) == 3 and sys.argv[1] == "get_medical_records"):
            patient_num = sys.argv[2]
            records = get_medical_records(patient_num, cursor)
            for record in records:
                print(record);
            
            if len(records) == 0:
                print("Patient has no medical record")
        else:
            print("invalid function or parameters")
        
        cursor.close()
        conn.close()


    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")


def get_medical_records(patient_num, cursor):
    try:
        query = """
        SELECT mr.*
        FROM medicalrecord mr 
        JOIN appointment a ON mr.appointmentid  = a.id
        JOIN patient p ON p.id = a.patientid
        WHERE p.patientnum = %s
        ORDER BY mr.date DESC;
        """
        cursor.execute(query, (patient_num,))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []
    
if __name__ == "__main__":
    main()