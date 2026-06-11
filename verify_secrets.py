import os

print("=== Verifying Environment Variables ===")
print(f"OWM_API_KEY: {'SET' if os.environ.get('OWM_API_KEY') else 'MISSING'}")
print(f"ACCOUNT_SID: {'SET' if os.environ.get('ACCOUNT_SID') else 'MISSING'}")
print(f"AUTH_TOKEN: {'SET' if os.environ.get('AUTH_TOKEN') else 'MISSING'}")
print("=== Verification Complete ===")
