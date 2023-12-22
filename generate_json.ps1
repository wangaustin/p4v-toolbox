param (
    [string]$Username
)

p4 changes -u $Username -s submitted -l > changelists.txt
Start-Sleep -Seconds .1
Get-Content changelists.txt | ForEach-Object {
    if ($_ -match '^Change (\d+) on (\d{4}/\d{2}/\d{2}) by (.+?)@(.+)$') {
        $currentObj = [PSCustomObject]@{
            Changelist = [int]$matches[1]
            Date = $matches[2]
            Author = $matches[3]
            Workspace = $matches[4]
            Description = @()
        }
    } elseif ($currentObj) {
        $currentObj.Description += $_ -replace '^\s+'
    }
    $currentObj
} | Group-Object Changelist | ForEach-Object {
    $_.Group[0].Description = $_.Group[0].Description -ne ''
    $_.Group[0]
} | Select-Object -Property Changelist, Date, Author, Workspace, Description | ConvertTo-Json | Out-File -Encoding UTF8 -FilePath changelists.json
