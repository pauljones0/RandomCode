# RandomCode 🚀

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/pauljones0/RandomCode/graphs/commit-activity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![C](https://img.shields.io/badge/C-GNU-00599C.svg)](https://gcc.gnu.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-5391FE.svg)](https://github.com/PowerShell/PowerShell)

A collection of utility scripts and experimental projects focused on automation and creative coding solutions.

## 🗂️ Projects

### 🎬 YouTube Watch Later Cleaner
A browser-based utility script for efficiently cleaning up your YouTube Watch Later playlist.

**Features:**
- Automated removal of videos from Watch Later playlist
- Shows hidden/unavailable videos automatically
- Smart playlist state detection
- Progress tracking with detailed console output
- Resilient retry mechanism for UI interactions
- Safe operation with built-in delays and URL validation
- Rate limiting with automatic 5-minute pauses after every 600 videos
- Automatic cleanup when navigating away from playlist

**Usage:**
1. Navigate to your [YouTube Watch Later playlist](https://www.youtube.com/playlist?list=WL)
2. Open browser DevTools (Press F12 or right-click → Inspect)
3. Paste the script into the Console tab and press Enter to begin cleanup

**Location:** `/Experiments/removeWatchLater.js`

### 🔆 Smart Home Light Control
A comprehensive multi-ecosystem light management system supporting Philips Hue, LIFX, and Govee devices.

**Features:**
- Cross-platform compatibility with major smart light brands
- GUI interface for easy control
- Advanced lighting effects:
  - RGB color cycling
  - Synchronized flashing
  - Breathing patterns
- Robust error handling and recovery

**Location:** `/ColorControlCode/MultiLightHouseLightControlCode/`

### 🖥️ NCURSES DVD Screensaver
A nostalgic terminal-based animation recreating the classic DVD screensaver.

**Features:**
- Smooth bouncing animation
- Configurable speed and text
- Terminal-responsive sizing

**Location:** `/Experiments/NCURSES_DVD/`

### 🤖 LinkedIn Automation
Automated LinkedIn profile updater that syncs with LeetCode statistics.

**Features:**
- Automatic profile updates
- LeetCode API integration
- Headless browser operation

**Location:** `/Experiments/LinkedInUpdatingScript.py`

### 📚 Medical Terminology Parser
A tool for analyzing and breaking down medical terminology.

**Features:**
- Comprehensive medical prefix/suffix database
- Intelligent term separation
- Detailed meaning analysis

**Location:** `/TrulyRandomCode/USask_Anatomy_Midterm_Assistance_Code.py`

### 🔆 Windows Screen Brightness Control
PowerShell-based monitor brightness controller with various animation patterns.

**Features:**
- Multiple animation modes (Fade, Flash, Pulse)
- Configurable brightness ranges
- Hidden window operation option

**Location:** `/ColorControlCode/WindowsScreenBrightnessControl.ps1`

### 📊 Financial Analysis Practice
A collection of scripts exploring financial concepts and data visualization while working through University of Chicago's program materials.

**Programs:**
1. **Stock Analysis Tool** (`financial_analysis.py`)
   - Interactive GUI application for analyzing stock performance
   - Features:
     - Real-time stock data fetching via yfinance API
     - Dynamic P/E ratio calculation and visualization
     - EPS (Earnings Per Share) history tracking
     - Moving average calculations
     - Interactive plots with price trends
     - Customizable time period selection (1mo to 5y)
     - Professional-grade visualizations using matplotlib and seaborn
     - Loading animations and error handling
     - Responsive modern UI design

2. **Financial Calculator** (`financial_calculator.py`)
   - Command-line calculator for fundamental financial computations
   - Features:
     - Future Value (FV) calculations
     - Present Value (PV) calculations
     - Annuity payment computations
     - Robust error handling for invalid inputs
     - Clear documentation of financial formulas
     - Interactive user prompts for inputs

3. **Trading Strategy Backtester** (`backtesting.py`)
   - Comprehensive framework for evaluating trading strategies
   - Features:
     - Vectorized backtesting using VectorBT for efficient performance
     - Moving Average Crossover strategy implementation
     - Detailed performance metrics (Sharpe ratio, drawdowns, win rate)
     - Automated visualization of results with entry/exit points
     - Benchmark comparison against market indices
     - Monthly returns heatmaps and drawdown analysis
     - HTML report generation with QuantStats
     - Robust error handling and progress tracking
     - Non-interactive plotting for automation compatibility

**Learning Focus:**
- Financial mathematics implementation
- Data visualization best practices
- Market analysis methodologies
- Statistical modeling
- API integration for financial data
- GUI development with tkinter
- Error handling and user experience
- Real-time data processing
- Algorithmic trading strategy evaluation

**Location:** `/financial_practice/`

## 🛠️ Setup & Requirements

Each project has its own dependencies and requirements. Please refer to the individual project directories for specific setup instructions.

## 📝 License
MIT License - Feel free to use and modify the code as needed.

