$low = 80
$high = 100
$sleepseconds = 5

while($true){ #forever loop
for ($i = $high; $i -ge $low; $i--)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #makes the screen brighter
Start-Sleep -m 200 #takes 200 millisecond breaks
}
Start-Sleep -s $sleepseconds
for ($i = $low; $i -le $high; $i++)
{
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$i) #dims the screen
Start-Sleep -m 200
}
Start-Sleep -s $sleepseconds
}
