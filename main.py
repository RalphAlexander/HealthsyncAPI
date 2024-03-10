import os
import sys
import psycopg2
from dotenv import load_dotenv
from employee_API.create import *
from employee_API.get import *
from employee_API.update import *
from patient_API.create import *
from patient_API.get import *
from patient_API.update import *

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
        if (len(sys.argv) == 3 and sys.argv[1] == "ViewMedicalRecordsByPatient"):
    

            # Join the command line arguments into a single string and then split by ", "
            parameters = sys.argv[2].split(", ")

            patient_num = parameters[0]
            startDate = None
            endDate = None
            if len(parameters) <= 2:
                startDate = parameters[1]
            if len(parameters) == 3:
                endDate = parameters[2]
            
            records = ViewMedicalRecordsByPatient(cursor, patient_num, startDate, endDate)
            print("\n--| Patient Number | Medical Record Num | Appointment Number | Date | Record |--")
            for record in records:
                print(record);
            print("\n")
            

        # view current prescriptions
        elif (len(sys.argv) == 3 and sys.argv[1] == "ViewCurrentPrescriptions"):
            patient_num = sys.argv[2]
            prescriptions = ViewCurrentPrescriptions(cursor, patient_num)
            print("\n--| Medication Name | Dose in Milligrams | Frequency | End Date |--")
            for prescription in prescriptions:
                print(prescription);
            print("\n")
            
            if len(prescriptions) == 0:
                print("Patient has no current prescriptions")

        # view all prescriptions
        elif (len(sys.argv) == 3 and sys.argv[1] == "ViewAllPrescription"):
            patient_num = sys.argv[2]
            prescriptions = ViewAllPrescription(cursor, patient_num)
            print("\n--| Medication Name | Dose in Milligrams | Frequency | End Date |--")
            for prescription in prescriptions:
                print(prescription);
            print("\n")
            
            if len(prescriptions) == 0:
                print("Patient has no prescriptions")
        
        # view patient info
        elif (len(sys.argv) == 3 and sys.argv[1] == "ViewPatientInfo"):
            patient_num = sys.argv[2]
            patientinfo = ViewPatientInfo(cursor, patient_num)
            print("\n--| First Name | Last Name | Email | Phone | Sex | Date of Birth | Address 1 | Address 2 | Postal Code | City | State Abbreviation |--")
            for patientinfostuff in patientinfo:
                print(patientinfostuff);
            print("\n")
            
            if len(patientinfo) == 0:
                print("Patient has no info")

        # view patients future appointments
        elif (len(sys.argv) == 3 and sys.argv[1] == "ViewFutureAppt"):
            patient_num = sys.argv[2]
            patientinfo = ViewFutureAppt(cursor, patient_num)
            print("\n--| Appointment Number | Check In Building | Check In Room Number | Date | Duration | Purpose | Provider First Name | Provider Last Name | Provider Number |--")
            for patientinfostuff in patientinfo:
                print(patientinfostuff);
            print("\n")
            
            if len(patientinfo) == 0:
                print("Patient has no info")

        # view providers appointments
        elif (len(sys.argv) >= 3 and sys.argv[1] == "ViewProviderAppt"):
            parameters = sys.argv[2:]
            employee_num = parameters[0]
            date = None
            if len(parameters) == 2:
                date = parameters[1]
            providerAppts = ViewProviderAppt(cursor, employee_num, date)
            print("\n--| Appointment Number | Patient First Name | Patient Last Name | Patient Number | Date | Duration | Purpose |--")

            if (providerAppts is None):
                print("Provider has no Appointments\n")
                return
            
            for providerAppt in providerAppts:
                print(providerAppt);
            print("\n")


        # list all titles
        elif (len(sys.argv) == 2 and sys.argv[1] == "ListAllTitles"):
            titles = ListAllTitles(cursor)
            print("\n--| Title Abbreviation | Title Name |--")
            for title in titles:
                print(title);
            print("\n")
            
            if len(titles) == 0:
                print("There are no current titles")

        # list all specialties
        elif (len(sys.argv) == 2 and sys.argv[1] == "ListAllSpecialties"):
            specialties = ListAllSpecialties(cursor)
            print("\n--| Specialty Abbreviation | Specialty Name |--")
            for specialty in specialties:
                print(specialty);
            print("\n")
            
            if len(specialties) == 0:
                print("There are no current specialties")

        # list all departments
        elif (len(sys.argv) == 2 and sys.argv[1] == "ListAllDepartments"):
            departments = ListAllDepartments(cursor)
            print("\n--| Department Abbreviation | Department Name | Check In Office Building | Check In Office Room Number |--")
            for department in departments:
                print(department);
            print("\n")
            
            if len(departments) == 0:
                print("There are no current departments")

        # # list all check in offices
        # elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_checkinoffices"):
        #     checkinoffices = list_all_checkinoffices(cursor)
        #     print("\n--| Check In Office Building | Check In Office Room Number |--")
        #     for checkinoffice in checkinoffices:
        #         print(checkinoffice);
        #     print("\n")
            
        #     if len(checkinoffices) == 0:
        #         print("There are no current checkinoffices")

        # # list all check in employees
        # elif (len(sys.argv) == 2 and sys.argv[1] == "list_all_employees"):
        #     employees = list_all_employees(cursor)
        #     print("\n--| First Name | Last Name | Employee Number | Title |--")
        #     for employee in employees:
        #         print(employee);
        #     print("\n")
            
        #     if len(employees) == 0:
        #         print("There are no current employees")

        # find employee/employees that match                       doesnt take third param but should
        elif (len(sys.argv) == 4 and sys.argv[1] == "FindEmployee"):
            first_name = sys.argv[2]
            last_name = sys.argv[3]
            records = FindEmployee(cursor, first_name, last_name)
            print("\n--| First Name | Last Name | Employee Number | Title |--")
            for record in records:
                print(record);
            print("\n")
            
            if len(records) == 0:
                print("There are no employees that match")

        # find patients/patients that match                       doesnt take third param but should
        elif (len(sys.argv) == 4 and sys.argv[1] == "FindPatient"):
            first_name = sys.argv[2]
            last_name = sys.argv[3]
            records = FindPatient(cursor,first_name, last_name)
            print("\n--| First Name | Last Name | Patient Number | Date of Birth | First Address | City |--")
            for record in records:
                print(record);
            print("\n")
            
            if len(records) == 0:
                print("There are no patients that match")
        
        elif (len(sys.argv) == 3 and sys.argv[1] == "AddAddress"):
            raw_parameters = sys.argv[2].split(", ")
            # Convert 'None' string to None type
            parameters = [None if param == 'None' else param for param in raw_parameters]
            patientNum, city, stateAbbreviation, address1 = parameters[0:4]
            address2 = None
            postalCode = None
            if len(parameters) == 5:
                address2 = parameters[4]
            if len(parameters) == 6:
                postalCode = parameters[5]
            # TODO:DEBUG
            # print({"patientNum: ":patientNum,"city: ": city, "stateAbbreviation: " : stateAbbreviation, "address1: ":address1, "address2:":address2, "postalCode:":postalCode})
            isSuccessful = AddAddress(cursor, conn, patientNum, city, stateAbbreviation, address1, address2, postalCode)
            if isSuccessful:
                print("Address added successfully")
                return
            print("Address failed to be added")
            return
        
        else:
            print("invalid function or parameters")
        
        cursor.close()
        conn.close()


    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    
if __name__ == "__main__":
    main()