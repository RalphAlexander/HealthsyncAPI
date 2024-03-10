import os
import sys
import psycopg2
from dotenv import load_dotenv
import employee_API.get as eget
import employee_API.create as ecreate
import employee_API.update as eupdate
import patient_API.get as pget
import patient_API.create as pcreate
import patient_API.update as pupdate


#--- provider functions ---
def ViewProvider():
    print("View Provider")
    print("Enter a department abbreviation to filter by (optional)")
    dept = input()
    print("Enter a specialty abbreviation to filter by (optional)")
    specialty = input()
    print("Enter a provider title to filter by (optional)")
    title = input()
    out = pget.ViewProvider(cursor, dept, specialty, title)
    #TODO implement printing out

def CreateHealthCareProvider():
    print("Create Healthcare Provider")
    print("Enter a first name")
    fname = input()
    print("Enter a last name")
    lname = input()
    print("Enter a title abbreviation")
    title = input()
    print("Enter a department abbreviation")
    dept = input()
    print("Enter a specialty")
    special = input()
    out = ecreate.CreateHealthCareProvider(cursor, fname, lname, title, dept, special)
    #TODO implement printing out

def EditHealthcareProvider():
    print("Edit Healthcare provider")
    print("Enter employee number")
    employee_num = input()
    print("Enter new title (optional)")
    title = input()
    print("Enter new first name (optional)")
    fname = input()
    print("Enter new last name (optional)")
    lname = input()
    print("Enter new department abbreviation (optional)")
    dept = input()
    out = eupdate.EditHealthcareProvider(cursor, employee_num, title, fname, lname, dept)
     #TODO implement printing out

def EditSpecialty():
    print("Edit specialty")
    print("Enter employee number")
    employee_num = input()
    print("Enter specialty")
    specialty = input()
    out = eupdate.EditSpecialty(cursor, employee_num, specialty)
    #TODO implement printing out

def FindEmployee():
    print("Find employee")
    print("Enter first name")
    fname = input()
    print("Enter last name")
    lname = input()
    print("Enter title abbreviation (optional)")
    title = input()
    out = pget.FindEmployee(cursor, fname, lname, title)
    #TODO implement printing out

def ChangeEmploymentStatus():
    print("Change employment status")
    print("Enter employee number")
    employee_num = input()
    out = eupdate.ChangeEmploymentStatus(cursor, employee_num)
    #TODO implement printing out

def ListAllSpecialties():
    print("List all specialties")
    out = pget.ListAllSpecialties(cursor)
    #TODO implement printing out

def ListAllTitles():
    print("List all titles")
    out = pget.ListAllTitles(cursor)
    #TODO implement printing out

def ListAllDepartments():
    print("List all departments")
    out = pget.ListAllDepartments(cursor)
    #TODO implement printing out

#--- schedule functions ---
def CreateShift():
    print("Create shift")
    print("Enter employee number")
    employee_num = input()
    print("Enter shift start date (yyyy-mm-dd)")
    date = input()
    print("Enter shift start time in 24 hour format (hh:mm)")
    time = input()
    print("Enter shift end date (yyyy-mm-dd)")
    edate = input()
    print("Enter shift end time in 24 hour format (hh:mm)")
    etime = input()
    out = eupdate.CreateShift(cursor, employee_num, date + " " + time, edate + " " + etime)
    #TODO implement printing out

def CancelShift():
    print("Cancel shift")
    print("Enter employee number")
    employee_num = input()
    print("Enter shift start date (yyyy-mm-dd)")
    date = input()
    print("Enter shift start time in 24 hour format (hh:mm)")
    time = input()
    out = eupdate.CancelShift(cursor, employee_num, date + " " + time)
    #TODO implement printing out

def FindPatient():
    print("Find patient")
    print("Enter first name")
    fname = input()
    print("Enter last name")
    lname = input()
    print("Enter birthday (yyyy-mm-dd)")
    bday = input()
    out = eget.FindPatient(cursor, fname, last_name, bday)
    #TODO implement printing out

def ViewPatientInfo():
    print("View patient info")
    print("Enter patient number")
    pt_num = input()
    out = eget.ViewPatientInfo(cursor, pt_num)
    #TODO implement printing out

def CreatePatient():
    print("Create patient")
    print("Enter first name")
    fname = input()
    print("Enter last name")
    lname = input()
    print("Enter email (optional)")
    email = input()
    print("Enter phone number (digits only. i.e. 1234567890) (optional)")
    phone = input()
    print("Enter sex (m or f)")
    sex = input()
    print("Enter birthday (yyyy-mm-dd)")
    bday = input()
    print("Enter street address")
    street = input()
    print("Enter unit number (optional)")
    street2 = input()
    print("Enter postal code (optional)")
    post = input()
    print("Enter city")
    city = input()
    print("Enter state abbreviation (CO, NY, WA, etc.)")
    state = input()
    out = ecreate.CreatePatient(cursor, fname, lname, email, phone, sex, bday, street, street2, post, city, state)
    #TODO implement printing out

