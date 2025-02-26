/**
 * YouTube Watch Later Cleaner Content Script
 * This script handles the actual video removal functionality by interacting with YouTube's DOM.
 * It uses a robust, language-agnostic approach with multiple fallback strategies.
 */

// Utility function to pause execution
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// Message handling utilities
const log = (text, className = '') => 
  browser.runtime.sendMessage({ type: 'log', text, class: className });

// Update the counter with debouncing to ensure it's more responsive
const updateCount = (() => {
  let lastUpdate = 0;
  let pendingCount = null;
  let updateTimer = null;
  
  return (count) => {
    const now = Date.now();
    pendingCount = count;
    
    // If we've recently updated, wait a bit before updating again
    if (now - lastUpdate < 200 && !updateTimer) {
      updateTimer = setTimeout(() => {
        if (pendingCount !== null) {
          browser.runtime.sendMessage({ type: 'count', count: pendingCount });
          lastUpdate = Date.now();
          pendingCount = null;
        }
        updateTimer = null;
      }, 200);
    } else if (!updateTimer) {
      // If it's been a while since our last update, update immediately
      browser.runtime.sendMessage({ type: 'count', count });
      lastUpdate = now;
      pendingCount = null;
    }
  };
})();

const reportError = text => 
  browser.runtime.sendMessage({ type: 'error', text });

/**
 * Attempts to find an element using multiple strategies
 * Each strategy is tried in order until one succeeds
 * @param {Array<Function>} strategies - Array of functions that return elements
 * @param {number} maxAttempts - Maximum number of retry attempts
 * @param {number} delayMs - Delay between attempts in milliseconds
 * @returns {Promise<Element|null>} Found element or null
 */
async function findElement(strategies, maxAttempts = 3, delayMs = 200) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    for (const strategy of strategies) {
      const element = strategy();
      if (element) return element;
    }
    await sleep(delayMs);
  }
  return null;
}

/**
 * Finds the playlist menu button by its 3-dot icon
 * @returns {Element|null} The menu button element or null
 */
function findPlaylistMenuButtonByIcon() {
  // Path data for the 3-dot icon
  const threeDotIconPathData = "M12 16.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5-1.5-.67-1.5-1.5.67-1.5 1.5-1.5zM10.5 12c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5-.67-1.5-1.5-1.5-1.5.67-1.5 1.5zm0-6c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5-.67-1.5-1.5-1.5-1.5.67-1.5 1.5z";

  // Search for a button containing an SVG path element with the specific d attribute
  return document.querySelector(`ytd-playlist-header-renderer yt-icon-button button yt-icon svg path[d="${threeDotIconPathData}"]`)?.closest('button');
}

/**
 * Finds the "Show unavailable videos" option by its eye icon
 * @returns {Element|null} The menu item element or null
 */
function findShowHiddenOptionByIcon() {
  // Path data for the eye icon (visibility icon)
  const eyeIconPathData = "M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z";

  // Find menu items in the popup
  const menuItems = document.querySelectorAll('ytd-menu-popup-renderer [role="menuitem"]');

  for (const menuItem of Array.from(menuItems)) {
    // Search for an SVG path element with the specific d attribute within each menu item
    const eyeIcon = menuItem.querySelector(`yt-icon svg path[d="${eyeIconPathData}"]`);
    if (eyeIcon) {
      return menuItem; // Found the menu item with the eye icon
    }
  }
  return null; // Not found
}

/**
 * Shows hidden/unavailable videos in the playlist
 * Uses multiple strategies to find and click the necessary UI elements
 * @returns {Promise<void>}
 */
async function showHiddenVideos() {
  // DOM Assumption: Playlist header contains a menu button
  const playlistMenuButton = await findElement([
    // Strategy 1: Icon-based detection - most robust, relies on the 3-dot icon
    findPlaylistMenuButtonByIcon
  ]);

  if (!playlistMenuButton) {
    log('Playlist menu button not found', 'error');
    return;
  }

  // Click the menu button and wait for popup to appear
  playlistMenuButton.click();
  await sleep(500);

  // DOM Assumption: Menu popup contains "Show unavailable videos" as a menu item
  const showHiddenOption = await findElement([
    // Strategy: Icon-based detection - relies on the eye icon
    findShowHiddenOptionByIcon
  ]);

  if (showHiddenOption) {
    showHiddenOption.click();
    await sleep(500);
  } else {
    log('Show hidden videos option not found', 'warning');
  }
}

