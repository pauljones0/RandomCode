  
$low = 0
$high = 30
$sleep = 200

while($true){ #forever loop
for ($i = $high; $i -ge $low; $i--)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #makes the screen brighter
Start-Sleep -m $sleep
}
for ($i = $low; $i -le $high; $i++)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #dims the screen
Start-Sleep -m $sleep
}
}
