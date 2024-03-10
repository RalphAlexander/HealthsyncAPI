
# TODO: Not in the doc, dont know what to do with this
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
    
# TODO: Not in the doc, dont know what to do with this
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
