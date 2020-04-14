while($true){ #forever loop
for ($i = 100; $i -gt 1; $i--)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #makes the screen brighter
Start-Sleep -m 250 #takes 250 millisecond breaks
}
for ($i = 1; $i -lt 100; $i++)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #dims the screen
Start-Sleep -m 250
}
Start-Sleep -s 30 #does nothing for 30 seconds
}