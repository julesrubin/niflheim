# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A React-based portfolio website showcasing projects with dark mode support. Built with React 18, TailwindCSS, and Framer Motion for animations. Deployed with Docker/nginx and hosted at https://www.julesrubin.com.

**Key Stack:**
- React 18 with React Router v6 for routing
- TailwindCSS for styling with custom dark mode theme
- Framer Motion (v4.1.17) for animations
- EmailJS for contact form functionality
- Docker multi-stage build with nginx for production

**Base Path:** The app runs at `/portfolio` base path (configured in `package.json` homepage and `Router basename`)

## Development Commands

### Start Development Server
```bash
yarn start
# or
npm start
```
Note: Uses `--openssl-legacy-provider` flag for Node compatibility

### Build for Production
```bash
yarn build
# Outputs to /build directory
```

### Run Tests
```bash
yarn test
# Uses Jest via react-scripts
```

### Build TailwindCSS
```bash
yarn build:css
# Processes src/css/tailwind.css → src/css/main.css
# Rarely needed; handled automatically by react-scripts
```

### Docker Build
```bash
docker build -t portfolio .
docker run -p 8080:8080 portfolio
```

## Architecture

### Routing Structure
- **App.js** is the main router using `BrowserRouter` with `basename="/portfolio"`
- Routes use lazy loading for all pages (`React.lazy()`)
- Each project has a dedicated route: `/projects/{project-key}`
- Main routes: `/`, `/projects`, `/about`, `/contact`

### State Management
- **Context API** for global state (no Redux)
- Three main contexts:
  - `ProjectsContext`: Project filtering and search (`src/context/ProjectsContext.jsx`)
  - `SingleProjectContext`: Individual project details (`src/context/SingleProjectContext.jsx`)
  - `AboutMeContext`: About page data (`src/context/AboutMeContext.jsx`)

### Dark Mode Implementation
- **Custom hook:** `useThemeSwitcher` (`src/hooks/useThemeSwitcher.jsx`)
- Uses `localStorage.theme` for persistence
- Toggles `dark` class on document root
- TailwindCSS dark mode configured as `class` mode in `tailwind.config.js`
- Theme colors defined in Tailwind config:
  - Light: `primary-light`, `secondary-light`, `ternary-light`
  - Dark: `primary-dark`, `secondary-dark`, `ternary-dark`

### Project Data Structure
- **Projects data:** `src/data/projects.js` exports `projectsData` array
- Each project requires:
  - `id`: unique number
  - `title`: display name
  - `category`: project type (e.g., "Website", "Mobile Application")
  - `img`: thumbnail image import
  - `projectKey`: URL-friendly identifier (matches route)
- Array is reversed on export (newest first)
- Individual project pages import from `src/data/singleProjectData.js`

### Component Organization
```
src/
├── components/
│   ├── shared/          # AppHeader, AppFooter, AppBanner
│   ├── about/           # About page sections
│   ├── contact/         # Contact form components
│   ├── projects/        # Project listing and filtering
│   └── reusable/        # Button, FormInput shared components
├── pages/               # Page-level components (lazy loaded)
├── context/             # React Context providers
├── hooks/               # Custom hooks (theme, scroll)
├── data/                # Static data (projects, about, clients)
├── images/              # Project images, brands, etc.
└── fonts/               # GeneralSans font family
```

### Adding a New Project
1. Add project object to `nonOrderedProjectsData` in `src/data/projects.js`
2. Create page component in `src/pages/{ProjectName}.jsx`
3. Add route in `src/App.js` Routes
4. Import and use lazy loading for the page component
5. Add project images to `src/images/projects/{ProjectName}/`

### Contact Form Integration
- Uses EmailJS (`@emailjs/browser`) for email sending
- Configuration in `src/components/contact/ContactForm.jsx:25-29`
- Service ID, template ID, and public key are hardcoded (consider environment variables)
- Form state managed with React hooks (no form library)

### Styling Conventions
- TailwindCSS utility classes for all styling
- Dark mode classes: `dark:{utility}`
- Custom colors defined in `tailwind.config.js`
- Responsive breakpoints: `sm:`, `lg:`, `xl:`, `2xl:`
- Container padding configured per breakpoint
- GeneralSans font family loaded via CSS (`src/css/App.css`)

### Animation Patterns
- Framer Motion `AnimatePresence` wraps entire app
- Lazy-loaded pages use Suspense with empty fallback
- Scroll animations handled by `framer-motion` and `react-scroll`
- Custom scroll-to-top hook: `useScrollToTop.jsx`

## Testing
- Jest configured via `react-scripts`
- Test files in `src/__tests__/` directory
- Existing tests: `Banner.test.js`, `Modal.test.js`
- Uses React Testing Library (`@testing-library/react`)

## Deployment Notes
- Multi-stage Docker build (Node build → nginx serve)
- Production served via nginx on port 8080
- Custom `nginx.conf` handles SPA routing
- Public files include redirects config: `public/_redirects`
- Build output directory: `/build`
- Nginx serves from `/usr/share/nginx/html`
