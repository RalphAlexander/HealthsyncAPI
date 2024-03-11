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
    print("Enter a first name")
    fname = input()
    print("Enter a last name")
    lname = input()
    print("Enter a department abbreviation to filter by (optional)")
    dept = input()
    print("Enter a provider title to filter by (optional)")
    title = input()
    out = pget.ViewProvider(cursor, fname, lname, dept, title)
    if(not out):
        print("No results")
        return
    print("Number".ljust(8) + "First Name".ljust(16) + "Last name".ljust(16) + "Title".ljust(8) + "Department".ljust(21) + "Specialty")
    for provider in out:
        print(provider[0].ljust(7), provider[1].ljust(15), provider[2].ljust(15), provider[3].ljust(7), provider[4].ljust(20), provider[5])

def CreateHealthCareProvider():
    print("Create Healthcare Provider")
    print("Enter employee number")
    employee_num = input()
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
    out = ecreate.CreateHealthCareProvider(cursor, conn, employee_num, fname, lname, title, dept, special)
    print(out)

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
    out = eupdate.EditHealthCareProvider(cursor, conn, employee_num, title, fname, lname, dept)
    print(out)

def EditSpecialty():
    print("Edit specialty")
    print("Enter employee number")
    employee_num = input()
    print("Enter specialty")
    specialty = input()
    out = eupdate.EditSpecialty(cursor, conn, employee_num, specialty)
    print(out)

def ChangeEmploymentStatus():
    print("Change employment status")
    print("Enter employee number")
    employee_num = input()
    out = eupdate.ChangeEmploymentStatus(cursor, conn, employee_num)
    print(out)

def ListAllSpecialties():
    print("List all specialties")
    out = pget.ListAllSpecialties(cursor)
    if not out:
        return
    print("Abbreviation".ljust(14) + "Specialty")
    for specialty in out:
        print(specialty[0].ljust(14) + specialty[1])

def ListAllTitles():
    print("List all titles")
    out = pget.ListAllTitles(cursor)
    if not out:
        return
    print("Abbreviation".ljust(14) + "Specialty")
    for title in out:
        print(title[0].ljust(14) + title[1])

def ListAllDepartments():
    print("List all departments")
    out = pget.ListAllDepartments(cursor)
    if not out:
        return
    print("Abbreviation".ljust(14) + "Specialty")
    for dept in out:
        print(dept[0].ljust(14) + dept[1])

#--- schedule functions ---
def CreateShift():
    print("Create shift")
    print("Enter employee number")
    employee_num = input()
    print("Enter shift start date and time (yyyy-mm-dd hh:mm)")
    date = input() + ":00"
    print("Enter shift length (hh mm)")
    duration = input()
    if(len(duration.split()) == 1):
        duration = duration.split()[0] +"h"
    else:
        duration = duration.split()[0]+ "h " + duration.split()[1] + "m" 
    out = ecreate.CreateShift(cursor, conn, employee_num, date, duration)
    print(out)

def CancelShift():
    print("Cancel shift")
    print("Enter employee number")
    employee_num = input()
    print("Enter shift start date and time (yyyy-mm-dd hh:mm)")
    date = input() + ":00"
    out = eupdate.CancelShift(cursor, conn, employee_num, date)
    print(out)

def ViewShifts():
    print("View employee shifts")
    print("Enter employee number")
    employee_num = input()
    print("Enter start date (yyyy-mm-dd) (optional)")
    start = input()
    print("Enter end date (yyyy-mm-dd) (optional)")
    end = input()
    out = eget.ViewShifts(cursor, employee_num, start, end)
    if (out is None or not len(out)):
        print("No shifts during this date")
        return
    print("\nShift Start".ljust(26) + "Shift End".ljust(25))
    for shift in out:
        print(str(shift[3]).ljust(25) + str(shift[4]).ljust(25))

#--- Patient functions ---
def FindPatient():
    print("Find patient")
    print("Enter first name")
    fname = input()
    print("Enter last name")
    lname = input()
    print("Enter birthday (yyyy-mm-dd)")
    bday = input()
    out = eget.FindPatient(cursor, fname, lname, bday)
    if not out:
        print("No patients found")
        return
    print("First".ljust(15) + "Last".ljust(15) + "Patient Num".ljust(15) + "Birthday".ljust(15) + "Address")
    for pt in out:
        print(pt[0].ljust(15) + pt[1].ljust(15) +pt[2].ljust(15) + str(pt[3]).ljust(15) + pt[4] + " " + pt[5] + " " + pt[6])

