import streamlit as st
from supabase import create_client, Client

# Streamlit secrets se secure credentials fetch karna
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

@st.cache_resource
def init_connection() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

def add_violation(vehicle_no, violation_type, confidence, risk, compliance):
    """Database mein new violation save karne ke liye function"""
    data = {
        "vehicle_number": vehicle_no,
        "violation_type": violation_type,
        "confidence_score": float(confidence),
        "risk_score": float(risk),
        "compliance_score": float(compliance),
        "status": "Pending"
    }
    response = supabase.table("violations").insert(data).execute()
    return response.data

def get_all_violations():
    """Saari violations fetch karne ke liye function"""
    response = supabase.table("violations").select("*").execute()
    return response.data