/**
 * Checks the number of remaining videos in the playlist
 * Uses numeric extraction that works across all languages
 * @returns {Promise<{count: number, needsRefresh: boolean}>}
 */
async function checkRemainingVideos() {
  await sleep(1000);

  // DOM Assumption: Videos are rendered as playlist video elements
  const videoElements = document.querySelectorAll('ytd-playlist-video-renderer');
  // DOM Assumption: Video count is shown in the playlist byline
  const videoCountElement = document.querySelector('ytd-playlist-byline-renderer yt-formatted-string.byline-item');
  
  // If we can't find the video count element and there are no videos, we're probably empty
  if (!videoCountElement) {
    if (videoElements.length === 0) {
      log('No video count element and no videos found - playlist appears empty', 'success');
      return { count: 0, needsRefresh: false };
    }
    log('No video count element found, attempting refresh', 'warning');
    return { count: 0, needsRefresh: true };
  }
  
  const text = videoCountElement.textContent.trim();
  
  // Check for "No videos" or equivalent text that indicates an empty playlist
  if (text.match(/no videos/i) || text.match(/0 videos?/i)) {
    log('Playlist is empty (shows "No videos" or "0 videos")', 'success');
    return { count: 0, needsRefresh: false };
  }
  
  // Language-agnostic number extraction
  // Matches any number, ignoring surrounding text
  const match = text.match(/(\d+)(?:\D|$)/);
  const countFromText = match ? parseInt(match[1]) : 0;
  
  // If the count is 0 and there are no videos, we're done
  if (countFromText === 0 && videoElements.length === 0) {
    log('Playlist is empty (0 videos count and no visible videos)', 'success');
    return { count: 0, needsRefresh: false };
  }
  
  // If there are visible videos but the count is 0, YouTube's UI might be in a stale state
  if (videoElements.length > 0 && countFromText === 0) {
    log('Count shows 0 but videos are visible, attempting refresh', 'warning');
    return { count: 0, needsRefresh: true };
  }
  
  // If there are no videos visible but the count is non-zero, we definitely need to refresh
  if (videoElements.length === 0 && countFromText > 0) {
    log(`Count shows ${countFromText} but no videos are visible, attempting refresh`, 'warning');
    return { count: countFromText, needsRefresh: true };
  }
  
  return { 
    count: countFromText, 
    needsRefresh: false // Only refresh when specifically needed
  };
}

// Function to find the "Remove from Watch Later" option by its icon (No changes needed here)
function findRemoveOptionByIcon() {
  // ... (findRemoveOptionByIcon function remains the same) ...
  const menuItems = document.querySelectorAll('ytd-menu-popup-renderer [role="menuitem"]');
  const garbageIconPathData = "M11 17H9V8h2v9zm4-9h-2v9h2V8zm4-4v1h-1v16H6V5H5V4h4V3h6v1h4zm-2 1H7v15h10V5z";

  for (const menuItem of Array.from(menuItems)) {
      const garbageIcon = menuItem.querySelector(`yt-icon svg path[d="${garbageIconPathData}"]`);
      if (garbageIcon) {
          return menuItem;
      }
  }
  return null;
}

/**
 * Removes videos one by one from the playlist
 * Implements breaks to prevent overwhelming YouTube's servers
 * @param {number} count - Number of videos removed so far
 * @param {Object} settings - User settings for the removal process
 * @returns {Promise<void>}
 */
