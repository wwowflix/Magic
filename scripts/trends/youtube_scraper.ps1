# Your API Key
$apiKey = "AIzaSyAFhk0N5grMqInsZkH4pTJBdyXVJ-n5xs4"

# Keyword you want to search on YouTube
$query = "AI tools"

# Max number of results to fetch
$maxResults = 10

# Encode the search query
Add-Type -AssemblyName System.Web
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)

# Build the URL safely using -f string formatting (no ampersands interpreted)
$urlTemplate = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={0}&q={1}&type=video&key={2}'
$url = $urlTemplate -f $maxResults, $encodedQuery, $apiKey

# Call YouTube Search API
$response = Invoke-RestMethod -Uri $url

# Extract relevant info
$rows = foreach ($item in $response.items) {
    [PSCustomObject]@{
        date     = $item.snippet.publishedAt
        keyword  = $item.snippet.title
        platform = "YouTube"
        metric   = 0
        author   = $item.snippet.channelTitle
    }
}

# Write to CSV
$csvPath = "D:\MAGIC\outputs\youtube_scrape.csv"
$rows | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Host "`n✅ youtube_scrape.csv created at $csvPath"
