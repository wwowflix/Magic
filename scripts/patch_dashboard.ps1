# patch_dashboard.ps1 — auto-patch dashboard.py to use SQLite for all platforms

Write-Host "Patching dashboard.py for SQLite integration..."

# Read in the dashboard source
$content = Get-Content .\dashboard.py -Raw

# Remove any pd.read_csv(...) calls
$content = $content -replace 'pd\.read_csv\([^)]*\)\s*',''

# Inject SQLite-loading logic for each platform
$injection = @"
import sqlite3
def load_platform(platform):
    conn = sqlite3.connect(r\"D:\MAGIC\outputs\zephyr_trends.db\")
    df = pd.read_sql_query(f\"SELECT * FROM trends WHERE platform = '{platform}'\", conn)
    conn.close()
    return df

# Replace data-loading section:
platforms = ['google_trends','reddit','YouTube','tiktok']
for plat in platforms:
    st.subheader(plat.capitalize())
    df = load_platform(plat)
    st.dataframe(df)
"@

# Replace old loop or placeholder with the new injection
$content = $content -replace '(?s)#\s*DATA-LOADING-PLACEHOLDER.*?#\s*END-PLACEHOLDER', $injection

# Write the patched file back
Set-Content .\dashboard.py $content -Encoding UTF8

Write-Host "✅ dashboard.py patched successfully!"
