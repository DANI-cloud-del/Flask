# Tailwind CSS Cheat Sheet for Beginners

Simple guide to styling with Tailwind CSS. No jargon, just what you need.

---

## What is Tailwind CSS?

Tailwind is a CSS framework that lets you style HTML using short class names instead of writing CSS files.

**Example:**
```html
<!-- Old way: Write CSS -->
<style>
  .my-button {
    background-color: blue;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
  }
</style>
<button class="my-button">Click me</button>

<!-- Tailwind way: Use class names -->
<button class="bg-blue-500 text-white px-6 py-3 rounded-lg">Click me</button>
```

Both look the same, but Tailwind is faster once you know the class names.

---

## How to Add Tailwind to Your Project

### Quick Method (CDN - for workshop)

Add this line inside the `<head>` tag of your HTML file:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

That's it! Now you can use Tailwind classes.

**Complete example:**
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div class="bg-blue-500 text-white p-4">
        Hello Tailwind!
    </div>
</body>
</html>
```

---

## Color Classes

### Text Colors

Change text color:
```html
<p class="text-red-500">Red text</p>
<p class="text-blue-500">Blue text</p>
<p class="text-green-500">Green text</p>
<p class="text-gray-500">Gray text</p>
<p class="text-black">Black text</p>
<p class="text-white">White text</p>
```

**Color intensity:** Numbers go from 50 (lightest) to 950 (darkest)
```html
<p class="text-blue-100">Very light blue</p>
<p class="text-blue-300">Light blue</p>
<p class="text-blue-500">Medium blue</p>
<p class="text-blue-700">Dark blue</p>
<p class="text-blue-900">Very dark blue</p>
```

### Background Colors

Change background color (same as text colors):
```html
<div class="bg-red-500">Red background</div>
<div class="bg-blue-500">Blue background</div>
<div class="bg-green-500">Green background</div>
<div class="bg-gray-100">Light gray background</div>
```

### Available Colors

- `red`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`
- `gray`, `slate`, `zinc`, `neutral`, `stone`
- `black`, `white`
- `indigo`, `violet`, `cyan`, `teal`, `emerald`, `lime`, `amber`, `rose`, `fuchsia`, `sky`

---

## Spacing (Padding & Margin)

### Padding (space inside)

```html
<!-- All sides -->
<div class="p-4">Padding on all sides</div>

<!-- Specific sides -->
<div class="pt-4">Padding top</div>
<div class="pb-4">Padding bottom</div>
<div class="pl-4">Padding left</div>
<div class="pr-4">Padding right</div>

<!-- Horizontal (left + right) -->
<div class="px-4">Padding left and right</div>

<!-- Vertical (top + bottom) -->
<div class="py-4">Padding top and bottom</div>
```

### Margin (space outside)

Same as padding, but use `m` instead of `p`:
```html
<div class="m-4">Margin on all sides</div>
<div class="mt-4">Margin top</div>
<div class="mb-4">Margin bottom</div>
<div class="mx-4">Margin left and right</div>
<div class="my-4">Margin top and bottom</div>
```

### Spacing Scale

| Class | Size | Pixels |
|-------|------|--------|
| `p-0` | 0 | 0px |
| `p-1` | 0.25rem | 4px |
| `p-2` | 0.5rem | 8px |
| `p-3` | 0.75rem | 12px |
| `p-4` | 1rem | 16px |
| `p-5` | 1.25rem | 20px |
| `p-6` | 1.5rem | 24px |
| `p-8` | 2rem | 32px |
| `p-10` | 2.5rem | 40px |
| `p-12` | 3rem | 48px |

**Most used:** `p-2`, `p-4`, `p-6`, `p-8`

---

## Text Styling

### Font Size

```html
<p class="text-xs">Extra small text</p>
<p class="text-sm">Small text</p>
<p class="text-base">Normal text (default)</p>
<p class="text-lg">Large text</p>
<p class="text-xl">Extra large text</p>
<p class="text-2xl">2x large text</p>
<p class="text-3xl">3x large text</p>
<p class="text-4xl">4x large text</p>
```

### Font Weight (bold/normal)

```html
<p class="font-light">Light text</p>
<p class="font-normal">Normal text</p>
<p class="font-medium">Medium text</p>
<p class="font-semibold">Semi-bold text</p>
<p class="font-bold">Bold text</p>
```

### Text Alignment

```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
```

---

## Width & Height

### Width

```html
<!-- Fixed width -->
<div class="w-32">Width 128px</div>
<div class="w-64">Width 256px</div>

<!-- Percentage width -->
<div class="w-1/2">Width 50%</div>
<div class="w-1/3">Width 33.33%</div>
<div class="w-2/3">Width 66.66%</div>
<div class="w-full">Width 100%</div>

<!-- Screen width -->
<div class="w-screen">Full screen width</div>
```

### Height