def ViewPatientInfo():
    print("View patient info")
    print("Enter patient number")
    pt_num = input()
    out = pget.ViewPatientInfo(cursor, pt_num)
    if not out:
        print("Patient not found")
        return
    print("First".ljust(15) + "Last".ljust(15) + "Email".ljust(20) + "Phone".ljust(15) 
            + "Sex".ljust(6) + "Birthday".ljust(15) + "Address")
    for pt in out:
        print(pt[0].ljust(15) + pt[1].ljust(15) +pt[2].ljust(20) + pt[3].ljust(15) + pt[4].ljust(6) 
            + str(pt[5]).ljust(15) + pt[6] + " " + pt[7] + " " + pt[8] + " " + pt[9] + " " + pt[10])

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
    out = ecreate.CreatePatient(cursor, conn, fname, lname, sex, bday, email, phone)
    print("\n" + out)

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
    out = pupdate.EditPatient(cursor, conn, pt_num, fname, lname, email, phone)
    print(out)

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
    out = pcreate.AddAddress(cursor, conn, pt_num, city, state, street, street2, post)
    print(out)
    
def removeAddress():
    print("Remove address")
    print("Enter patient number")
    pt_num = input()
    print("Enter street address")
    street = input()
    print("Enter city")
    city = input()
    print("Enter state abbreviation (CO, NY, WA, etc.)")
    state = input()
    out = pupdate.RemoveAddress(cursor, conn, pt_num, street, city, state)
    print(out)


#--- Record functions ---
def CreateMedicalRecord():
    print("Create medical record")
    print("Enter appointment number")
    appt = input()
    print("Enter record text")
    text = input()
    out = ecreate.CreateMedicalRecord(cursor, conn, appt, text)
    print(out)

def ViewMedicalRecordsByPatient():
    print("View medical records by patient")
    print("Enter patient number")
    pt_num = input()
    print("Enter start date to filter by (yyyy-mm-dd) (optional)")
    start = input()
    print("Enter end date to filter by (yyyy-mm-dd) (optional)")
    end = input()
    out = pget.ViewMedicalRecordsByPatient(cursor, pt_num, start, end)
    if not out or not len(out):
        print("No records found")
        return
    print("Record num".ljust(15) + "Appt num".ljust(10) + "Date".ljust(25) + "Record")
    for record in out:
        print(str(record[0]).ljust(15) + str(record[1]).ljust(10) + str(record[2])[:19].ljust(25) + record[3])

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
    freq = input()+":00"
    print("Enter expiration date (yyyy-mm-dd)")
    expire = input()
    out = ecreate.CreatePrescription(cursor, conn, record, med, dose, freq, expire)
    print(out)

def CancelPrescription():
    print("Cancel prescription")
    print("Enter patient number")
    pt_num = input()
    print("Enter medication abbreviation")
    med = input()
    out = eupdate.CancelPrescription(cursor, conn, pt_num, med)
    print(out)

def ViewCurrentPrescriptions():
    print("View current prescriptions")
    print("Enter patient number")
    pt_num = input()
    out = pget.ViewCurrentPrescriptions(cursor, pt_num)
    if not out or not len(out):
        print("No current prescriptions")
        return
    print("\nMedication Name".ljust(21) + "Dose (mg)".ljust(15) + "Frequency".ljust(15) + "End Date")
    for pre in out:
        print(pre[0].ljust(20) + str(pre[1]).ljust(15) + str(pre[2]).ljust(15) + str(pre[3]))

def ViewAllPrescriptions():
    print("View all prescriptions")
    print("Enter patient number")
    pt_num = input()
    out = eget.ViewAllPrescriptions(cursor, pt_num)
    if not out or not len(out):
        print("No prescriptions found")
        return
        print("\nMedication Name".ljust(21) + "Dose (mg)".ljust(15) + "Frequency".ljust(15) + "End Date")
    for pre in out:
        print(pre[0].ljust(20) + str(pre[1]).ljust(15) + str(pre[2]).ljust(15) + str(pre[3]))

#--- Appointment functions ---
def ViewFutureAppointments():
    print("View future appointments")
    print("Enter patient number")
    pt_num = input()
    out = pget.ViewFutureAppt(cursor, pt_num)
    if (out is None or not len(out)):
        print("No future appointments")
        return
    print("\nAppointment Number".ljust(24) + "Building".ljust(19) + "Room Number".ljust(15) + "Date".ljust(25) + 
          "Duration".ljust(15) + "Purpose".ljust(30) + "Provider First".ljust(19) + "Last")
    for appt in out:
        print(str(appt[0]).ljust(23) + appt[1].ljust(19) + appt[2].ljust(15) + str(appt[3]).ljust(25) + 
              str(appt[4]).ljust(15) + appt[5].ljust(30) + appt[6].ljust(19) + appt[7])

