	while(1){
$time = Get-Random -Minimum 1 -Maximum 2
start-sleep -seconds $time



#$obj = new-object -com wscript.shell 
#$obj.SendKeys([char]173) #this requires no extra programs, but the mute button apppears.
cmd /c powershell.exe "nircmd.exe mutesysvolume 0"


$time = Get-Random -Minimum 1 -Maximum 2
start-sleep -seconds $time


#$obj = new-object -com wscript.shell 
#$obj.SendKeys([char]173) #ditto
cmd /c powershell.exe "nircmd.exe mutesysvolume 1" #this is nice because nothing new appears on the screen.
}
