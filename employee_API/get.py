from datetime import datetime

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
    query = """
    SELECT m.name, pr.milligrams, pr.frequency, pr.endDate
    FROM Prescription pr
        JOIN medicalrecord mr ON (mr.id = pr.medicalrecordid)
        JOIN appointment a ON (a.id = mr.appointmentid )
        JOIN patient p ON (p.id = a.patientid)
        JOIN medication m ON (m.abbreviation = pr.medicationAbbreviation)
    WHERE p.patientNum ILIKE %s
    ORDER BY pr.enddate DESC;
    """
    try:
        cursor.execute(query, (patientNum,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return None

def ViewProviderAppt(cursor, employeeNum, date = ""):
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
        if (date == ""):
            query = """
            SELECT a.AppointmentNum, p.FirstName, p.LastName, p.PatientNum, a.Date, a.Duration, a.Purpose
            FROM Patient p
                JOIN Appointment a ON (p.ID = a.PatientID)
                JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
                JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
            WHERE hc.employeeNum ILIKE %s;
            """
            cursor.execute(query, (employeeNum,))
        else:
            query = """
            SELECT a.AppointmentNum, p.FirstName, p.LastName, p.PatientNum, a.Date, a.Duration, a.Purpose
            FROM Patient p
                JOIN Appointment a ON (p.ID = a.PatientID)
                JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
                JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
            WHERE hc.employeeNum ILIKE %s AND CAST(a.date AS DATE) = CAST(%s AS DATE);
            """
            cursor.execute(query, (employeeNum, date))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving provider appointments: {e}")
        return None


def ViewDepartmentAppt(cursor, departmentAbbreviation, startDate = "", endDate = ""):
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
    {AppointmentNum, PatientName, Date, Duration, purpose, providerName}
    """
    query = """
    SELECT a.AppointmentNum, p.FirstName, p.LastName, p.PatientNum, a.Date, a.Duration, a.Purpose, hc.FirstName, hc.LastName
    FROM Patient p
        JOIN Appointment a ON (p.ID = a.PatientID)
        JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
        JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
        JOIN Department d ON (hc.DepartmentAbbreviation = d.Abbreviation)
    WHERE d.Abbreviation ILIKE %s
        AND a.Date >= %s AND a.Date <= %s;
    """
    if not endDate:
        endDate = '3000-02-02'
    if not startDate:
        startDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute(query, (departmentAbbreviation, startDate, endDate))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return None

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

def ViewShifts(cursor, EmployeeNum, startDate = "", endDate = ""):
    """
    Description: 
    Given a Employee number, and date, return all shift times that employee works during that date range

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    DepartmentAbbreviation (string) : Department of the provider to be searched.
    date (string)                   : A date formatted in any accepted format.

    Returns:
    {FirstName, LastName, EmployeeNum, Email, Phone}

    """
    if not endDate:
        endDate = '3000-02-02'
    if not startDate:
        startDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
    SELECT hc.FirstName, hc.LastName, hc.EmployeeNum, ps.shiftstart, ps.duration
    FROM ProviderShifts ps
        JOIN HealthCareProvider hc ON (ps.HealthCareProviderID = hc.ID)
    WHERE hc.EmployeeNum ILIKE %s AND ps.shiftstart >= %s AND ps.shiftstart <= %s;
    """
    try:
        cursor.execute(query, (EmployeeNum, startDate, endDate))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return None