def EditPatient():
    print("Edit patient")
    print("Enter patient number")
    pt_num = input()
    print("Enter new first name (optional)")
    fname = input()
    print("Enter new last name (optional)")
    lname = input()
    print("Enter new email (optional)")
    email = input()
    print("Enter new phone number (digits only. i.e. 1234567890) (optional)")
    phone = input()
    out = pupdate.EditPatient(cursor, pt_num, fname, lname, email, phone)
    #TODO implement printing out

def AddAddress():
    print("Add address")
    print("Enter patient number")
    pt_num = input()
    print("Enter street address")
    street = input()
    print("Enter unit number (optional)")
    street2 = input()
    print("Enter postal code (optional)")
    post = input()
    print("Enter city")
    city = input()
    print("Enter state abbreviation (CO, NY, WA, etc.)")
    state = input()
    out = pupdate.AddAddress(cursor, pt_num, street, street2, post, city, state)
    #TODO implement printing out
    
def removeAddress():
    print("Remove address")
    print("Enter patient number")
    pt_num = input()
    print("Enter street address")
    street = input()
    print("Enter postal code (optional)")
    post = input()
    print("Enter city")
    city = input()
    print("Enter state abbreviation (CO, NY, WA, etc.)")
    state = input()
    out = pupdate.AddAddress(cursor, pt_num, street, post, city, state)
    #TODO implement printing out


#--- Record functions ---
def CreateMedicalRecord():
    print("Create medical record")
    print("Enter appointment number")
    appt = input()
    print("Enter record text")
    text = input()
    out = ecreate.CreateMedicalRecord(cursor, appt, text)
    #TODO implement printing out

def ViewMedicalRecordsByPatient():
    print("View medical records by patient")
    print("Enter patient number")
    pt_num = input()
    print("Enter start date to filter by (yyyy-mm-dd) (optional)")
    start = input()
    print("Enter end date to filter by (yyyy-mm-dd) (optional)")
    end = input()
    out = eget.ViewMedicalRecordsByPatient(cursor, pt_num, start, end)
    #TODO implement printing out

#--- Prescription functions ---
def CreatePrescription():
    print("Create prescription")
    print("Enter medical record number")
    record = input()
    print("Enter medication abbreviation")
    med = input()
    print("Enter dose in mg")
    dose = input()
    print("Enter frequency in hours")
    freq = input()
    print("Enter expiration date (yyyy-mm-dd)")
    expire = input()
    out = ecreate.CreatePrescription(cursor, record, med, dose, freq, expire)
    #TODO implement printing out

def CancelPrescription():
    print("Cancel prescription")
    print("Enter patient number")
    pt_num = input()
    print("Enter medication abbreviation")
    med = input()
    out = eupdate.CancelPrescription(cursor, pt_num, med)
    #TODO implement printing out

def ViewCurrentPrescriptions():
    print("View current prescriptions")
    print("Enter patient number")
    pt_num = input()
    out = pget.ViewCurrentPrescriptions(cursor, pt_num)
    #TODO implement printing out

def ViewAllPrescriptions():
    print("View all prescriptions")
    print("Enter patient number")
    pt_num = input()
    out = eget.ViewAllPrescriptions(cursor, pt_num)
    #TODO implement printing out

#--- Appointment functions ---
def ViewFutureAppointments():
    print("View future appointments")
    print("Enter patient number")
    pt_num = input()
    out = pget.ViewFutureAppointments(cursor, pt_num)
    #TODO implement printing out

def ViewProviderAppt():
    print("View provider appointments")
    print("Enter employee number")
    employee_num = input()
    print("Enter date (yyyy-mm-dd) (optional)")
    date = input()
    out = eget.ViewProviderAppt(cursor, employee_num, date)
    #TODO implement printing out

def ViewDeptAppt():
    print("View department appointments")
    print("Enter department abbreviation")
    dept = input()
    print("Enter start date (yyyy-mm-dd) (optional)")
    start = input()
    print("Enter end date (yyyy-mm-dd) (optional)")
    end = input()
    out = eget.ViewDeptAppt(cursor, dept, start, end)
    #TODO implement printing out

def ScheduleAppointment():
    print("Schedule appointment")
    print("Enter employee number")
    employee_num = input()
    print("Enter date (yyyy-mm-dd)")
    date = input()
    print("Enter time in 24 hour format (hh:mm)")
    time = input()
    print("Enter appointment purpose")
    purpose = input()
    print("Enter patient num (optional)")
    pt_num = input()
    out = pcreate.ScheduleAppointment(cursor, employee_num, date + " " + time, purpose, pt_num)
    #TODO implement printing out

#TODO Should we remove optional date parameter from this since we also have EditAppointmentDate?
def EditAppointment():
    print("Edit appointment")
    print("Enter appointment number")
    appt = input()
    print("Enter new date and time in 24 hour format (yyyy-mm-dd hh:mm) (optional)")
    date = input()
    print("Enter new duration in minutes (optional)")
    duration = input()
    print("Enter new purpose (optional)")
    purpose = input()
    print("Enter employee number to add to appointment (optional)")
    employee_num = input()
    out = pupdate.EditAppointment(cursor, appt, date, duration, purpose, employee_num)
    #TODO implement printing out

