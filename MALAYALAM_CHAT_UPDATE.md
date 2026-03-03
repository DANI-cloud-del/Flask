# 💬 Update chat.html for Malayalam Mode

## Quick Update Required

To complete Malayalam mode integration, update the `sendMessage` function in `templates/chat.html`:

### Find this code (around line 300):

```javascript
const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: message,
        conversation_id: currentConversationId
    })
});
```

### Replace with this:

```javascript
const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: message,
        conversation_id: currentConversationId,
        malayalam_mode: localStorage.getItem('malayalam_mode') === 'true'  // ADD THIS LINE
    })
});
```

---

## Optional: Add Visual Indicator

Add this HTML after the header in chat.html (around line 30):

```html
<!-- Malayalam Mode Indicator -->
<div id="malayalamIndicator" class="hidden bg-indigo-100 border-l-4 border-indigo-600 p-3 mb-4">
    <div class="flex items-center">
        <svg class="w-5 h-5 text-indigo-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
        </svg>
        <div>
            <p class="text-sm font-medium text-indigo-800">മലയാളം മോഡ് സജീവം (Malayalam Mode Active)</p>
            <p class="text-xs text-indigo-600">Type in English - AI responds in Malayalam</p>
        </div>
    </div>
</div>
```

Add this JavaScript at the end of chat.html:

```javascript
// Show Malayalam indicator if enabled
if (localStorage.getItem('malayalam_mode') === 'true') {
    document.getElementById('malayalamIndicator')?.classList.remove('hidden');
}
```

---

## ✅ That's It!

After this one-line change, Malayalam mode will work perfectly:
1. Type in English
2. Message gets translated to Malayalam
3. AI responds in Malayalam
4. Malayalam voice reads it aloud

🎉 **Malayalam mode is now fully functional!**
