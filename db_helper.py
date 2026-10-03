import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

@st.cache_resource
def init_connection() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

def insert_violation(plate: str, violation_type: str, risk_score: float, final_score: float, action: str):
    """Nayi violation ko Supabase table ('violations') mein save karta hai."""
    try:
        data = {
            "plate": plate,
            "violation_type": violation_type,
            "risk_score": float(risk_score),
            "final_score": float(final_score),
            "action": action
        }
        response = supabase.table("violations").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Database insert karne mein error aaya: {e}")
        return None

def get_violations(limit: int = 50):
    """Supabase table se recent violations fetch karta hai (order removed)."""
    try:
        # created_at ke baghair direct data fetch karenge
        response = supabase.table("violations").select("*").limit(limit).execute()
        return response.data
    except Exception as e:
        st.error(f"Data fetch karne mein error aaya: {e}")
        return []
