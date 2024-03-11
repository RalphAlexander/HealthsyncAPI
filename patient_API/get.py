def ViewProvider(cursor, firstname = "", lastname = "", departmentAbbreviation = "", titleAbbreviation = ""):
    """
    Description: 
    Given optional filters of department name, specialty and provider title, return all providers who match the given filters.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    departmentAbbreviation (string) : Department of the provider to be searched.
    specialtyAbbreviation (string)  : Specialty of the provider to be searched.
    titleAbbreviation (string)      : Title of the provider to be searched.

    Returns: 
    {FirstName, LastName, Title.name, Department.Name, Specialty.Name, EmployeeNum}
    """
    query = """
    SELECT employeeNum, firstname, lastname, titleabbreviation, department.name, specialtyname
    FROM healthcareprovider
        LEFT JOIN providerspecialties ON providerspecialties.providerid = healthcareprovider.id
        LEFT JOIN specialty ON specialtyabbreviation = specialty.abbreviation
        JOIN department ON departmentabbreviation = department.abbreviation
    WHERE currentlyemployed AND firstname ILIKE %s AND lastname ILIKE %s AND departmentabbreviation ILIKE %s AND titleAbbreviation ILIKE %s
    ORDER BY lastname
    """
    try:
        cursor.execute(query, ("%" + firstname +"%", "%"+lastname+"%", "%" + departmentAbbreviation + "%", "%" + titleAbbreviation + "%"))
        providers = cursor.fetchall()
        return providers
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    

# TODO: Needs implementation
def ViewEmployeeAvailability(cursor, employeeNum, date):
    """
    Description: 
    Given an employee number, return all times the provider is on shift and not scheduled for an appointment.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    employeeNum (string)    : The unique identifier for an employee.
    date (string)           : A date formatted in any accepted format.

    Returns: 
    {AvailableTime}
    """
    

def ViewCurrentPrescriptions(cursor, patientNum):
    """
    Description:
    Given a patient Number, return all active prescriptions for that patient.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)     : The unique identifier for a patient.

    Returns:
    {MedicationName, Milligrams, Frequence, EndDate};
    """

    try:
        query = """
        SELECT m.name, pr.milligrams, pr.frequency, pr.endDate
        FROM Prescription pr
            JOIN medicalrecord mr ON (mr.id = pr.medicalrecordid)
            JOIN appointment a ON (a.id = mr.appointmentid) 
            JOIN patient p ON (p.id = a.patientid)
            JOIN medication m ON (m.abbreviation = pr.medicationAbbreviation)
        WHERE p.patientNum ILIKE %s AND pr.enddate > CURRENT_DATE
        ORDER BY pr.enddate DESC;
        """
        cursor.execute(query, (patientNum,))
        return cursor.fetchall()
        
    except Exception as e:
        print(f"Error retrieving Current Prescriptions: {e}")
        return None

    
def ViewMedicalRecordsByPatient(cursor, patientNum, startDate = "", endDate = ""):
    """
    Description:
    Given a patient Number and optional start and end dates, return all medical records for that patient. 
    Return all medical records for that patient that were created between the start and end dates if provided.
    
    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)     : The unique identifier for a patient.
    startDate (string)      : A date formatted in any accepted format.
    endDate (string)        : A date formatted in any accepted format.
    
    Returns:
    {MedicationRecordNum, AppointmentNum, Date, RecordText}
    """
    query = """
    SELECT mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
    FROM medicalrecord mr 
        JOIN appointment a ON mr.appointmentid  = a.id
        JOIN patient p ON p.id = a.patientid
    WHERE p.patientnum ILIKE %s AND mr.date >= %s AND mr.date <= %s
    ORDER BY mr.date DESC;
    """
    if not len(startDate):
        startDate = "1900-01-01"
    if not len(endDate):
        endDate = "3000-12-31"
    try:
        cursor.execute(query, (patientNum, startDate, endDate))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return None

def ViewFutureAppt(cursor, patientNum):
    """
    Description: 
    Given a patient number, show all future appointments for that patient including their appointment providers and check in locations.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)     : The unique identifier for a patient.

    Returns:
    {AppointmentNum, Building, Room, Date, Time, Duration, Purpose, ProviderName}
    """
    query = """
    SELECT a.AppointmentNum, cio.Building, cio.RoomNumber, a.Date, a.Duration, a.Purpose, hc.FirstName, hc.LastName
    FROM Patient p
        JOIN Appointment a ON (p.ID = a.PatientID)
        JOIN AppointmentProviders ap ON (a.ID = ap.AppointmentID)
        JOIN HealthCareProvider hc ON (ap.HealthCareProviderID = hc.ID)
        JOIN Department d ON (hc.DepartmentAbbreviation = d.Abbreviation)
        JOIN CheckInOffice cio ON (d.CheckInOfficeID = cio.ID)
    WHERE p.patientNum ILIKE %s;
    """
    try:
        cursor.execute(query, (patientNum,))
        return cursor.fetchall()
    
    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return None

def ViewPatientInfo(cursor, patientNum):
    """
    Description: 
    Given a patient number, show all that patient's info and addresses. 

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)     : The unique identifier for a patient.

    Returns:
    {FirstName, LastName, Email, Phone, Sex, Birthday, Address1, Address2, PostalCode, City, StateAbbreviation}
    """
    
    try:
        query = """
        SELECT p.FirstName, p.LastName, p.Email, p.Phone, s.Sex, p.Birthday, a.Address1, a.Address2, 
                a.PostalCode, a.City, a.StateAbbreviation
        FROM Patient p
            JOIN PatientAddresses pa ON (p.ID = pa.PatientID)
	        JOIN Address a ON (pa.AddressID = a.ID)
            JOIN Sex s ON (p.SexID = s.SexID)
        WHERE p.patientNum ILIKE %s;
        """
        cursor.execute(query, (patientNum,))
        records = cursor.fetchall()
        if len(records) == 0:
            raise Exception("Patient not found")
        return records
    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return None

    
def ListAllSpecialties(cursor):
    """
    Description:
    Show a table of all the different kinds of specialties.

    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    
    Returns 
    {SpecialtyAbbreviation, Specialty.Name}

    """
    query = """
    SELECT *
    FROM Specialty
    ORDER BY abbreviation;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving all specialties: {e}")
        return None

def ListAllTitles(cursor):
    """
    Description:
    Show a table of all the different kinds of titles.

    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    
    Returns:
    {TitleAbbreviation, Title.Name}
    """
    
    try:
        query = """
        SELECT *
        FROM Title
        ORDER BY abbreviation;
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving all titles: {e}")
        return None

def ListAllDepartments(cursor):
    """
    Description: 
    Show a table of all the different departments including the building and room number for their check in offices.
    
    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    
    Returns: 
    {DepartmentAbbreviation, Department.Name, CheckInOffice.Building, CheckInOffice.RoomNumber}
    """
    
    try:
        query = """
        SELECT d.Abbreviation, d.Name, cio.Building, cio.RoomNumber
        FROM Department d
	        JOIN CheckInOffice cio ON (d.CheckInOfficeID = cio.ID)
        ORDER BY d.Name;
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving all departments: {e}")
        return []