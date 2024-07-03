{
    "name": "Clinic",
    "summary": "Clinic module",
    "author": "Quadova",
    
    "application": True,
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/patient_sequence.xml",
        "data/appointment_sequence.xml",
        "views/clinic_patient_views.xml",
        "views/clinic_appointment_views.xml",
        "views/clinic_doctor_views.xml",
        "views/clinic_treatment_views.xml",
        "views/clinic_medical_record_views.xml",
        "views/clinic_prescription_views.xml",
        "views/clinic_logs_views.xml",
        "views/clinic_menus.xml"
    ],
}