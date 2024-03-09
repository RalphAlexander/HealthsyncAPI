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

        # get medical records 
        if (len(sys.argv) == 3 and sys.argv[1] == "get_medical_records"):
            patient_num = sys.argv[2]
            records = get_API.get_medical_records(patient_num, cursor)
            print("\n--| Patient Number | Medical Record Num | Appointment Number | Date | Record |--")
            for record in records:
                print(record);
            print("\n")
            
            if len(records) == 0:
                print("Patient has no medical record")

        # view current prescriptions
        elif (len(sys.argv) == 3 and sys.argv[1] == "view_current_prescriptions"):
            patient_num = sys.argv[2]
            prescriptions = get_API.view_current_prescriptions(patient_num, cursor)
            print("\n--| Medication Name | Dose in Milligrams | Frequency | End Date |--")
            for prescription in prescriptions:
                print(prescription);
            print("\n")
            
            if len(prescriptions) == 0:
                print("Patient has no current prescriptions")

        # view all prescriptions
        elif (len(sys.argv) == 3 and sys.argv[1] == "view_all_prescriptions"):
            patient_num = sys.argv[2]
            prescriptions = get_API.view_all_prescriptions(patient_num, cursor)
            print("\n--| Medication Name | Dose in Milligrams | Frequency | End Date |--")
            for prescription in prescriptions:
                print(prescription);
            print("\n")
            
            if len(prescriptions) == 0:
                print("Patient has no prescriptions")
        
        # view patient info
        elif (len(sys.argv) == 3 and sys.argv[1] == "view_patient_info"):
            patient_num = sys.argv[2]
            patientinfo = get_API.view_patient_info(patient_num, cursor)
            print("\n--| First Name | Last Name | Email | Phone | Sex | Date of Birth | Address 1 | Address 2 | Postal Code | City | State Abbreviation |--")
            for patientinfostuff in patientinfo:
                print(patientinfostuff);
            print("\n")
            
            if len(patientinfo) == 0:
                print("Patient has no info")

        # list all titles
        elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_titles"):
            titles = get_API.list_all_titles(cursor)
            print("\n--| Title Abbreviation | Title Name |--")
            for title in titles:
                print(title);
            print("\n")
            
            if len(titles) == 0:
                print("There are no current titles")

        # list all specialties
        elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_specialties"):
            specialties = get_API.list_all_specialties(cursor)
            print("\n--| Specialty Abbreviation | Specialty Name |--")
            for specialty in specialties:
                print(specialty);
            print("\n")
            
            if len(specialties) == 0:
                print("There are no current specialties")

        # list all departments
        elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_departments"):
            departments = get_API.list_all_departments(cursor)
            print("\n--| Department Abbreviation | Department Name | Check In Office Building | Check In Office Room Number |--")
            for department in departments:
                print(department);
            print("\n")
            
            if len(departments) == 0:
                print("There are no current departments")

        # list all check in offices
        elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_checkinoffices"):
            checkinoffices = get_API.list_all_checkinoffices(cursor)
            print("\n--| Check In Office Building | Check In Office Room Number |--")
            for checkinoffice in checkinoffices:
                print(checkinoffice);
            print("\n")
            
            if len(checkinoffices) == 0:
                print("There are no current checkinoffices")

        # list all check in employees
        elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_employees"):
            employees = get_API.list_all_employees(cursor)
            print("\n--| First Name | Last Name | Employee Number | Title |--")
            for employee in employees:
                print(employee);
            print("\n")
            
            if len(employees) == 0:
                print("There are no current employees")

        # find employee/employees that match                       doesnt take third param but should
        elif (len(sys.argv) == 4 and sys.argv[1] == "find_employees"):
            first_name = sys.argv[2]
            last_name = sys.argv[3]
            records = get_API.find_employees(first_name, last_name, cursor)
            print("\n--| First Name | Last Name | Employee Number | Title |--")
            for record in records:
                print(record);
            print("\n")
            
            if len(records) == 0:
                print("There are no employees that match")

        # find patients/patients that match                       doesnt take third param but should
        elif (len(sys.argv) == 4 and sys.argv[1] == "find_patients"):
            first_name = sys.argv[2]
            last_name = sys.argv[3]
            records = get_API.find_patients(first_name, last_name, cursor)
            print("\n--| First Name | Last Name | Patient Number | Date of Birth | First Address | City |--")
            for record in records:
                print(record);
            print("\n")
            
            if len(records) == 0:
                print("There are no patients that match")
        
        else:
            print("invalid function or parameters")
        
        cursor.close()
        conn.close()


    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    
if __name__ == "__main__":
    main()