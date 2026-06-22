param(
    [ValidateSet("amd64", "arm64")]
    [string]$Architecture = "amd64"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$releaseDir = Join-Path $projectRoot "release"
$platform = "linux/$Architecture"
$imageArchive = Join-Path $releaseDir "solar-ems-images-linux-$Architecture.tar"
$deployArchive = Join-Path $releaseDir "solar-ems-linux-$Architecture-deploy.zip"

New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null

docker build --platform $platform -f (Join-Path $projectRoot "Dockerfile.frontend") -t solar-ems-frontend:latest $projectRoot
docker build --platform $platform -f (Join-Path $projectRoot "local-server/Dockerfile") -t solar-ems-backend:latest (Join-Path $projectRoot "local-server")
docker save -o $imageArchive solar-ems-frontend:latest solar-ems-backend:latest

Copy-Item (Join-Path $projectRoot "compose.deploy.yaml") (Join-Path $releaseDir "compose.deploy.yaml") -Force
Copy-Item (Join-Path $projectRoot "deploy/README.md") (Join-Path $releaseDir "README.md") -Force

if (Test-Path $deployArchive) {
    Remove-Item -LiteralPath $deployArchive -Force
}

Compress-Archive `
    -Path $imageArchive, (Join-Path $releaseDir "compose.deploy.yaml"), (Join-Path $releaseDir "README.md") `
    -DestinationPath $deployArchive

Write-Output "Docker deployment package created:"
Write-Output "  $deployArchive"
