$low = 0
$high = 20
$hz = 15
$sleep = 1000/($hz*2)

while($true){ #forever loop
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$low)
Start-Sleep -m $sleep
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$high)
Start-Sleep -m $sleep
}