# TODO: Needs to be tested
def ViewAllPrescriptions(cursor, patientNum):
    """
    Description:
    Given a patient Number, return all active prescriptions for that patient.

    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (int)    : The unique identifier for a patient.

    Return:
    {MedicationName, Milligrams, Frequence, EndDate};
    """
    
    try:
        query = """
        SELECT m.name, pr.milligrams, pr.frequency, pr.endDate
        FROM Prescription pr
            JOIN medicalrecord mr ON (mr.id = pr.medicalrecordid)
            JOIN appointment a ON (a.id = mr.appointmentid )
            JOIN patient p ON (p.id = a.patientid)
            JOIN medication m ON (m.abbreviation = pr.medicationAbbreviation)
        WHERE p.patientNum = %s
        ORDER BY pr.enddate DESC;
        """
        cursor.execute(query, (patientNum,))
        records = cursor.fetchall()
        
        # Format records for better readability
        formatted_records = []
        for record in records:
            name, milligrams, frequency, endDate = record
            # Convert frequency to a total number of hours (if stored as seconds)
            hours = frequency.total_seconds() / 3600
            formatted_record = (name, milligrams, f"{hours} hours", endDate.strftime("%Y-%m-%d"))
            formatted_records.append(formatted_record)
        
        return formatted_records

    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []

def ViewProviderAppt(cursor, employeeNum, date = None):     # TESTED 1
    """
    Description: 
    Given an employee number and optional date, return all appointments for that provider.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    employeeNum (int)       : The unique identifier for an employee.
    date (string)           : A date formatted in any accepted format.

    Returns:
    {AppointmentNum, PatientName, Date, Duration, Purpose}
    """
    try:
        if (date is None):
            query = """
            SELECT a.AppointmentNum, p.FirstName, p.LastName, p.PatientNum, a.Date, a.Duration, a.Purpose
            FROM Patient p
                JOIN Appointment a ON (p.ID = a.PatientID)
                JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
                JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
            WHERE hc.employeeNum = %s;
            """
            cursor.execute(query, (employeeNum,))
        else:
            query = """
            SELECT a.AppointmentNum, p.FirstName, p.LastName, p.PatientNum, a.Date, a.Duration, a.Purpose
            FROM Patient p
                JOIN Appointment a ON (p.ID = a.PatientID)
                JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
                JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
            WHERE hc.employeeNum = %s AND CAST(a.date AS DATE) = CAST(%s AS DATE);
            """
            cursor.execute(query, (employeeNum, date,))
        appointments = cursor.fetchall()
        if len(appointments) == 0:
            print("Employee with EmployeeNum {employeeNum} does not exist")
            return
    
        # Format the Date and Duration fields for better readability
        formatted_appointments = []
        for record in appointments:
            appointment_num, first_name, last_name, patient_num, date, duration, purpose = record

            # Format the Date field
            formatted_date = date.strftime('%Y-%m-%d %H:%M:%S') if date else 'N/A'

            # Format the Duration field
            formatted_duration = f"{duration.seconds // 3600} hours {duration.seconds % 3600 // 60} minutes" if duration else 'N/A'

            # Replace the original Date and Duration with the formatted ones in the record
            formatted_record = (appointment_num, first_name, last_name, patient_num, formatted_date, formatted_duration, purpose)
            formatted_appointments.append(formatted_record)

        return formatted_appointments

    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return []

def ViewDepartmentAppt(cursor, departmentAbbreviation, startDate = None, endDate = None):
    """
    Description: 
    Given a department abbreviation, and an optional date range, return all appointments
    for that department.Show only appointments between the date range if provided.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    DepartmentAbbreviation (string) : Department of the provider to be searched.
    startDate (string)              : A date formatted in any accepted format.
    endDate (string)                : A date formatted in any accepted format.

    Returns:
    {AppointmentNum, PatientName, Date, time, Duration, purpose, providerName}
    """
    
def ViewEmployeesAvailablity(cursor, departmentAbbreviation, date):
    """
    Description: 
    Given a department abbreviation, and date, return all providers who are on shift but not in an appointment at that time.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    DepartmentAbbreviation (string) : Department of the provider to be searched.
    date (string)                   : A date formatted in any accepted format.

    Returns:
    {FirstName, LastName, EmployeeNum, Email, Phone}

    """

def FindPatient(cursor, firstName, lastName, birthday):
    """
    Description: 
    Given a patient's first name, last name, and date of birth. Show a list of patients that match the input and include patientNum. 

    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    firstName (string)  : First name of the patient to be searched.
    lastName (string)   : Last name of the patient to be searched.
    birthday (string)   : Title of the patient to be searched.

    Returns:
    {FirstName, LastName, PatientNum, Birthday, Address1, City}
    """
    
    try:
        query = """
        SELECT p.FirstName, p.LastName, p.PatientNum, p.birthday, a.Address1, a.City, a.stateabbreviation
        FROM Patient p
	        JOIN PatientAddresses pa ON (p.ID = pa.PatientID)
	        JOIN Address a ON (pa.AddressID = a.ID)
        WHERE FirstName ILIKE %s AND LastName ILIKE %s AND birthday = %s
        ORDER BY PatientNum;
        """
        cursor.execute(query, (firstName, lastName, birthday))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving patient: {e}")
        return None