/**
 * Malayalam Mode Indicator for Chat Interface
 * Shows a visual indicator when Malayalam mode is active
 */

// Check Malayalam mode on page load
document.addEventListener('DOMContentLoaded', () => {
    updateMalayalamIndicator();
});

// Update Malayalam mode indicator
function updateMalayalamIndicator() {
    const malayalamMode = localStorage.getItem('malayalam_mode') === 'true';
    const indicator = document.getElementById('malayalamIndicator');
    
    if (indicator) {
        indicator.classList.toggle('hidden', !malayalamMode);
    }
}

// Add Malayalam mode to all chat messages
function getMalayalamMode() {
    return localStorage.getItem('malayalam_mode') === 'true';
}
