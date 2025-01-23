import os
from supabase import create_client

# إعداد Supabase Client
def get_supabase_client():
    url = os.getenv("SUPABASE_URL")  # رابط المشروع من Supabase
    key = os.getenv("SUPABASE_KEY")  # مفتاح service_role
    return create_client(url, key)