async function removeNextVideo(count = 0, settings) {
  // Check if the process has been stopped
  if (window.cleanerIsRunning === false) {
    log('Cleaning process stopped.', 'warning');
    return;
  }

  // DOM Assumption: Each video is a playlist video renderer element
  const video = document.querySelector('ytd-playlist-video-renderer');
  if (!video) {
    const { count: remaining, needsRefresh } = await checkRemainingVideos();
    
    // Only refresh if we need to and haven't tried too many times already
    const maxRefreshAttempts = 3;
    if (needsRefresh && window.cleanerRefreshAttempts < maxRefreshAttempts) {
      if (remaining > 0) {
        log(`Cleaned ${count} videos. ${remaining} videos remaining. Refreshing page...`, 'warning');
      } else {
        log(`No videos visible. Refreshing page to check for more videos (attempt ${window.cleanerRefreshAttempts + 1}/${maxRefreshAttempts})...`, 'warning');
      }
      
      // Increment refresh counter
      window.cleanerRefreshAttempts = (window.cleanerRefreshAttempts || 0) + 1;
      
      // Trigger refresh and wait for reload
      browser.runtime.sendMessage({ 
        type: 'needsRefresh', 
        videosRemoved: count, 
        videosRemaining: remaining 
      });
      
      return; // Exit and let the page reload
    }
    
    // If we've already refreshed multiple times with no videos, we're truly done
    log(`Successfully removed all ${count} videos!`, 'success');
    browser.runtime.sendMessage({ type: 'complete', count });
    window.cleanerIsRunning = false;
    return;
  }

  // Reset refresh attempts if we found videos to remove
  window.cleanerRefreshAttempts = 0;

  // DOM Assumption: Each video has a menu button with ARIA attributes
  const menuButton = await findElement([
    // Strategy 1: ARIA-based (most robust)
    () => video.querySelector('button[aria-label="Action menu"], button[aria-haspopup="true"]'),
    // Strategy 2: ID-based
    () => video.querySelector('#menu button'),
    // Strategy 3: Structure-based
    () => video.querySelector('ytd-menu-renderer button')
  ]);

  if (!menuButton) {
    await sleep(200);
    return removeNextVideo(count, settings);
  }

  menuButton.click();
  await sleep(300); // Increased from 200ms to give the menu more time to open

  // Try multiple strategies to find the "Remove" option in the video menu, prioritizing icon-based detection
  const removeOption = await findElement([
    // Strategy 1: Icon-based detection - most robust, relies on the garbage icon
    findRemoveOptionByIcon, 
    // Strategy 2: ARIA role and position - Fallback if icon detection fails, now targets 3rd child
    () => document.querySelector('ytd-menu-popup-renderer tp-yt-paper-listbox [role="menuitem"]:nth-child(3)'),
  ], 4, 250); // Increased attempts and delay to give more chance to find the option

  if (removeOption) {
    removeOption.click();
    count++;
    updateCount(count);
    await sleep(700); // Increased from 500ms to give YouTube more time to process the removal
  } else {
    // If we can't find the remove option, close any open menu by clicking elsewhere
    document.body.click();
    log('Remove option not found, retrying...', 'warning');
    await sleep(500);
  }

  if (count > 0 && count % settings.breakInterval === 0) {
    log(`Taking a ${settings.breakDuration || 5} minute break after removing ${count} videos...`, 'warning');
    await sleep((settings.breakDuration || 5) * 60000); // Configurable break duration in minutes
  }

  // Only call once with a return to ensure proper flow control
  return removeNextVideo(count, settings);
}

// Listen for messages from popup
browser.runtime.onMessage.addListener(async (message) => {
  if (message.command === 'start') {
    if (!window.location.href.match(/youtube\.com\/playlist\?list=WL/)) {
      reportError('This script only works on YouTube Watch Later playlist page.');
      return;
    }
    
    try {
      // Default settings if not provided
      const settings = message.settings || { 
        autoRefresh: true, 
        breakInterval: 600,
        breakDuration: 5 // Default 5 minutes
      };
      
      log('Starting to clean your Watch Later playlist...', 'success');
      
      // Store a flag to track if the script is running and initialize refresh counter
      window.cleanerIsRunning = true;
      window.cleanerRefreshAttempts = 0;
      
      await showHiddenVideos();
      await removeNextVideo(0, settings);
    } catch (error) {
      reportError(`An error occurred: ${error.message}`);
    }
  } else if (message.command === 'stop') {
    window.cleanerIsRunning = false;
    log('Cleaning process stopped by user.', 'warning');
  } else if (message.command === 'resume') {
    // Allow resuming after page reload
    if (message.count && message.count > 0) {
      log(`Resuming cleaning. ${message.count} videos removed so far.`, 'success');
      window.cleanerIsRunning = true;
      await sleep(1000); // Give the page a moment to fully initialize
      await showHiddenVideos();
      await removeNextVideo(message.count, message.settings || {
        autoRefresh: true,
        breakInterval: 600,
        breakDuration: 5
      });
    }
  }
}); 