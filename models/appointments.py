from models.utils import MongoConn

def get_appointments(collection):
    
    try:
        conn = MongoConn().connect()
        
        patient_ids = [patient['_id'] for patient in conn['Patients'].find()]
        pipeline = [{
            "$lookup" : {
                "from" : "Patients",
                "localField": "patiendID",
                "foreignField": "_id",
                "as" : "patient_info"                
            }
            },
            {
                "$unwind" : "$patient_info"
            },
            {
                "$project": {
                    "appointment_id": "$_id",
                    "first_name" : "$patient_info.firstName",
                    "last_name" : "$patient_info.lastName",
                    "appointment_time" : "$appointmentDate",
                    "reason": "$reason",
                    "status" : "$status",
                    "notes": "$notes"
                }
            }  
        ]
        appointments = conn.appointments.aggregate(pipeline=pipeline)
        appointments = [appointment for appointment in appointments]
        return appointments
    except Exception as e:
        return f"Error Occured in fetching appointments {e}"