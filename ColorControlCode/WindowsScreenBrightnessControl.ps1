<#
.SYNOPSIS
    Controls monitor brightness with various animation patterns.

.DESCRIPTION
    A PowerShell script that provides multiple monitor brightness control modes:
    - Fade: Smoothly transitions between minimum and maximum brightness
    - Flash: Rapidly alternates between two brightness levels
    - Pulse: Creates subtle brightness pulses relative to current brightness

    All modes can be run with a hidden or visible window.

.PARAMETER Mode
    The brightness control pattern to use:
    - Fade: Smooth transitions (default)
    - Flash: Rapid brightness changes
    - Pulse: Subtle brightness pulses

.PARAMETER MinBrightness
    Minimum brightness level (0-100). Default: 0

.PARAMETER MaxBrightness
    Maximum brightness level (0-100). Default: 30

.PARAMETER TransitionDelay
    Milliseconds between brightness changes. Default: 200

.PARAMETER HideWindow
    Switch to hide the PowerShell window. Default: False

.EXAMPLE
    # Basic fade effect
    .\BrightnessControl.ps1

.EXAMPLE
    # Hidden flash effect
    .\BrightnessControl.ps1 -Mode Flash -HideWindow

.EXAMPLE
    # Visible pulse effect with custom brightness range
    .\BrightnessControl.ps1 -Mode Pulse -MinBrightness 20 -MaxBrightness 80

.NOTES
    Requirements:
    - Windows operating system
    - Administrative privileges
    - Monitor that supports WMI brightness control

    Exit the script using Ctrl+C

    Warning: This script can cause screen flickering. Use with caution if you have
    photosensitivity or epilepsy.
#>

# Configuration
param(
    [ValidateSet('Fade', 'Flash', 'Pulse')]
    [string]$Mode = 'Fade',
    [int]$MinBrightness = 0,
    [int]$MaxBrightness = 30,
    [int]$TransitionDelay = 200,
    [switch]$HideWindow
)

# Function to hide PowerShell window
function Hide-Window {
    $signature = '[DllImport("user32.dll")] public static extern bool ShowWindow(int handle, int state);'
    Add-Type -Name Win -Member $signature -Namespace Native
    [Native.Win]::ShowWindow(([System.Diagnostics.Process]::GetCurrentProcess() | Get-Process).MainWindowHandle, 0)
}

# Initialize WMI objects with error handling
try {
    $brightnessMonitor = Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness
    $brightnessController = Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods
} catch {
    Write-Error "Failed to initialize WMI objects: $_"
    exit 1
}

# Hide window if requested
if ($HideWindow) {
    Hide-Window
}

# Mode-specific brightness control functions
function Start-BrightnessFade {
    while($true) {
        # Fade from bright to dim
        for ($brightness = $MaxBrightness; $brightness -ge $MinBrightness; $brightness--) {
            $brightnessController.WmiSetBrightness(1, $brightness)
            Start-Sleep -Milliseconds $TransitionDelay
        }
        
        # Fade from dim to bright
        for ($brightness = $MinBrightness; $brightness -le $MaxBrightness; $brightness++) {
            $brightnessController.WmiSetBrightness(1, $brightness)
            Start-Sleep -Milliseconds $TransitionDelay
        }
    }
}

function Start-BrightnessFlash {
    $flashDelay = [int](1000 / 30) # 15Hz * 2 for complete cycle
    while($true) {
        $brightnessController.WmiSetBrightness(1, $MinBrightness)
        Start-Sleep -Milliseconds $flashDelay
        $brightnessController.WmiSetBrightness(1, $MaxBrightness)
        Start-Sleep -Milliseconds $flashDelay
    }
}

function Start-BrightnessPulse {
    while($true) {
        $currentBrightness = $brightnessMonitor | Select-Object -ExpandProperty "CurrentBrightness"
        $increase = [math]::Max(1, [int]($currentBrightness/10))
        $sleepDuration = Get-Random -Minimum 50 -Maximum 200
        
        # Pulse up
        $brightnessController.WmiSetBrightness(1, $currentBrightness + $increase)
        Start-Sleep -Milliseconds $sleepDuration
        
        # Return to original
        $brightnessController.WmiSetBrightness(1, $currentBrightness)
        Start-Sleep -Milliseconds $sleepDuration
    }
}

# Main execution
try {
    switch ($Mode) {
        'Fade'  { Start-BrightnessFade }
        'Flash' { Start-BrightnessFlash }
        'Pulse' { Start-BrightnessPulse }
    }
} catch {
    Write-Error "Error during brightness control: $_"
    exit 1
} finally {
    # Restore brightness to maximum on exit
    $brightnessController.WmiSetBrightness(1, $MaxBrightness)
}