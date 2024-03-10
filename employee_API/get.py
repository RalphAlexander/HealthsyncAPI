# TODO: Needs to be tested
def ViewAllPrescription(cursor, patientNum):
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

def ViewProviderAppt(cursor, employeeNum, date = None):
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