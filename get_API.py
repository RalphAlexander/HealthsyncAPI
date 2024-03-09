def get_medical_records(patient_num, cursor):
    try:
        query = """
        SELECT p.PatientNum, mr.MedicalRecordNum, a.AppointmentNum, mr.Date, mr.Record
        FROM medicalrecord mr 
            JOIN appointment a ON mr.appointmentid  = a.id
            JOIN patient p ON p.id = a.patientid
        WHERE p.patientnum = %s
        ORDER BY mr.date DESC;
        """
        cursor.execute(query, (patient_num,))
        records = cursor.fetchall()
        
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
    

def view_current_prescriptions(patient_num, cursor):

    """
    Description:
    Accessible by employee and patient
    Given a patient Number, return all active prescriptions for that patient.

    Parameters:
    patient_num (int) : The unique identifier for a patient
    cursor (psycopg2) : A cursor object obtained from a psycopg2 database connection, used to execute database queries.

    Return:
    {[MedicationName, Milligrams, Frequence, EndDate]};
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
        cursor.execute(query, (patient_num,))
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
    
def view_all_prescriptions(patient_num, cursor):
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
        cursor.execute(query, (patient_num,))
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
    
def view_patient_info(patient_num, cursor):
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
        cursor.execute(query, (patient_num,))
        records = cursor.fetchall()
        
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
    
def list_all_titles(cursor):
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
    
def list_all_specialties(cursor):
    try:
        query = """
        SELECT s.*
        FROM Specialty s
        ORDER BY s.abbreviation;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving all specialties: {e}")
        return []
    
def list_all_departments(cursor):
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
    
def list_all_checkinoffices(cursor):
    try:
        query = """
        SELECT cio.* 
        FROM CheckInOffice cio
        ORDER BY cio.ID;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving all check in offices: {e}")
        return []
    
def list_all_employees(cursor):
    try:
        query = """
        SELECT * 
        FROM HealthCareProvider
        ORDER BY ID;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving all check in employees: {e}")
        return []

# gotta edit this to take a third param     -------- issue, how do we provide all the specialties for each employee, what if they have more than one
def find_employees(first_name, last_name, cursor):
    try:
        query = """
        SELECT FirstName, LastName, EmployeeNum, t.Name
        FROM HealthCareProvider
	        JOIN Title t ON (TitleAbbreviation = t.Abbreviation)
        WHERE FirstName = %s AND LastName = %s
        ORDER BY EmployeeNum;
        """
        cursor.execute(query, (first_name, last_name))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving employee: {e}")
        return []

# gotta edit this to take a third param like add date of birth optional
def find_patients(first_name, last_name, cursor):
    try:
        query = """
        SELECT p.FirstName, p.LastName, p.PatientNum, p.birthday, a.Address1, a.City
        FROM Patient p
	        JOIN PatientAddresses pa ON (p.ID = pa.PatientID)
	        JOIN Address a ON (pa.AddressID = a.ID)
        WHERE FirstName = %s AND LastName = %s
        ORDER BY PatientNum;
        """
        cursor.execute(query, (first_name, last_name))
        records = cursor.fetchall()
        
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