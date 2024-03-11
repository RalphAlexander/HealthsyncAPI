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

def EditAppointmentDate():
    print("Edit appointment date")
    print("Enter appointment number")
    appt = input()
    print("Enter new date and time in 24 hour format (yyyy-mm-dd hh:mm)")
    date = input()
    out = pupdate.EditAppointmentDate(cursor, conn, appt, date)
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
        + "2: List all specialties\n"
        + "3: List all titles\n"
        + "4: List all departments")
    print("--- Schedule ---\n"
        + "5: View shifts")
    print("--- Patients ---\n"
        + "6: View patient info\n"
        + "7: Edit patient\n"
        + "8: Add address\n"
        + "9: Remove address")
    print("--- Records ---\n"
        + "10: View medical records by patient")
    print("--- Prescriptions ---\n"
        + "11: View current prescriptions")
    print("--- Appointments ---\n"
        + "12: View future appointments for patient\n"
        + "13: Schedule appointment\n"
        + "14: Edit appointment date\n"
        + "15: Cancel appointment")
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
            ListAllSpecialties()
        case 3:
            ListAllTitles()
        case 4: 
            ListAllDepartments()
        case 5:
            ViewShifts()
        case 6:
            ViewPatientInfo()
        case 7:
            EditPatient()
        case 8: 
            AddAddress()
        case 9:
            removeAddress()
        case 10:
            ViewMedicalRecordsByPatient()
        case 11: 
            ViewCurrentPrescriptions()
        case 12:
            ViewFutureAppointments()
        case 13: 
            ScheduleAppointment()
        case 14: 
            EditAppointmentDate()
        case 15:
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
