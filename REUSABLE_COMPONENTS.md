# Reusable Tailwind CSS Components

Copy-paste ready components for your Flask application. Each component is fully styled with Tailwind CSS.

---

## Navigation Bars

### 1. Simple Navbar with Logo and Links

```html
<nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <!-- Logo -->
            <div class="flex items-center">
                <a href="/" class="text-2xl font-bold text-blue-600">
                    🚀 MyApp
                </a>
            </div>
            
            <!-- Links -->
            <div class="flex space-x-4">
                <a href="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition">
                    Home
                </a>
                <a href="/about" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition">
                    About
                </a>
                <a href="/login" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition">
                    Login
                </a>
            </div>
        </div>
    </div>
</nav>
```

### 2. Glassmorphism Navbar

```html
<nav class="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
                ✨ GlassNav
            </a>
            <div class="flex space-x-4">
                <a href="/" class="text-gray-700 hover:text-blue-600 transition">Home</a>
                <a href="/about" class="text-gray-700 hover:text-blue-600 transition">About</a>
                <button class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-2 rounded-lg transition shadow-md">
                    Get Started
                </button>
            </div>
        </div>
    </div>
</nav>
```

### 3. Navbar with User Profile

```html
<nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <div class="text-xl font-bold text-gray-800">Dashboard</div>
            
            <!-- User Profile -->
            <div class="flex items-center space-x-4">
                <span class="text-gray-700">Hello, <span class="font-semibold">John</span></span>
                <img src="https://via.placeholder.com/40" class="w-10 h-10 rounded-full border-2 border-blue-500">
                <a href="/logout" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition">
                    Logout
                </a>
            </div>
        </div>
    </div>
</nav>
```

---

## Buttons

### Primary Buttons

```html
<!-- Solid Button -->
<button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition duration-300">
    Click Me
</button>

<!-- Gradient Button -->
<button class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-lg shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105">
    Gradient Button
</button>

<!-- Outline Button -->
<button class="bg-transparent border-2 border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white font-semibold px-6 py-3 rounded-lg transition duration-300">
    Outline Button
</button>

<!-- Pill Button -->
<button class="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-full shadow-md transition">
    Pill Button
</button>

<!-- Icon Button -->
<button class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-full shadow-lg transition">
    ❤️
</button>
```

---

## Cards

### 1. Simple Card

```html
<div class="bg-white rounded-xl shadow-lg p-6">
    <h3 class="text-xl font-bold mb-3 text-gray-800">Card Title</h3>
    <p class="text-gray-600 mb-4">
        This is a simple card component with some content inside.
    </p>
    <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition">
        Learn More
    </button>
</div>
```

### 2. Card with Image

```html
<div class="bg-white rounded-xl shadow-lg overflow-hidden">
    <img src="https://via.placeholder.com/400x200" class="w-full h-48 object-cover">
    <div class="p-6">
        <h3 class="text-xl font-bold mb-2 text-gray-800">Image Card</h3>
        <p class="text-gray-600 mb-4">
            Beautiful card with an image at the top.
        </p>
        <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition w-full">
            View Details
        </button>
    </div>
</div>
```

### 3. Glassmorphic Card

```html
<div class="bg-white/60 backdrop-blur-lg rounded-2xl shadow-xl border border-gray-200 p-8">
    <div class="text-4xl mb-4">🎨</div>
    <h3 class="text-2xl font-bold mb-3 text-gray-800">Glass Card</h3>
    <p class="text-gray-700 mb-4">
        Modern glassmorphic effect with blur and transparency.
    </p>
    <button class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-lg shadow-md hover:shadow-lg transition">
        Explore
    </button>
</div>
```

### 4. Hoverable Card

```html
<div class="bg-white rounded-xl shadow-lg p-6 transform hover:scale-105 hover:shadow-2xl transition duration-300 cursor-pointer">
    <div class="text-3xl mb-3">⚡</div>
    <h3 class="text-xl font-bold mb-2 text-gray-800">Hover Me!</h3>
    <p class="text-gray-600">
        This card grows when you hover over it.
    </p>
</div>
```

---

## Forms

### 1. Simple Input

```html
<input 
    type="text" 
    placeholder="Enter your name"
    class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
>
```