def EditAppointmentDate():
    print("Edit appointment date")
    print("Enter appointment number")
    appt = input()
    print("Enter new date and time in 24 hour format (yyyy-mm-dd hh:mm) (optional)")
    date = input()
    out = pupdate.EditAppointmentDate(cursor, appt, date)
    #TODO implement printing out

#TODO Why is this function accessible by patient, should it only be accessible by employee?
def RemoveProviderFromAppointment():
    print("Remove provider from appointment")
    print("Enter employee number")
    employee_num = input()
    print("Enter appointment number")
    appt = input()
    out = pupdate.RemoveProviderFromAppointment(cursor, employee_num, appt)
    #TODO implement printing out

def CancelAppointment():
    print("Cancel appointment")
    print("Enter appointment number")
    appt = input()
    out = pupdate.CancelAppointment(cursor, appt)
    #TODO implement printing out

def ViewEmployeesAvailable():
    print("View employees available")
    print("Enter department abbreviation")
    dept = input()
    print("Enter date (yyyy-mm-dd)")
    date = input()
    out = eget.ViewEmployeesAvailable(cursor, dept, date)
    #TODO implement printing out

def ViewEmployeeAvailability():
    print("View employees availability")
    print("Enter employee number")
    employee_num = input()
    print("Enter date (yyyy-mm-dd)")
    date = input()
    out = pget.ViewEmployeeAvailability(cursor, employee_num, date)
    #TODO implement printing out

def CancelAppointment():
    print("Cancel appointment")
    print("Enter appointment number")
    appt = input()
    pupdate.CancelAppointment(cursor, appt)
    #TODO implement printing out

def display_cmds():
    print("--- Providers ---\n"
        + "1: View provider\n"
        + "2: Create HealthCare Provider\n"
        + "3: Edit HealthCare Provider\n"
        + "4: Edit specialty\n"
        + "5: Find employee\n"
        + "6: Change Employment status\n"
        + "7: List all specialties\n"
        + "8: List all titles\n"
        + "9: List all departments")
    print("--- Schedule ---\n"
        + "10: Create shift\n"
        + "11: Cancel shift")
    print("--- Patients ---\n"
        + "12: Find patient\n" 
        + "13: View patient info\n"
        + "14: Create patient\n"
        + "15: Edit patient\n"
        + "16: Add address\n"
        + "17: Remove address")
    print("--- Records ---\n"
        + "18: Create medical record\n"
        + "19: View medical records by patient")
    print("--- Prescriptions ---\n"
        + "20: Create prescription\n"
        + "21: Cancel prescription\n"
        + "22: View current prescriptions\n"
        + "23: View all prescriptions")
    print("--- Appointments ---\n"
        + "24: View future appointments for patient\n"
        + "25: View provider appointments\n"
        + "26: View department appointments\n"
        + "27: Schedule appointment\n"
        + "28: Edit appointment\n"
        + "29: Edit appointment date\n"
        + "30: Remove provider from appointment\n"
        + "31: View employees available\n"
        + "32: View employees availability\n"
        + "33: Cancel appointment")
    print("Type exit to terminate program")
    
def get_input():
    print("\nPlease enter API number: ")
    entry = input()
    if(entry.lower() == "exit"):
        exit(0)
    if not entry.isnumeric() or int(entry) < 1 or int(entry) > 32:
        print("Invalid entry")
        return
    entry = int(entry)
    match entry:
        case 1:
            ViewProvider()
        case 2:
            CreateHealthCareProvider()
        case 3:
            EditHealthcareProvider()
        case 4:
            EditSpecialty()
        case 5:
            FindEmployee()
        case 6: 
            ChangeEmploymentStatus()
        case 7:
            ListAllSpecialties()
        case 8:
            ListAllTitles()
        case 9: 
            ListAllDepartments()
        case 10:
            CreateShift()
        case 11:
            CancelShift()
        case 12:
            FindPatient()
        case 13:
            ViewPatientInfo()
        case 14:
            CreatePatient()
        case 15:
            EditPatient()
        case 16: 
            AddAddress()
        case 17:
            removeAddress()
        case 18:
            CreateMedicalRecord()
        case 19:
            ViewMedicalRecordsByPatient()
        case 20: 
            CreatePrescription()
        case 21: 
            CancelPrescription()
        case 22: 
            ViewCurrentPrescriptions()
        case 23: 
            ViewAllPrescriptions()
        case 24:
            ViewFutureAppointments()
        case 25: 
            ViewProviderAppt()
        case 26: 
            ViewDeptAppt()
        case 27: 
            ScheduleAppointment()
        case 28:
            EditAppointment()
        case 29: 
            EditAppointmentDate()
        case 30: 
            RemoveProviderFromAppointment()
        case 31:
            ViewEmployeesAvailable()
        case 32:
            ViewEmployeeAvailability()
        case 33:
            CancelAppointment()
    print("Press enter to continue")
    input()
        
    

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
        global cursor
        cursor = conn.cursor()
        while True:
            display_cmds()
            get_input()
    
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    main()
