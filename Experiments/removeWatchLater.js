/**
 * YouTube Watch Later Playlist Cleaner
 * A utility script to automatically remove videos from YouTube's Watch Later playlist.
 * Run this in the browser console while on the Watch Later playlist page.
 */

/**
 * Utility function to pause execution for a specified duration
 * @param {number} ms - Time to sleep in milliseconds
 * @returns {Promise<void>}
 */
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Recursively removes videos from the Watch Later playlist one by one
 * @param {number} [count=0] - Counter for tracking the number of videos removed
 * @returns {Promise<void>}
 */
async function removeNextVideo(count = 0) {
  // Select the first video in your Watch Later playlist
  const video = document.querySelector('ytd-playlist-video-renderer');
  if (!video) {
    console.log(`All videos removed! Total removed: ${count}`);
    return;
  }
  
  // Find and click the action (menu) button
  const menuButton = video.querySelector('button[aria-label="Action menu"]');
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
    // Wait a bit to allow the playlist to update
    await sleep(300);
  } else {
    console.log('Remove option not found after several attempts. Skipping this video.');
    await sleep(300);
  }
  
  // Process the next video recursively
  removeNextVideo(count);
}

// Initialize the removal process
removeNextVideo();
