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
        "views/patient_dashboard_views.xml",
        "views/clinic_menus.xml"
    ],
}