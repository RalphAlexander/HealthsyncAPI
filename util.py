def GenerateAppointmentNum(cursor):
    """
    Generates the next appointment number by incrementing the highest existing appointment number in the database.
    
    Parameters:
    cursor (psycopg2): Database cursor for executing SQL queries.
    
    Returns:
    int: The next appointment number.
    """
    try:
        # Query to find the highest appointment number
        cursor.execute("SELECT MAX(appointmentNum) FROM Appointment;")
        max_appointment_num = cursor.fetchone()[0]
        
        if max_appointment_num is not None:
            # Increment the highest number by 1
            next_appointment_num = max_appointment_num + 1
        else:
            # If no appointments exist, start from a specific number (e.g., 1)
            next_appointment_num = 1
            
        return next_appointment_num
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error as appropriate (e.g., logging, re-throwing, etc.)
        return None
