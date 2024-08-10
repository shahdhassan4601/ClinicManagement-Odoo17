{
    "name": "Clinic",
    "summary": "Clinic module",
    "author": "Quadova",
    
    "application": True,
    "depends": [
        "base",
        "account",
        "sale"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "reports/clinic_patient_reports.xml",
        "reports/clinic_patient_templates.xml",
        "views/clinic_patient_views.xml",
        "views/clinic_appointment_views.xml",
        "views/clinic_doctor_views.xml",
        "views/clinic_treatment_views.xml",
        "views/clinic_medical_record_views.xml",
        "views/clinic_prescription_views.xml",
        "views/clinic_logs_views.xml",
        "views/account_move_views.xml",
        "views/clinic_menus.xml"
    ],
}