Same as width, but use `h` instead of `w`:
```html
<div class="h-32">Height 128px</div>
<div class="h-screen">Full screen height</div>
```

---

## Flexbox (Layout)

Flexbox helps arrange items horizontally or vertically.

### Basic Flex Container

```html
<div class="flex">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```
Items appear in a row (horizontal).

### Flex Direction

```html
<!-- Horizontal (default) -->
<div class="flex flex-row">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<!-- Vertical -->
<div class="flex flex-col">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

### Justify Content (horizontal alignment)

```html
<div class="flex justify-start">Items at start</div>
<div class="flex justify-center">Items in center</div>
<div class="flex justify-end">Items at end</div>
<div class="flex justify-between">Items spread with space between</div>
<div class="flex justify-around">Items spread with space around</div>
```

### Align Items (vertical alignment)

```html
<div class="flex items-start">Items at top</div>
<div class="flex items-center">Items in center</div>
<div class="flex items-end">Items at bottom</div>
```

### Spacing Between Items

```html
<!-- Horizontal spacing -->
<div class="flex space-x-4">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>

<!-- Vertical spacing -->
<div class="flex flex-col space-y-4">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

---

## Borders & Rounded Corners

### Borders

```html
<!-- Add border -->
<div class="border">Has border</div>

<!-- Border width -->
<div class="border-2">Thicker border</div>
<div class="border-4">Even thicker</div>

<!-- Border color -->
<div class="border border-red-500">Red border</div>
<div class="border border-blue-500">Blue border</div>

<!-- Specific sides -->
<div class="border-t">Top border only</div>
<div class="border-b">Bottom border only</div>
<div class="border-l">Left border only</div>
<div class="border-r">Right border only</div>
```

### Rounded Corners

```html
<div class="rounded">Slightly rounded</div>
<div class="rounded-md">Medium rounded</div>
<div class="rounded-lg">Large rounded</div>
<div class="rounded-xl">Extra large rounded</div>
<div class="rounded-full">Fully rounded (circle if square)</div>

<!-- Specific corners -->
<div class="rounded-t-lg">Rounded top corners</div>
<div class="rounded-b-lg">Rounded bottom corners</div>
```

---

## Shadows

```html
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Normal shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-2xl">2x large shadow</div>
```

---

## Hover Effects

Add `hover:` before any class to apply it on mouse hover.

```html
<!-- Change color on hover -->
<button class="bg-blue-500 hover:bg-blue-700">Hover me</button>

<!-- Change text color on hover -->
<p class="text-black hover:text-blue-500">Hover over me</p>

<!-- Scale up on hover -->
<div class="transform hover:scale-110">Hover to grow</div>

<!-- Smooth transition -->
<button class="bg-blue-500 hover:bg-blue-700 transition duration-300">
    Smooth color change
</button>
```

---

## Responsive Design

Make your design work on different screen sizes.

### Breakpoints

| Prefix | Screen Size | Usage |
|--------|-------------|-------|
| (none) | All screens | Default |
| `sm:` | ≥640px | Small tablets |
| `md:` | ≥768px | Tablets |
| `lg:` | ≥1024px | Laptops |
| `xl:` | ≥1280px | Desktops |

### Example

```html
<!-- Small on mobile, large on desktop -->
<p class="text-sm md:text-lg lg:text-2xl">Responsive text</p>

<!-- Hide on mobile, show on desktop -->
<div class="hidden md:block">Only visible on tablets and up</div>

<!-- Padding changes by screen size -->
<div class="p-2 md:p-4 lg:p-8">Responsive padding</div>
```

---

## Glassmorphism Effect

Popular modern design effect with blur and transparency.

```html
<div class="backdrop-blur-lg bg-white/30 rounded-2xl p-6 shadow-xl border border-white/20">
    <h2 class="text-2xl font-bold">Glassmorphic Card</h2>
    <p class="text-gray-700">This has a glass effect!</p>
</div>
```

**Breakdown:**
- `backdrop-blur-lg` → Blurs background behind element
- `bg-white/30` → White background with 30% opacity
- `rounded-2xl` → Very rounded corners
- `shadow-xl` → Large shadow
- `border border-white/20` → White border with 20% opacity

---

## Common Button Styles

```html
<!-- Primary button -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
    Click Me
</button>

<!-- Outlined button -->
<button class="bg-transparent hover:bg-blue-500 text-blue-700 hover:text-white border border-blue-500 py-2 px-4 rounded">
    Outlined
</button>

<!-- Rounded pill button -->
<button class="bg-green-500 hover:bg-green-700 text-white py-2 px-6 rounded-full">
    Pill Button
</button>

<!-- Icon button -->
<button class="bg-red-500 hover:bg-red-700 text-white p-3 rounded-full">
    ❤️
</button>
```

---

## Common Card Styles

