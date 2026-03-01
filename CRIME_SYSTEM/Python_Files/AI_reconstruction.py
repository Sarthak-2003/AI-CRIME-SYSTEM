import os
from datetime import datetime

def generate_case_story(crime_desc, ipc_sections):
    date = datetime.now().strftime("%d %B %Y")
    
    story = f"""
    OFFICIAL INCIDENT RECONSTRUCTION REPORT
    
    Date of Report: {date}
    
    Incident Summary:
    {crime_desc}
    
    Legal Analysis:
    Based on automated legal intelligence analysis,
    the applicable IPC Sections are: {ipc_sections}.
    
    Reconstruction Narrative:
    The incident appears to involve unlawful activity
    as described above. The accused engaged in actions
    violating Indian Penal Code provisions.
    
    Further investigation is recommended.
    """
    
    return story