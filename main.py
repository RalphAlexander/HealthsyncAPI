import os
import sys
import psycopg2
import get_API
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
            records = get_API.get_medical_records(patient_num, cursor)
            for record in records:
                print(record);
            
            if len(records) == 0:
                print("Patient has no medical record")

        elif (len(sys.argv) == 3 and sys.argv[1] == "view_current_prescriptions"):
            patient_num = sys.argv[2]
            prescriptions = get_API.view_current_prescriptions(patient_num, cursor)
            for prescription in prescriptions:
                print(prescription);
            
            if len(prescriptions) == 0:
                print("Patient has no current prescriptions")
        else:
            print("invalid function or parameters")
        
        cursor.close()
        conn.close()


    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    
if __name__ == "__main__":
    main()