```html
<!-- Simple card -->
<div class="bg-white rounded-lg shadow-lg p-6">
    <h3 class="text-xl font-bold mb-2">Card Title</h3>
    <p class="text-gray-700">Card content goes here.</p>
</div>

<!-- Card with image -->
<div class="bg-white rounded-lg shadow-lg overflow-hidden">
    <img src="image.jpg" class="w-full h-48 object-cover">
    <div class="p-6">
        <h3 class="text-xl font-bold mb-2">Card Title</h3>
        <p class="text-gray-700">Card content.</p>
    </div>
</div>

<!-- Hoverable card -->
<div class="bg-white rounded-lg shadow-lg p-6 transform hover:scale-105 transition duration-300">
    <h3 class="text-xl font-bold mb-2">Hover Me</h3>
    <p class="text-gray-700">I grow on hover!</p>
</div>
```

---

## Complete Example: Chat Message

```html
<!-- User message (right side) -->
<div class="flex justify-end mb-4">
    <div class="bg-blue-500 text-white rounded-lg px-4 py-2 max-w-xs">
        <p>This is my message!</p>
    </div>
</div>

<!-- AI response (left side) -->
<div class="flex justify-start mb-4">
    <div class="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-xs">
        <p>This is the AI response.</p>
    </div>
</div>
```

---

## Quick Reference Table

### Most Used Classes

| Category | Classes | What it does |
|----------|---------|-------------|
| **Colors** | `text-blue-500`, `bg-red-500` | Text and background colors |
| **Spacing** | `p-4`, `m-4`, `px-6`, `py-3` | Padding and margin |
| **Text** | `text-xl`, `font-bold`, `text-center` | Font size, weight, alignment |
| **Layout** | `flex`, `flex-col`, `justify-center` | Arrange items |
| **Size** | `w-full`, `h-32`, `w-1/2` | Width and height |
| **Borders** | `border`, `rounded-lg`, `shadow-lg` | Borders, corners, shadows |
| **Hover** | `hover:bg-blue-700`, `hover:scale-110` | Mouse hover effects |
| **Responsive** | `sm:text-lg`, `md:p-8` | Different styles by screen size |

---

## Tips for Tomorrow's Workshop

### 1. Start Simple
Begin with basic colors and spacing:
```html
<div class="bg-blue-500 text-white p-4">
    Simple example
</div>
```

### 2. Build Up Gradually
Add more classes step by step:
```html
<!-- Step 1: Color -->
<div class="bg-blue-500 text-white">

<!-- Step 2: Add spacing -->
<div class="bg-blue-500 text-white p-4">

<!-- Step 3: Add rounded corners -->
<div class="bg-blue-500 text-white p-4 rounded-lg">

<!-- Step 4: Add shadow -->
<div class="bg-blue-500 text-white p-4 rounded-lg shadow-lg">

<!-- Step 5: Add hover effect -->
<div class="bg-blue-500 text-white p-4 rounded-lg shadow-lg hover:bg-blue-700">
```

### 3. Use Browser DevTools
Right-click on any element → Inspect → Edit classes live to see changes instantly.

### 4. Tailwind Documentation
If you forget a class, search on: https://tailwindcss.com/docs

### 5. Common Mistakes to Avoid
- **Don't** use spaces in class values: `text-blue 500` ❌
- **Do** use hyphens: `text-blue-500` ✅
- **Don't** forget the CDN link in HTML `<head>`
- **Do** combine multiple classes: `bg-blue-500 text-white p-4 rounded-lg`

---

## Best Online Cheat Sheets

If you want more reference during workshop:

1. **Nerdcave Tailwind Cheat Sheet**
   - URL: https://nerdcave.com/tailwind-cheat-sheet
   - Single page, searchable, clean design

2. **Flowbite Tailwind Cheat Sheet**
   - URL: https://flowbite.com/tools/tailwind-cheat-sheet/
   - Interactive, filter by category

3. **Creative Tim Cheat Sheet**
   - URL: https://www.creative-tim.com/twcomponents/cheatsheet
   - Visual examples for each class

4. **Official Tailwind Docs**
   - URL: https://tailwindcss.com/docs
   - Most complete and always up-to-date

---

## Practice Exercise for Students

Give students this challenge during workshop:

**"Create a profile card with:"**
- White background
- Rounded corners
- Shadow
- Padding inside
- Profile image (rounded circle)
- Name (large, bold text)
- Description (gray text)
- Blue button at bottom

**Solution:**
```html
<div class="bg-white rounded-lg shadow-lg p-6 max-w-sm">
    <img src="profile.jpg" class="w-24 h-24 rounded-full mx-auto mb-4">
    <h2 class="text-2xl font-bold text-center mb-2">John Doe</h2>
    <p class="text-gray-600 text-center mb-4">Web Developer</p>
    <button class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded w-full">
        Contact Me
    </button>
</div>
```

---

**END OF CHEAT SHEET**

*Keep this open during your workshop. Search with Ctrl+F to find any class quickly!*