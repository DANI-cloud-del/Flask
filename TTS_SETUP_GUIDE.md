# 🎙️ Text-to-Speech (TTS) Setup Guide

## ✅ What's Been Added

### New Files:
1. **`templates/settings.html`** - Complete settings page with TTS controls
2. **Updated `app.py`** - Added `/settings` route

### Features:
- ✅ TTS enable/disable toggle
- ✅ Auto-read responses toggle
- ✅ Voice selection (all system voices)
- ✅ Speech rate control (0.5x - 2x)
- ✅ Pitch control (0.5 - 2)
- ✅ Volume control (0-100%)
- ✅ Test voice button
- ✅ Settings persist in localStorage
- ✅ Settings link in chat header
- ✅ Clear all conversations button

---

## 🚀 Installation Steps

### Step 1: Pull Latest Code
```bash
cd ~/Desktop/Flask
git fetch origin main
git reset --hard origin/main
```

### Step 2: Add Settings Icon to Chat Header

Open `templates/chat.html` and find the header actions section (around line 55).

Find this code:
```html
<div class="flex items-center space-x-2">
    <button id="deleteConversationBtn" ...>
```

Replace with:
```html
<div class="flex items-center space-x-2">
    <!-- Settings Button -->
    <a href="{{ url_for('settings') }}" class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition" title="Settings">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
        </svg>
    </a>
    
    <!-- Delete Button -->
    <button id="deleteConversationBtn" onclick="deleteCurrentConversation()" class="hidden p-2 text-red-600 hover:bg-red-50 rounded-lg transition" title="Delete chat">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
        </svg>
    </button>
    
    <!-- Logout Button -->
    <a href="{{ url_for('logout') }}" class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition" title="Sign out">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
        </svg>
    </a>
</div>
```

### Step 3: Add TTS Integration to Chat

In `templates/chat.html`, add this code **before the closing `</script>` tag** (at the very end of the script section):

```javascript
// ============================================================================
// TEXT-TO-SPEECH INTEGRATION
// ============================================================================

let availableVoices = [];

// Load voices when available
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => {
        availableVoices = speechSynthesis.getVoices();
    };
}
availableVoices = speechSynthesis.getVoices();

// Speak text function
function speakText(text) {
    // Check if TTS and auto-read are enabled
    const ttsEnabled = localStorage.getItem('tts_enabled') === 'true';
    const autoReadEnabled = localStorage.getItem('auto_read_enabled') === 'true';
    
    if (!ttsEnabled || !autoReadEnabled) {
        return; // TTS or auto-read is disabled
    }
    
    // Stop any current speech
    speechSynthesis.cancel();
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Apply settings from localStorage
    const voiceName = localStorage.getItem('tts_voice');
    if (voiceName && availableVoices.length > 0) {
        const voice = availableVoices.find(v => v.name === voiceName);
        if (voice) utterance.voice = voice;
    }
    
    utterance.rate = parseFloat(localStorage.getItem('tts_rate') || '1.0');
    utterance.pitch = parseFloat(localStorage.getItem('tts_pitch') || '1.0');
    utterance.volume = parseFloat(localStorage.getItem('tts_volume') || '100') / 100;
    
    // Speak
    speechSynthesis.speak(utterance);
}
```

### Step 4: Update `addMessageToUI` Function

In `templates/chat.html`, find the `addMessageToUI` function and modify the assistant case.

Find this section:
```javascript
} else if (type === 'assistant') {
    messageDiv.innerHTML = `
        <div class="flex items-start space-x-3 mb-4">
            ...
        </div>
    `;
}
```

Change it to:
```javascript
} else if (type === 'assistant') {
    messageDiv.innerHTML = `
        <div class="flex items-start space-x-3 mb-4">
            <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mt-1">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
            </div>
            <div class="flex-1">
                <p class="text-gray-800 whitespace-pre-wrap leading-relaxed">${escapeHtml(content)}</p>
            </div>
        </div>
    `;
    
    // Auto-read response with TTS
    speakText(content);
}
```

---

## 🎯 Testing

### 1. Start the Server
```bash
python app.py
```

### 2. Go to Settings
1. Visit `http://localhost:5001`
2. Click the **gear icon** (⚙️) in the top-right header
3. You should see the Settings page

### 3. Configure TTS
1. **Enable TTS** - Toggle the first switch
2. **Select a voice** - Choose from the dropdown
3. **Adjust settings** - Rate, pitch, volume
4. **Click "Test Voice"** - You should hear a test message
5. **Enable Auto-read** - Toggle the second switch

### 4. Test in Chat
1. Go back to chat (click the back arrow)
2. Send a message: "Hello, test TTS"
3. The AI response should be read aloud automatically!

---

## 🔧 Troubleshooting

### Issue: No voices in dropdown
**Solution**: Refresh the page. Some browsers load voices asynchronously.

### Issue: TTS not working
**Check**:
1. Both toggles are ON (TTS + Auto-read)
2. Volume is not 0
3. Browser supports Web Speech API (Chrome, Edge, Safari)
4. System volume is not muted

### Issue: Settings icon not showing
**Solution**: Make sure you added the settings icon code in the correct location in `chat.html`

---

## 📝 Settings Storage

All settings are stored in browser's localStorage:
- `tts_enabled` - TTS on/off
- `auto_read_enabled` - Auto-read on/off
- `tts_voice` - Selected voice name
- `tts_rate` - Speech rate (0.5 - 2.0)
- `tts_pitch` - Speech pitch (0.5 - 2.0)
- `tts_volume` - Volume (0 - 100)

---

## 🎨 Features Overview

### Settings Page
- **Profile Section** - Shows user info
- **TTS Section** - Enable/disable with voice controls
- **Auto-read Section** - Toggle automatic reading
- **Theme Section** - Placeholder for dark mode (coming soon)
- **Danger Zone** - Clear all conversations

### Chat Integration
- **Automatic Reading** - AI responses read aloud when enabled
- **Settings Persistence** - Preferences saved across sessions
- **Non-intrusive** - Works silently in background
- **Stop on Navigation** - Speech stops when you leave page

---

## 🚀 Next Steps

1. Test all features
2. Adjust voice settings to your preference
3. Try different voices and rates
4. Optional: Add manual read buttons for individual messages
5. Optional: Add keyboard shortcuts to toggle TTS

---

## ✅ Checklist

- [ ] Pulled latest code
- [ ] Added settings icon to chat header
- [ ] Added TTS functions to chat.html
- [ ] Updated addMessageToUI function
- [ ] Tested settings page loads
- [ ] Tested TTS voice selection
- [ ] Tested auto-read in chat
- [ ] Verified settings persist after refresh

---

**Enjoy your new TTS feature! 🎙️**
