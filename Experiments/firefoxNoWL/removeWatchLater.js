/**
 * YouTube Watch Later Playlist Cleaner
 * A utility script to automatically remove videos from YouTube's Watch Later playlist.
 * Run this in the browser console while on the Watch Later playlist page.
 */

// Add script validation at the start
(function() {
  if (!window.location.href.match(/youtube\.com\/playlist\?list=WL/)) {
    console.log('This script only works on YouTube Watch Later playlist page.');
    // Clean up any existing intervals/observers if they exist
    if (window.watchLaterCleanupObserver) {
      window.watchLaterCleanupObserver.disconnect();
      delete window.watchLaterCleanupObserver;
    }
    return;
  }
})();

/**
 * Utility function to pause execution for a specified duration
 * @param {number} ms - Time to sleep in milliseconds
 * @returns {Promise<void>}
 */
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Shows hidden videos in the playlist
 * @returns {Promise<void>}
 */
async function showHiddenVideos() {
  // Find and click the playlist menu button using a reasonable selector
  const playlistMenuButton = document.querySelector('ytd-playlist-header-renderer ytd-menu-renderer button');
  if (!playlistMenuButton) {
    console.log('Playlist menu button not found');
    return;
  }
  
  playlistMenuButton.click();
  await sleep(500);
  
  // Find and click the "Show unavailable videos" option using more specific XPath
  let showHiddenOption = null;
  let attempts = 0;
  while (!showHiddenOption && attempts < 3) {
    showHiddenOption = document.evaluate(
      '//ytd-menu-navigation-item-renderer//yt-formatted-string[text()="Show unavailable videos"]',
      document,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null
    ).singleNodeValue;
    if (!showHiddenOption) {
      await sleep(200);
      attempts++;
    }
  }
  
  if (showHiddenOption) {
    // Click the parent tp-yt-paper-item for better reliability
    const clickTarget = showHiddenOption.closest('tp-yt-paper-item');
    if (clickTarget) {
      clickTarget.click();
    } else {
      showHiddenOption.click();
    }
    await sleep(500);
  } else {
    console.log('Show hidden videos option not found after multiple attempts');
  }
}

/**
 * Checks if there are still videos in the playlist that need rendering
 * @returns {Object} Object containing count of remaining videos and whether refresh is needed
 */
async function checkRemainingVideos() {
  // Add a delay to allow YouTube's UI to update
  await sleep(1000);

  const videoElements = document.querySelectorAll('ytd-playlist-video-renderer');
  const videoCountElement = document.querySelector('ytd-playlist-byline-renderer yt-formatted-string.byline-item');
  
  // If there are no actual video elements, consider the playlist empty
  if (videoElements.length === 0) {
    return { count: 0, needsRefresh: false };
  }

  if (!videoCountElement) {
    console.log('Debug: No video count element found');
    return { count: 0, needsRefresh: false };
  }

  const text = videoCountElement.textContent.trim();
  console.log('Debug: Video count text:', text);

  if (text === 'No videos') {
    console.log('Debug: "No videos" detected');
    return { count: 0, needsRefresh: false };
  }

  const match = text.match(/(\d+)\s+videos?/);
  if (match) {
    const count = parseInt(match[1]);
    console.log('Debug: Found video count:', count);
    // Only suggest refresh if we actually see video elements
    return { count, needsRefresh: count > 0 && videoElements.length > 0 };
  }

  console.log('Debug: No match found in text');
  return { count: 0, needsRefresh: false };
}

/**
 * Recursively removes videos from the Watch Later playlist one by one
 * @param {number} [count=0] - Counter for tracking the number of videos removed
 * @returns {Promise<void>}
 */
async function removeNextVideo(count = 0) {
  const video = document.querySelector('ytd-playlist-video-renderer');
  if (!video) {
    const { count: remaining, needsRefresh } = await checkRemainingVideos();
    console.log('Debug: Remaining count:', remaining, 'Needs refresh:', needsRefresh);
    
    if (needsRefresh && remaining > 0) {  // Only show refresh message if there are actually videos remaining
      console.log(`
=== YouTube Watch Later Cleanup Status ===
Videos removed: ${count}
Videos remaining: ${remaining}
Action needed: Please refresh the page and run the script again
=======================================
      `);
    } else {
      console.log(`All videos removed! Total removed: ${count}`);
    }
    return;
  }
  
  // Try the standard menu button first, then fallback to the hidden video menu button
  let menuButton = video.querySelector('button[aria-label="Action menu"]');
  if (!menuButton) {
    menuButton = video.querySelector('#menu button');
  }
  
  if (!menuButton) {
    console.log('Menu button not found, retrying...');
    await sleep(200);
    return removeNextVideo(count);
  }
  menuButton.click();
  await sleep(200);
  
  // Try up to 3 times to locate the "Remove from" option
  let removeOption = null;
  let attempts = 0;
  while (!removeOption && attempts < 3) {
    removeOption = document.evaluate(
      '//tp-yt-paper-item//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "remove from")]',
      document,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null
    ).singleNodeValue;
    if (!removeOption) {
      await sleep(200);
      attempts++;
    }
  }
  
  if (removeOption) {
    removeOption.click();
    count++;
    console.log(`Removed video #${count}`);
    // Wait a bit for YouTube to update the playlist
    await sleep(500);  // Increased from 300
  } else {
    console.log('Remove option not found, retrying...');
    await sleep(300);
  }
  
  // After every 600 videos, pause for 5 minutes to avoid overloading YouTube
  if (count > 0 && count % 600 === 0) {
    console.log(`Reached ${count} videos, taking a 5 minute break...`);
    await sleep(300000); // 5 minutes in milliseconds
  }
  
  // Process the next video
  removeNextVideo(count);
}

// Add URL change detection
window.watchLaterCleanupObserver = new MutationObserver((mutations) => {
  if (!window.location.href.match(/youtube\.com\/playlist\?list=WL/)) {
    console.log('Navigated away from Watch Later playlist. Cleaning up script...');
    window.watchLaterCleanupObserver.disconnect();
    delete window.watchLaterCleanupObserver;
  }
});

// Start observing URL changes
window.watchLaterCleanupObserver.observe(document.querySelector('title'), {
  subtree: true,
  characterData: true,
  childList: true
});

// Initialize only if we're on the correct page
(async () => {
  if (window.location.href.match(/youtube\.com\/playlist\?list=WL/)) {
    await showHiddenVideos();
    removeNextVideo();
  }
})();
