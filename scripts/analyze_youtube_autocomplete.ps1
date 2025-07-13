param(
    [string]$keyword = "ai"
)

$url = "https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q=$keyword&hl=en"

$response = Invoke-WebRequest -Uri $url -Headers @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

$content = $response.Content

$prefix = "window.google.ac.h("
$suffix = ");"

if ($content.StartsWith($prefix)) {
    $jsonBody = $content.Substring($prefix.Length, $content.Length - $prefix.Length - $suffix.Length)

    if ($jsonBody -match '^\s*\[[^,]+,(.*),\s*\{') {
        $arrayPart = $matches[1].Trim()

        try {
            $suggestionsArray = $arrayPart | ConvertFrom-Json

            $suggestions = $suggestionsArray | ForEach-Object { $_[0] }

            Write-Host "`n✅ Suggestions for '$keyword':"
            $suggestions
        }
        catch {
            Write-Host "❌ JSON parse error: $_"
        }
    }
    else {
        Write-Host "❌ Regex could not extract suggestions array."
    }
}
else {
    Write-Host "❌ Unexpected response format."
    $content
}
