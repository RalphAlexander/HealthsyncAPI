# TODO: Needs implementation
def ViewProvider(cursor, departmentAbbreviation = None, specialtyAbbreviation = None, titleAbbreviation = None):
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
    

# TODO: needs to be tested
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
        WHERE p.patientNum = %s AND pr.enddate > CURRENT_DATE
        ORDER BY pr.enddate DESC;
        """
        cursor.execute(query, (patientNum,))
        prescriptions = cursor.fetchall()
        
        if len(prescriptions) == 0:
            print("Patient does not have any ongoing prescriptions")
            return prescriptions
        
        # Format records for better readability
        formatted_prescriptions = []
        for prescription in prescriptions:
            name, milligrams, frequency, endDate = prescription
            # Convert frequency to a total number of hours (if stored as seconds)
            hours = frequency.total_seconds() / 3600
            formatted_prescription = (name, milligrams, f"{hours} hours", endDate.strftime("%Y-%m-%d"))
            formatted_prescriptions.append(formatted_prescription)
        
        return formatted_prescriptions
        
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []

    
# TODO: Needs to be tested
def ViewMedicalRecordsByPatient(cursor, patientNum, startDate = None, endDate = None):
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
    
    try:
        # if startDate == None and endDate == None
        if not startDate and not endDate:
            query = """
            SELECT p.PatientNum, mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
            FROM medicalrecord mr 
                JOIN appointment a ON mr.appointmentid  = a.id
                JOIN patient p ON p.id = a.patientid
            WHERE p.patientnum = %s
            ORDER BY mr.date DESC;
            """
            cursor.execute(query, (patientNum,))
        # if startDate == None and endDate != None
        if not startDate:
            query = """
            SELECT p.PatientNum, mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
            FROM medicalrecord mr 
                JOIN appointment a ON mr.appointmentid  = a.id
                JOIN patient p ON p.id = a.patientid
            WHERE p.patientnum = %s AND mr.date <= %s
            ORDER BY mr.date DESC;
            """
            cursor.execute(query, (patientNum, endDate))
        # if startDate != None and endDate == None
        if not endDate:
            query = """
            SELECT p.PatientNum, mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
            FROM medicalrecord mr 
                JOIN appointment a ON mr.appointmentid  = a.id
                JOIN patient p ON p.id = a.patientid
            WHERE p.patientnum = %s AND mr.date >= %s
            ORDER BY mr.date DESC;
            """
            cursor.execute(query, (patientNum, startDate))
        
        # if startDate != None and endDate != None
        else:
            query = """
            SELECT p.PatientNum, mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
            FROM medicalrecord mr 
                JOIN appointment a ON mr.appointmentid  = a.id
                JOIN patient p ON p.id = a.patientid
            WHERE p.patientnum = %s AND mr.date >= %s and mr.date <= %s
            ORDER BY mr.date DESC;
            """
            cursor.execute(query, (patientNum, startDate, endDate))
            
        records = cursor.fetchall()
        if len(records) == 0:
            print("Patient does not have any medical records with the given parameters")
        # Format the records for better readability, specifically the Date field
        formatted_records = []
        for record in records:
            # Extract the date and format it
            date = record[3]
            formatted_date = date.strftime('%Y-%m-%d') if date else 'N/A'
            
            # Replace the original date with the formatted one in the record
            formatted_record = record[:3] + (formatted_date,) + record[4:]
            formatted_records.append(formatted_record)
        
        return formatted_records

    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []

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
        WHERE p.patientNum = %s;
        """
        cursor.execute(query, (patientNum,))
        records = cursor.fetchall()
        if len(records) == 0:
            print("Patient with PatientNum {patientNum} does not exist")
            return
        
        # Format the records for better readability
        formatted_records = []
        for record in records:
            # Extract birthday and format it
            birthday = record[5]
            formatted_birthday = birthday.strftime('%Y-%m-%d') if birthday else 'N/A'
            
            # Replace the original birthday with the formatted one in the record
            formatted_record = record[:5] + (formatted_birthday,) + record[6:]
            formatted_records.append(formatted_record)
        
        return formatted_records

    except Exception as e:
        print(f"Error retrieving patient info: {e}")
        return []

#TODO: gotta edit this to take a third param like add date of birth optional
def FindPatient(cursor, firstName, lastName, birthday = None):
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
        SELECT p.FirstName, p.LastName, p.PatientNum, p.birthday, a.Address1, a.City
        FROM Patient p
	        JOIN PatientAddresses pa ON (p.ID = pa.PatientID)
	        JOIN Address a ON (pa.AddressID = a.ID)
        WHERE FirstName = %s AND LastName = %s
        ORDER BY PatientNum;
        """
        cursor.execute(query, (firstName, lastName))
        records = cursor.fetchall()
        if len(records) == 0:
            print("Patient with the given information does not exist")
            return
        
        # Format the date of birth for each record before returning
        formatted_records = []
        for record in records:
            first_name, last_name, patient_num, dob, address1, city = record
            # Format the date of birth (dob) to a string in the desired format
            formatted_dob = dob.strftime('%Y-%m-%d')  # Converts date to 'YYYY-MM-DD' format
            # Append the formatted record to the list
            formatted_records.append((first_name, last_name, patient_num, formatted_dob, address1, city))
        
        return formatted_records

    except Exception as e:
        print(f"Error retrieving patient: {e}")
        return []

# TODO: gotta edit this to take a third param     -------- issue, how do we provide all the specialties for each employee, what if they have more than one
def FindEmployee(cursor, firstName, lastName):
    """
    Description: 
    Given an employee's first name, last name and optional title abbreviation. Show a table of matching employees with their unique num. 

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    firstName (string)          : First name of the employee to be searched.
    lastName (string)           : Last name of the employee to be searched.
    titleAbbreviation (string)  : Title of the employee to be searched.

    Returns:
    {EmployeeNum, FirstName, LastName, Title, Specialty}
    """
    
    try:
        query = """
        SELECT FirstName, LastName, EmployeeNum, t.Name
        FROM HealthCareProvider
	        JOIN Title t ON (TitleAbbreviation = t.Abbreviation)
        WHERE FirstName = %s AND LastName = %s
        ORDER BY EmployeeNum;
        """
        cursor.execute(query, (firstName, lastName))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving employee: {e}")
        return []
    
    
def ListAllSpecialties(cursor):
    """
    Description:
    Show a table of all the different kinds of specialties.

    Parameters:
    cursor (psycopg2)   : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    
    Returns 
    {SpecialtyAbbreviation, Specialty.Name}

    """
    try:
        query = """
        SELECT s.*
        FROM Specialty
        ORDER BY abbreviation;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    
    except Exception as e:
        print(f"Error retrieving all specialties: {e}")
        return []

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
        SELECT t.*
        FROM Title t
        ORDER BY t.abbreviation;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving all titles: {e}")
        return []

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
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving all departments: {e}")
        return []