def ViewProviderAppt():
    print("View provider appointments")
    print("Enter employee number")
    employee_num = input()
    print("Enter date (yyyy-mm-dd) (optional)")
    date = input()
    out = eget.ViewProviderAppt(cursor, employee_num, date)
    if (out is None or not len(out)):
        print("No provider appointments")
        return
    print("\nAppointment Number".ljust(24) + "Patient First".ljust(19) + "Last".ljust(15) + "Patient Number".ljust(25) + 
          "Date".ljust(25) + "Duration".ljust(15) + "Purpose")
    for appt in out:
        print(str(appt[0]).ljust(23) + appt[1].ljust(19) + appt[2].ljust(15) + appt[3].ljust(25) + 
              str(appt[4]).ljust(25) + str(appt[5]).ljust(15) + appt[6])

def ViewDeptAppt():
    print("View department appointments")
    print("Enter department abbreviation")
    dept = input()
    print("Enter start date (yyyy-mm-dd) (optional)")
    start = input()
    print("Enter end date (yyyy-mm-dd) (optional)")
    end = input()
    out = eget.ViewDepartmentAppt(cursor, dept, start, end)
    if (out is None or not len(out)):
        print("No appointments for this departmnet")
        return
    print("\nAppointment Number".ljust(24) + "Patient First".ljust(19) + "Last".ljust(15) + "Patient Number".ljust(25) +
          "Date".ljust(25) + "Duration".ljust(15) + "Purpose")
    for appt in out:
        print(str(appt[0]).ljust(23) + appt[1].ljust(19) + appt[2].ljust(15) + appt[3].ljust(25) +
              str(appt[4]).ljust(25) + str(appt[5]).ljust(15) + appt[6])

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
    out = pcreate.ScheduleAppointment(cursor, conn, employee_num, date + " " + time, purpose, pt_num)
    if (out is None or not len(out)):
        print("No appointments for this departmnet")
        return
    print(out)

def EditAppointment():
    print("Edit appointment")
    print("Enter appointment number")
    appt = input()
    print("Enter new purpose (optional)")
    purpose = input()
    print("Enter new duration in minutes (optional)")
    duration = input()
    if len(duration):
        duration += "m"
    print("Enter new patient number (optional)")
    patientNum = input()
    print("Enter employee number to add to appointment (optional)")
    employeeNum = input()
    out = eupdate.EditAppointment(cursor, conn, appt, purpose, duration, patientNum, employeeNum)
    print(out)

def EditAppointmentDate():
    print("Edit appointment date")
    print("Enter appointment number")
    appt = input()
    print("Enter new date and time in 24 hour format (yyyy-mm-dd hh:mm)")
    date = input()
    out = pupdate.EditAppointmentDate(cursor, conn, appt, date)
    print(out)

def RemoveProviderFromAppointment():
    print("Remove provider from appointment")
    print("Enter employee number")
    employee_num = input()
    print("Enter appointment number")
    appt = input()
    out = eupdate.RemoveProviderFromAppointment(cursor, conn, employee_num, appt)
    print(out)

def CancelAppointment():
    print("Cancel appointment")
    print("Enter appointment number")
    appt = input()
    out = pupdate.CancelAppointment(cursor, conn, appt)
    if not len(out):
        print("Appointment is within 24 hours and cannot be cancelled")
        return
    print(out)

def display_cmds():
    print("--- Providers ---\n"
        + "1: View provider\n"
        + "2: Create HealthCare Provider\n"
        + "3: Edit HealthCare Provider\n"
        + "4: Edit specialty\n"
        + "5: Change Employment status\n"
        + "6: List all specialties\n"
        + "7: List all titles\n"
        + "8: List all departments")
    print("--- Schedule ---\n"
        + "9: Create shift\n"
        + "10: Cancel shift\n"
        + "11: View shifts")
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
        + "31: Cancel appointment")
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
            ChangeEmploymentStatus()
        case 6:
            ListAllSpecialties()
        case 7:
            ListAllTitles()
        case 8: 
            ListAllDepartments()
        case 9:
            CreateShift()
        case 10:
            CancelShift()
        case 11:
            ViewShifts()
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
        global conn
        global cursor
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        while True:
            display_cmds()
            get_input()
    
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    main()
