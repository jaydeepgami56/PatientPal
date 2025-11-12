# Healthcare Agent Gallery Demo - Frontend

This folder contains a small Vite + React demo that reproduces the Dribbble-inspired gallery layout for your healthcare agent.

Prerequisites
- Node 18+ and npm installed.

Quick start
1. Open a terminal and run:
```bash
cd frontend
npm install
npm run dev
```

Tailwind setup (if missing)
```bash
# install tailwind deps then initialize
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
Ensure `@tailwind base; @tailwind components; @tailwind utilities;` exist in [`frontend/src/index.css`](frontend/src/index.css:1).

Files of interest
- [`frontend/package.json`](frontend/package.json:1)
- [`frontend/index.html`](frontend/index.html:1)
- [`frontend/src/main.jsx`](frontend/src/main.jsx:1)
- [`frontend/src/App.jsx`](frontend/src/App.jsx:1)
- [`frontend/src/components/DesignComponents.jsx`](frontend/src/components/DesignComponents.jsx:1)
- [`frontend/src/index.css`](frontend/src/index.css:1)
- [`frontend/tailwind.config.cjs`](frontend/tailwind.config.cjs:1)

Add local assets
- Put images under `frontend/public/assets/` (create the folder).
- Reference them from React as `/assets/your-image.jpg`.

Example: replace placeholder gallery items in [`frontend/src/App.jsx`](frontend/src/App.jsx:1)
```javascript
// frontend/src/App.jsx (example snippet)
const items = [
  { img: '/assets/patient-1.jpg', title: 'Patient UI 1', desc: 'Mockup', assets: 4 },
  { img: '/assets/scan-2.jpg', title: 'Scan 2', desc: 'Mockup', assets: 3 }
];
```

Use the Gallery component
```javascript
import Gallery from './components/DesignComponents';

// inside App render
<Gallery items={items} />
```

Troubleshooting
- If you see "could not determine executable to run" when using `npm exec`, run the tailwind commands with `npx` or install the dev deps first (see Tailwind setup above).
- Verify Node/npm versions: `node -v` and `npm -v`.

Next steps
- Replace Unsplash placeholders with approved design assets.
- Tweak the theme/colors in [`frontend/tailwind.config.cjs`](frontend/tailwind.config.cjs:1).
- Make any accessibility and responsive refinements required for your healthcare UI.

Notes
- This is a demo inspired by a Dribbble shot. Do not copy protected assets or proprietary designs.
