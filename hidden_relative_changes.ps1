#stuff grabbed from stack overflow to hide the powershell window
$t = '[DllImport("user32.dll")] public static extern bool ShowWindow(int handle, int state);'
add-type -name win -member $t -namespace native
[native.win]::ShowWindow(([System.Diagnostics.Process]::GetCurrentProcess() | Get-Process).MainWindowHandle, 0)  


while($true){ #forever loop
$brightness = Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Select -ExpandProperty "CurrentBrightness" #gets the current brightness
$sleep = Get-Random -Minimum -50 -Maximum 200 #gets random interval to pause by
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$brightness + [math]::Max(1,[int]($brightness/10))) #makes the screen brighter by 10%
Start-Sleep -m $sleep
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$brightness) #dims the screens the screen barely
Start-Sleep -m $sleep
}