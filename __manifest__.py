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
        "views/patient_dashboard_views.xml",
        "views/appointment_management_views.xml",
        "views/doctor_dashboard_views.xml",
        "views/treatment_management_views.xml",
        "views/clinic_menus.xml"
    ],
}