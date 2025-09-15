# patch_dashboard.ps1 — replace CSV reads with SQLite queries in dashboard.py

# 1) Backup the original
Copy-Item -Path .\dashboard.py -Destination .\dashboard.py.bak -Force

# 2) Load the dashboard into memory
$code = Get-Content .\dashboard.py -Raw

# 3) Remove the old CSV loop (from file_paths to end of that block)
$code = $code -replace '(?ms)for\s+platform,\s*file\s+in\s*file_paths\.items\(\).*?conn\.close\(\)', @"
import sqlite3
conn = sqlite3.connect('zephyr_trends.db')
for platform in ['google_trends','reddit','YouTube','tiktok']:
    st.header(platform.capitalize())
    df = pd.read_sql_query(
        \"SELECT * FROM trends WHERE platform = '$platform'\",
        conn
    )
    st.dataframe(df)
conn.close()
"@

# 4) Save the patched dashboard.py
Set-Content .\dashboard.py -Value $code -Encoding UTF8

Write-Host "✅ dashboard.py patched to use SQLite (backup at dashboard.py.bak)"