### 2. Input with Label

```html
<div class="mb-4">
    <label class="block text-gray-700 font-semibold mb-2">Email Address</label>
    <input 
        type="email" 
        placeholder="you@example.com"
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
    >
</div>
```

### 3. Textarea

```html
<textarea 
    rows="4"
    placeholder="Write your message..."
    class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition resize-none"
></textarea>
```

### 4. Select Dropdown

```html
<select class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition">
    <option>Choose an option</option>
    <option>Option 1</option>
    <option>Option 2</option>
    <option>Option 3</option>
</select>
```

### 5. Complete Form

```html
<form class="bg-white rounded-xl shadow-lg p-8 max-w-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Contact Us</h2>
    
    <!-- Name -->
    <div class="mb-4">
        <label class="block text-gray-700 font-semibold mb-2">Name</label>
        <input 
            type="text" 
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
        >
    </div>
    
    <!-- Email -->
    <div class="mb-4">
        <label class="block text-gray-700 font-semibold mb-2">Email</label>
        <input 
            type="email" 
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
        >
    </div>
    
    <!-- Message -->
    <div class="mb-6">
        <label class="block text-gray-700 font-semibold mb-2">Message</label>
        <textarea 
            rows="4"
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition resize-none"
        ></textarea>
    </div>
    
    <!-- Submit -->
    <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-lg transition">
        Send Message
    </button>
</form>
```

---

## Alerts / Flash Messages

### Success Alert

```html
<div class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-r-lg shadow-sm mb-4">
    <p class="font-semibold">✅ Success!</p>
    <p class="text-sm">Your action was completed successfully.</p>
</div>
```

### Error Alert

```html
<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-r-lg shadow-sm mb-4">
    <p class="font-semibold">❌ Error!</p>
    <p class="text-sm">Something went wrong. Please try again.</p>
</div>
```

### Warning Alert

```html
<div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-r-lg shadow-sm mb-4">
    <p class="font-semibold">⚠️ Warning!</p>
    <p class="text-sm">Please be careful with this action.</p>
</div>
```

### Info Alert

```html
<div class="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded-r-lg shadow-sm mb-4">
    <p class="font-semibold">ℹ️ Info</p>
    <p class="text-sm">Here's some information you should know.</p>
</div>
```

---

## Hero Sections

### 1. Simple Hero

```html
<div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white py-20">
    <div class="max-w-4xl mx-auto text-center px-4">
        <h1 class="text-5xl font-bold mb-4">Welcome to Our App</h1>
        <p class="text-xl mb-8 text-blue-100">Build amazing things with Flask and Tailwind</p>
        <button class="bg-white text-blue-600 font-bold px-8 py-4 rounded-lg shadow-lg hover:shadow-xl transition transform hover:scale-105">
            Get Started
        </button>
    </div>
</div>
```

### 2. Hero with Background Image

```html
<div class="relative bg-cover bg-center h-screen" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa');">
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black bg-opacity-50"></div>
    
    <!-- Content -->
    <div class="relative z-10 flex items-center justify-center h-full text-white text-center px-4">
        <div>
            <h1 class="text-6xl font-bold mb-4">Build The Future</h1>
            <p class="text-2xl mb-8">One line of code at a time</p>
            <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-10 py-4 rounded-lg transition">
                Start Building
            </button>
        </div>
    </div>
</div>
```

---

## Feature Grids

### 3-Column Feature Grid

```html
<div class="grid md:grid-cols-3 gap-8 py-12">
    <!-- Feature 1 -->
    <div class="bg-white rounded-xl shadow-lg p-8 text-center hover:shadow-2xl transition">
        <div class="text-5xl mb-4">🚀</div>
        <h3 class="text-xl font-bold mb-3 text-gray-800">Fast</h3>
        <p class="text-gray-600">Lightning-fast performance for your applications.</p>
    </div>
    
    <!-- Feature 2 -->
    <div class="bg-white rounded-xl shadow-lg p-8 text-center hover:shadow-2xl transition">
        <div class="text-5xl mb-4">🔒</div>
        <h3 class="text-xl font-bold mb-3 text-gray-800">Secure</h3>
        <p class="text-gray-600">Bank-level security for your data.</p>
    </div>
    
    <!-- Feature 3 -->
    <div class="bg-white rounded-xl shadow-lg p-8 text-center hover:shadow-2xl transition">
        <div class="text-5xl mb-4">✨</div>
        <h3 class="text-xl font-bold mb-3 text-gray-800">Modern</h3>
        <p class="text-gray-600">Built with the latest technologies.</p>
    </div>
</div>
```

