# 🌐 PlantPixel Frontend

This directory contains the React/TypeScript frontend application for the PlantPixel plant analysis system.

## 🏗️ Architecture

The frontend is built with:
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Chart.js** for data visualization

## 📁 Directory Structure

```
frontend/
├── public/                     # Static assets
│   ├── favicon.ico            # App favicon
│   ├── placeholder.svg        # Placeholder images
│   └── robots.txt            # SEO robots file
├── src/                       # Source code
│   ├── components/           # React components
│   │   ├── ui/              # shadcn/ui components
│   │   ├── GrowthChart.tsx  # Growth visualization
│   │   ├── ImageUpload.tsx  # Image upload component
│   │   ├── Layout.tsx       # App layout
│   │   └── MetricsDisplay.tsx # Metrics display
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility libraries
│   ├── pages/               # Page components
│   │   ├── Analysis.tsx     # Analysis page
│   │   ├── History.tsx      # History page
│   │   ├── Index.tsx        # Home page
│   │   └── NotFound.tsx     # 404 page
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # App entry point
│   └── *.css                # Styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.ts           # Vite configuration
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── README.md                # This file
```

## 🚀 Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```
The app will be available at `http://localhost:5173`

### Building for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 🔗 Backend Integration

The frontend communicates with the Flask backend API running on `http://localhost:5000`. Key endpoints:

- `POST /api/analyze` - Upload and analyze plant images
- `GET /api/history` - Retrieve analysis history
- `GET /api/metrics` - Get system performance metrics

## 🎨 Features

- **📸 Image Upload**: Drag-and-drop or click to upload plant images
- **📊 Real-time Analysis**: Instant plant growth metrics and visualization
- **📈 Growth Charts**: Interactive charts showing plant development over time
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **🎯 Modern UI**: Clean, professional interface with shadcn/ui components

## 🛠️ Technologies

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Chart.js with react-chartjs-2
- **HTTP Client**: Fetch API
- **State Management**: React hooks and context

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript checks
