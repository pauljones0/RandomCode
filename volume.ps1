	while(1){
$time = Get-Random -Minimum 45 -Maximum 60
start-sleep -seconds $time
cmd /c powershell.exe "nircmd.exe mutesysvolume 0"
$time = Get-Random -Minimum 5 -Maximum 15
start-sleep -seconds $time
cmd /c powershell.exe "nircmd.exe mutesysvolume 1"
}