document.addEventListener('DOMContentLoaded', async () => {
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  const goToWatchLater = document.getElementById('goToWatchLater');
  const navInstruction = document.getElementById('navInstruction');
  const reviewButton = document.getElementById('reviewButton');
  const statusDiv = document.getElementById('status');
  const progressDiv = document.getElementById('progress');
  const countSpan = document.getElementById('count');
  const autoRefreshCheckbox = document.getElementById('autoRefresh');
  const breakIntervalSelect = document.getElementById('breakInterval');
  const breakDurationSelect = document.getElementById('breakDuration');

  // Apply tertiary style to Review button initially
  reviewButton.classList.add('tertiary');
  
  // Apply primary action style to Start button initially
  startButton.classList.add('primary-action');

  let currentTab = null;
  let videosRemoved = 0;
  let countdownTimer = null;
  
  // Load settings
  let settings = await browser.storage.local.get('settings').then(result => {
    return result.settings || {
      autoRefresh: true,
      breakInterval: 600,
      breakDuration: 5
    };
  });

  // Initialize settings UI
  autoRefreshCheckbox.checked = settings.autoRefresh;
  breakIntervalSelect.value = settings.breakInterval;
  if (breakDurationSelect && settings.breakDuration) {
    breakDurationSelect.value = settings.breakDuration;
  }

  // Helper functions for basic UI operations
  const updateStatus = (text, className = '') => {
    statusDiv.textContent = text;
    statusDiv.className = 'status ' + className;
    
    if (text.includes('Cleaning process stopped')) {
      setActiveMode('ready');
    }
  };
  
  const updateCount = (count) => {
    videosRemoved = count;
    countSpan.textContent = count;
  };

  // Simple UI state management
  const setActiveMode = (mode) => {
    if (mode === 'ready') {
      stopButton.classList.add('hidden');
      startButton.classList.remove('hidden');
      startButton.disabled = false;
    } else if (mode === 'cleaning') {
      startButton.classList.add('hidden');
      startButton.disabled = true;
      stopButton.classList.remove('hidden');
      progressDiv.classList.remove('hidden');
    }
  };
  
  // Clear countdown timer utility
  const clearActiveCountdown = () => {
    if (countdownTimer) {
      clearInterval(countdownTimer);
      countdownTimer = null;
    }
  };

  // Save settings
  const saveSetting = (key, value) => {
    settings[key] = value;
    browser.storage.local.set({ settings });
  };

  // Update UI based on current page
  const updateInterface = async () => {
    const tabs = await browser.tabs.query({active: true, currentWindow: true});
    if (tabs.length === 0) return;
    
    currentTab = tabs[0];
    const isWatchLaterPage = currentTab.url.includes('youtube.com/playlist?list=WL');
    
    // Handle navigation button visibility - ONLY show when NOT on Watch Later page
    if (isWatchLaterPage) {
      goToWatchLater.classList.add('hidden');
      navInstruction.classList.add('hidden');
      startButton.classList.remove('hidden');
      
      // Only apply highlight if we haven't completed cleaning successfully
      if (!reviewButton.classList.contains('highlight')) {
        startButton.classList.add('highlight');
      }
      
      progressDiv.classList.remove('hidden');
      updateStatus('Ready to clean your Watch Later playlist. Click Start Cleaning to begin.', 'success');
    } else {
      startButton.classList.add('hidden');
      startButton.classList.remove('highlight');
      stopButton.classList.add('hidden');
      goToWatchLater.classList.remove('hidden');
      goToWatchLater.classList.add('highlight');
      navInstruction.classList.remove('hidden');
      progressDiv.classList.add('hidden');
      updateStatus('Please navigate to your Watch Later playlist to use this extension.', 'warning');
    }
  };

  // Initialize UI on popup open
  await updateInterface();
  
  // Settings event listeners
  autoRefreshCheckbox.addEventListener('change', () => {
    saveSetting('autoRefresh', autoRefreshCheckbox.checked);
  });

  breakIntervalSelect.addEventListener('change', () => {
    saveSetting('breakInterval', parseInt(breakIntervalSelect.value));
  });

  breakDurationSelect.addEventListener('change', () => {
    saveSetting('breakDuration', parseInt(breakDurationSelect.value));
  });
  
  // Listen for tab updates
  browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && currentTab && tabId === currentTab.id) {
      currentTab = tab;
      updateInterface();
    }
  });

  // Handle messages from content script
  browser.runtime.onMessage.addListener((message) => {
    if (message.type === 'log') {
      updateStatus(message.text, message.class);
    } else if (message.type === 'count') {
      videosRemoved = message.count;
      updateCount(message.count);
    } else if (message.type === 'error') {
      updateStatus(message.text, 'error');
      setActiveMode('ready');
      clearActiveCountdown();
    } else if (message.type === 'needsRefresh') {
      const currentCount = message.videosRemoved || videosRemoved;
      
      if (settings.autoRefresh) {
        clearActiveCountdown();
        
        let countdownSeconds = 3;
        updateStatus(`Page needs to be refreshed. Refreshing in ${countdownSeconds} seconds...`, 'warning');
        
        countdownTimer = setInterval(() => {
          countdownSeconds--;
          if (countdownSeconds > 0) {
            updateStatus(`Page needs to be refreshed. Refreshing in ${countdownSeconds} seconds...`, 'warning');
          } else {
            clearActiveCountdown();
            updateStatus('Refreshing page now...', 'warning');
            
            browser.tabs.onUpdated.addListener(function resumeListener(tabId, info) {
              if (tabId === currentTab.id && info.status === 'complete') {
                browser.tabs.onUpdated.removeListener(resumeListener);
                
                let loadingSeconds = 2;
                updateStatus(`Page refreshed. Waiting ${loadingSeconds} seconds for YouTube to fully load...`, 'warning');
                
                countdownTimer = setInterval(() => {
                  loadingSeconds--;
                  if (loadingSeconds > 0) {
                    updateStatus(`Page refreshed. Waiting ${loadingSeconds} seconds for YouTube to fully load...`, 'warning');
                  } else {
                    clearActiveCountdown();
                    updateStatus('Resuming cleaning process...', 'success');
                    
                    browser.tabs.sendMessage(currentTab.id, { 
                      command: 'resume', 
                      count: currentCount,
                      settings: settings
                    });
                  }
                }, 1000);
              }
            });
            
            browser.tabs.reload(currentTab.id);
          }
        }, 1000);
      } else {
        updateStatus('Page needs to be refreshed. Click Start Cleaning to continue.', 'warning');
        localStorage.setItem('savedCount', currentCount.toString());
        setActiveMode('ready');
      }
    } else if (message.type === 'complete') {
      clearActiveCountdown();
      videosRemoved = 0;
      setActiveMode('ready');
      updateStatus(`Successfully removed ${message.count} videos!`, 'success');
      
      // After successful completion, swap styles between review and start buttons
      
      // Update review button: remove tertiary, add primary-action and highlight
      reviewButton.classList.remove('tertiary');
      reviewButton.classList.add('primary-action', 'highlight');
      
      // Update start button: remove primary-action and highlight, add tertiary
      startButton.classList.remove('primary-action', 'highlight');
      startButton.classList.add('tertiary');
    }
  });

  // Navigation button
  goToWatchLater.addEventListener('click', () => {
    updateStatus('Navigating to Watch Later playlist...', 'success');
    
    browser.tabs.update(currentTab.id, {
      url: 'https://www.youtube.com/playlist?list=WL'
    }).then(() => {
      browser.tabs.onUpdated.addListener(function listener(tabId, info) {
        if (tabId === currentTab.id && info.status === 'complete') {
          browser.tabs.onUpdated.removeListener(listener);
          
          setTimeout(() => {
            updateInterface();
            updateStatus('Watch Later playlist loaded. Click "Start Cleaning" when ready.', 'success');
          }, 1500);
        }
      });
    });
  });

  // Start button
  startButton.addEventListener('click', () => {
    const savedCount = parseInt(localStorage.getItem('savedCount') || '0');
    
    browser.tabs.sendMessage(currentTab.id, { 
      command: savedCount > 0 ? 'resume' : 'start',
      count: savedCount,
      settings: settings
    });
    
    if (savedCount > 0) {
      localStorage.removeItem('savedCount');
      videosRemoved = savedCount;
    }
    
    setActiveMode('cleaning');
  });

  // Stop button
  stopButton.addEventListener('click', () => {
    clearActiveCountdown();
    browser.tabs.sendMessage(currentTab.id, { command: 'stop' });
    updateStatus('Stopping cleaning process...', 'warning');
  });

  // Review button
  reviewButton.addEventListener('click', () => {
    browser.tabs.create({
      url: 'https://addons.mozilla.org/firefox/addon/youtube-watch-later-cleaner/'
    });
  });
}); 