---

## Chat Components

### User Message (Right)

```html
<div class="flex justify-end mb-4">
    <div class="bg-blue-500 text-white rounded-lg rounded-tr-none px-6 py-3 max-w-xs shadow-md">
        <p>This is a user message!</p>
    </div>
</div>
```

### AI/Bot Message (Left)

```html
<div class="flex justify-start mb-4">
    <div class="bg-gray-200 text-gray-800 rounded-lg rounded-tl-none px-6 py-3 max-w-xs shadow-md">
        <p>This is an AI response!</p>
    </div>
</div>
```

### Chat Input

```html
<div class="flex space-x-4">
    <input 
        type="text" 
        placeholder="Type a message..."
        class="flex-1 px-6 py-4 border-2 border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500 transition"
    >
    <button class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-2xl shadow-lg transition">
        Send →
    </button>
</div>
```

---

## Loading Indicators

### Spinner

```html
<div class="flex justify-center items-center">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
</div>
```

### Dots

```html
<div class="flex space-x-2">
    <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
    <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
    <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
</div>
```

---

## Badges

```html
<!-- Status Badges -->
<span class="bg-green-100 text-green-800 text-xs font-semibold px-3 py-1 rounded-full">Active</span>
<span class="bg-red-100 text-red-800 text-xs font-semibold px-3 py-1 rounded-full">Inactive</span>
<span class="bg-yellow-100 text-yellow-800 text-xs font-semibold px-3 py-1 rounded-full">Pending</span>
<span class="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full">New</span>
```

---

## Tables

```html
<div class="overflow-x-auto">
    <table class="min-w-full bg-white rounded-lg overflow-hidden shadow-lg">
        <thead class="bg-gray-100">
            <tr>
                <th class="px-6 py-4 text-left text-gray-700 font-semibold">Name</th>
                <th class="px-6 py-4 text-left text-gray-700 font-semibold">Email</th>
                <th class="px-6 py-4 text-left text-gray-700 font-semibold">Status</th>
                <th class="px-6 py-4 text-left text-gray-700 font-semibold">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b hover:bg-gray-50 transition">
                <td class="px-6 py-4">John Doe</td>
                <td class="px-6 py-4">john@example.com</td>
                <td class="px-6 py-4">
                    <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Active</span>
                </td>
                <td class="px-6 py-4">
                    <button class="text-blue-600 hover:text-blue-800">Edit</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

---

## Modals / Popups

```html
<!-- Modal Background -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <!-- Modal Content -->
    <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Modal Title</h2>
        <p class="text-gray-600 mb-6">
            This is a modal dialog. You can put any content here.
        </p>
        <div class="flex justify-end space-x-4">
            <button class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg transition">
                Cancel
            </button>
            <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition">
                Confirm
            </button>
        </div>
    </div>
</div>
```

---

## Complete Page Layouts

### Landing Page Layout

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 via-white to-purple-50">
    
    <!-- Navbar -->
    <nav class="bg-white/80 backdrop-blur-md shadow-sm">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold text-blue-600">🚀 MyApp</div>
            <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition">
                Sign In
            </button>
        </div>
    </nav>
    
    <!-- Hero -->
    <div class="max-w-7xl mx-auto px-4 py-20 text-center">
        <h1 class="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
            Welcome to the Future
        </h1>
        <p class="text-xl text-gray-600 mb-8">Build amazing things with our platform</p>
        <button class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-bold px-10 py-4 rounded-xl shadow-lg transition transform hover:scale-105">
            Get Started →
        </button>
    </div>
    
    <!-- Features -->
    <div class="max-w-7xl mx-auto px-4 py-12 grid md:grid-cols-3 gap-8">
        <!-- Feature cards here -->
    </div>
    
</body>
</html>
```

---

**Pro Tip**: All these components are modular! Mix and match them to create your perfect UI.
