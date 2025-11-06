# build_and_package.ps1
# Automates PyInstaller build and release folder creation

# Set paths
$root = Get-Location
$dist = "$root\dist"
$releaseFolder = "$dist\extract-pdf-release"
$exeName = "extract_pdf.exe"
$instructionsPDF = "$dist\Instructions.pdf"

# Step 1: Build the executable
Write-Host "Building extract_pdf.exe with PyInstaller..." -ForegroundColor Cyan
pyinstaller --onefile "$root\extract_pdf.py"

# Step 2: Clean previous release folder
if (Test-Path $releaseFolder) {
    Write-Host "Removing old release folder..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $releaseFolder
}

# Step 3: Create release folder and subfolders
Write-Host "Creating release folder structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $releaseFolder | Out-Null
New-Item -ItemType Directory -Path "$releaseFolder\input" | Out-Null
New-Item -ItemType Directory -Path "$releaseFolder\output" | Out-Null
New-Item -ItemType Directory -Path "$releaseFolder\archive" | Out-Null

# Step 4: Copy new executable
Write-Host "Copying executable..." -ForegroundColor Cyan
Copy-Item "$dist\$exeName" -Destination $releaseFolder -Force

# Step 5: Copy Instructions PDF
Write-Host "Copying Instructions.pdf..." -ForegroundColor Cyan
if (Test-Path $instructionsPDF) {
    Copy-Item $instructionsPDF -Destination $releaseFolder -Force
} else {
    Write-Host "WARNING: Instructions.pdf not found in dist" -ForegroundColor Red
}

# Step 6: Zip the release folder
$zipPath = "$dist\extract-pdf-release.zip"
Write-Host "Creating zip archive..." -ForegroundColor Cyan
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path $releaseFolder -DestinationPath "$dist\extract-pdf-release.zip" -Force

Write-Host "✅ Release package ready: $zipPath" -ForegroundColor Green

# Optional: Clean up PyInstaller build artifacts
Write-Host "Cleaning up PyInstaller build artifacts..." -ForegroundColor Cyan
Remove-Item -Recurse -Force "$root\build", "$root\extract_pdf.spec" -ErrorAction SilentlyContinue
