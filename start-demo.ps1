# start-demo.ps1
# One-button launcher for the PolicyDB Chatbot demo: starts Postgres, checks
# the policy data is loaded (offering to run the data pipeline if it isn't),
# starts both Cloudflare tunnels, then the backend and frontend already
# pointed at the correct tunnel URLs - no manual .env editing needed.
#
# Assumes Docker, Python, Node, cloudflared, and Ollama are already installed,
# and that the policydb-pg container already exists (created once via
# `docker run --name policydb-pg ...` - see README). Python dependencies for
# data-pipeline/backend/frontend are also assumed already installed.

$root = $PSScriptRoot
$backendDir = Join-Path $root "backend"
$frontendDir = Join-Path $root "frontend"
$dataPipelineDir = Join-Path $root "data-pipeline"

Write-Host "=== PolicyDB Chatbot Demo Launcher ===" -ForegroundColor Cyan

# 1. Postgres
Write-Host "`nStarting Postgres container..." -ForegroundColor Yellow
docker start policydb-pg | Out-Null

# 1b. Sanity check: does the database actually have data in it?
Write-Host "Checking policy data is loaded..." -ForegroundColor Yellow
Start-Sleep -Seconds 2  # give Postgres a moment to be ready to accept connections
$countOutput = docker exec policydb-pg psql -U postgres -d policydb -t -c "SELECT count(*) FROM policy_chunks;" 2>$null
$count = ($countOutput -as [string]).Trim()

if ([string]::IsNullOrEmpty($count) -or $count -eq "0") {
    Write-Host "`nWARNING: policy_chunks table is empty or unreachable!" -ForegroundColor Red
    Write-Host "The chatbot will start but won't be able to answer anything." -ForegroundColor Red
    $continue = Read-Host "Continue anyway with no data? (y/n)"

    if ($continue -ne "y") {
        $runPipeline = Read-Host "Run the data pipeline now to fill the database? Takes a few minutes (y/n)"
        if ($runPipeline -eq "y") {
            Write-Host "`nRunning data pipeline - this will take a few minutes..." -ForegroundColor Yellow
            Push-Location $dataPipelineDir

            python scrape_policies.py
            if ($LASTEXITCODE -ne 0) {
                Write-Host "scrape_policies.py failed - check the output above." -ForegroundColor Red
                Pop-Location; exit 1
            }

            python clean_and_chunk.py
            if ($LASTEXITCODE -ne 0) {
                Write-Host "clean_and_chunk.py failed - check the output above." -ForegroundColor Red
                Pop-Location; exit 1
            }

            python build_vector_db.py
            if ($LASTEXITCODE -ne 0) {
                Write-Host "build_vector_db.py failed - check the output above." -ForegroundColor Red
                Pop-Location; exit 1
            }

            Pop-Location
            Write-Host "Data pipeline complete." -ForegroundColor Green
        } else {
            Write-Host "Exiting. See the README's 'Local development setup' section to populate the database manually." -ForegroundColor Yellow
            exit 1
        }
    }
} else {
    Write-Host "Found $count policy chunks in the database." -ForegroundColor Green
}

# 2. Quick Ollama check (non-blocking - just a heads-up, not a hard stop)
try {
    Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 3 -UseBasicParsing | Out-Null
} catch {
    Write-Host "Warning: Ollama doesn't seem to be responding on localhost:11434. Check it's running." -ForegroundColor Red
}

# 3. Backend tunnel
Write-Host "Starting backend tunnel..." -ForegroundColor Yellow
$backendLog = Join-Path $root "tunnel-backend.log"
Remove-Item $backendLog -ErrorAction SilentlyContinue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cloudflared tunnel --url http://localhost:8000 2>&1 | Tee-Object -FilePath '$backendLog'" -WindowStyle Normal

# 4. Frontend tunnel
Write-Host "Starting frontend tunnel..." -ForegroundColor Yellow
$frontendLog = Join-Path $root "tunnel-frontend.log"
Remove-Item $frontendLog -ErrorAction SilentlyContinue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cloudflared tunnel --url http://localhost:5173 2>&1 | Tee-Object -FilePath '$frontendLog'" -WindowStyle Normal

# 5. Wait for both tunnel URLs to appear in their logs
function Wait-ForTunnelUrl($logPath, $label) {
    Write-Host "Waiting for $label tunnel URL..." -ForegroundColor Yellow
    $timeoutSeconds = 60
    $elapsed = 0
    while ($elapsed -lt $timeoutSeconds) {
        if (Test-Path $logPath) {
            $match = Select-String -Path $logPath -Pattern 'https://[a-zA-Z0-9.-]+\.trycloudflare\.com' -ErrorAction SilentlyContinue
            if ($match) {
                return $match[0].Matches[0].Value
            }
        }
        Start-Sleep -Seconds 2
        $elapsed += 2
    }
    Write-Host "Timed out waiting for $label tunnel URL. Check the $label tunnel window for errors." -ForegroundColor Red
    exit 1
}

$backendUrl = Wait-ForTunnelUrl $backendLog "backend"
$frontendUrl = Wait-ForTunnelUrl $frontendLog "frontend"

Write-Host "`nBackend tunnel:  $backendUrl" -ForegroundColor Green
Write-Host "Frontend tunnel: $frontendUrl" -ForegroundColor Green

# 6. Update frontend/.env with the backend tunnel URL
$frontendEnv = Join-Path $frontendDir ".env"
(Get-Content $frontendEnv) -replace '^VITE_API_BASE_URL=.*', "VITE_API_BASE_URL=$backendUrl" | Set-Content $frontendEnv

# 7. Update backend/.env with the frontend tunnel URL (kept alongside localhost so local dev still works too)
$backendEnv = Join-Path $backendDir ".env"
$origins = "http://localhost:5173,http://127.0.0.1:5173,$frontendUrl"
(Get-Content $backendEnv) -replace '^FRONTEND_ORIGINS=.*', "FRONTEND_ORIGINS=$origins" | Set-Content $backendEnv

# 8. Start the backend - reads the correct .env from its very first launch
Write-Host "`nStarting backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; python main.py" -WindowStyle Normal

# 9. Start the frontend
Write-Host "Starting frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev" -WindowStyle Normal

Write-Host "`nGiving the backend and frontend a moment to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# 10. Open the demo in your browser
Write-Host "`n=== Demo is live ===" -ForegroundColor Cyan
Write-Host "Link: $frontendUrl" -ForegroundColor Green
Start-Process $frontendUrl

Write-Host "`nKeep all the opened windows open for the demo to keep working." -ForegroundColor Yellow
