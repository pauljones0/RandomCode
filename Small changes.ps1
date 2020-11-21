  
$brightness = Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Select -ExpandProperty "CurrentBrightness" #gets the current brightness
$sleep = 200

while($true){ #forever loop
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$brightness+1) #makes the screen brighter by 1
Start-Sleep -m $sleep
(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,$brightness) #dims the screens the screen barely
Start-Sleep -m $sleep
}