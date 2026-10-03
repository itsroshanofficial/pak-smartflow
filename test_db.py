from supabase import create_client, Client

url = "https://oldfvpnmafwatbymgqaa.supabase.co"
key = "sb_publishable_4ZZuUs4Zbk9o_wa1522kWA_z1KmpN2C"

supabase: Client = create_client(url, key)

# Naya violation record insert karna
data = {
    "vehicle_number": "LEA-1234",
    "violation_type": "Speeding",
    "confidence_score": 0.95,
    "risk_score": 8.5,
    "compliance_score": 40.0,
    "status": "Pending"
}

response = supabase.table("violations").insert(data).execute()
print("Data Inserted Successfully:", response.data)