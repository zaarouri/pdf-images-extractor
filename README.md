# 📄 PDF Image Extractor

A modern, dynamic single-page web application for extracting images from PDF files. Built with Streamlit and PyMuPDF with a beautiful, responsive UI and slide preview functionality.

## ✨ Features

- **🎨 Modern UI**: Beautiful gradient design with glassmorphism effects
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **⚡ Single-Page Experience**: No scrolling - everything happens in one viewport
- **🖼️ Slide Preview**: Navigate through extracted images with slide controls
- **📊 Live Statistics**: Real-time extraction statistics and progress tracking
- **🎯 Smart Processing**: Intelligent image detection and extraction
- **📦 Multiple Download Options**: Individual images or ZIP archive
- **⚙️ Configurable Settings**: Adjust quality, size filters, and optimization
- **🔍 File Validation**: Comprehensive PDF validation and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pdf_image_extractor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎨 Modern Design Features

### Visual Design
- **Gradient Background**: Beautiful purple-blue gradient
- **Glassmorphism Cards**: Semi-transparent cards with blur effects
- **Modern Buttons**: Gradient buttons with hover animations
- **Responsive Layout**: Adapts to any screen size
- **Smooth Animations**: Hover effects and transitions

### User Experience
- **Single Page**: Everything happens in one viewport - no scrolling
- **Dynamic Components**: Content changes based on user actions
- **Real-time Feedback**: Live updates and progress
- **Intuitive Interface**: Easy-to-use drag-and-drop upload
- **Slide Navigation**: Browse through extracted images

## 📋 How It Works

1. **Upload**: Drag and drop your PDF or click to browse
2. **Preview**: See file information and current settings
3. **Process**: Click "Start Extraction" to begin processing
4. **Track**: Watch real-time progress and statistics
5. **Browse**: Navigate through extracted images with slide controls
6. **Download**: Get individual images or download all as ZIP

## 🏗️ Architecture

### Single-Page Dynamic Design
```
┌─────────────────────────────────────┐
│           Header (Gradient)         │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐ │
│  │      Dynamic Content Area      │ │
│  │                               │ │
│  │  Upload Section               │ │
│  │  ↓                            │ │
│  │  Processing Section           │ │
│  │  ↓                            │ │
│  │  Results Section              │ │
│  │  (with Slide Preview)         │ │
│  └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  │
│  │   Settings  │  │   Controls  │  │
│  │   Sidebar   │  │   & Nav     │  │
│  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────┘
```

### Key Components
- **Dynamic Sections**: Content changes based on app state
- **Slide Preview**: Image navigation with controls
- **Real-time Updates**: Live progress and statistics
- **Modern Styling**: CSS gradients, shadows, and animations
- **No Scrolling**: Everything fits in one viewport

## 🎯 User Interface Features

### Upload Section
- Drag-and-drop file upload
- File validation and preview
- File information display
- Settings overview

### Processing Section
- Real-time progress bar
- Page-by-page status updates
- Processing statistics
- Error handling with user-friendly messages

### Results Section with Slide Preview
- **Image Slide Navigation**: Previous/Next buttons
- **Slide Indicators**: Dot navigation for quick access
- **Current Image Display**: Large preview with caption
- **Individual Downloads**: Download current image
- **ZIP Archive**: Download all images at once
- **Statistics Dashboard**: Extraction metrics

### Settings Sidebar
- Image quality slider
- Minimum size filter
- Advanced options (optimization, metadata)
- Real-time settings preview

## 📊 Supported Features

### Input
- PDF files (max 50MB)
- Drag-and-drop upload
- File validation

### Output
- JPEG, PNG, GIF, BMP, TIFF images
- Individual image downloads
- ZIP archive downloads
- Image metadata display

### Processing
- Multi-page PDF support
- Image format detection
- Size filtering
- Quality optimization
- Progress tracking

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with PyMuPDF
- **Styling**: Modern CSS with gradients and animations
- **Responsive**: Mobile-first design approach
- **Performance**: Optimized image processing

## 🎨 Design Principles

### Modern UI/UX
- **Glassmorphism**: Semi-transparent cards with blur effects
- **Gradient Design**: Beautiful color transitions
- **Micro-interactions**: Hover effects and animations
- **Responsive Design**: Works on all devices
- **Accessibility**: Clear contrast and readable fonts

### User Experience
- **Single Viewport**: No scrolling needed
- **Dynamic Content**: Sections appear based on context
- **Real-time Feedback**: Live updates and progress
- **Intuitive Flow**: Logical step-by-step process
- **Error Handling**: Friendly error messages
- **Slide Navigation**: Easy image browsing

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop**: Full-featured experience with sidebar
- **Tablet**: Optimized layout with touch-friendly buttons
- **Mobile**: Compact design with swipe gestures

### Mobile Features
- Touch-optimized buttons
- Swipe-friendly interface
- Readable text sizes
- Optimized spacing

## 🔧 Configuration

All settings are easily accessible in the sidebar:
- **Image Quality**: 1-100% slider
- **Minimum Size**: Filter small images
- **Optimization**: Enable image compression
- **Metadata**: Preserve image metadata

## 🚀 Performance

- **Fast Processing**: Optimized image extraction
- **Memory Efficient**: Proper resource management
- **Progress Tracking**: Real-time status updates
- **Error Recovery**: Graceful error handling

## 🎯 Future Enhancements

The modern architecture supports easy addition of:
- [ ] Batch processing of multiple PDFs
- [ ] Advanced image filtering options
- [ ] Cloud storage integration
- [ ] OCR text extraction
- [ ] Image editing capabilities
- [ ] Social sharing features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on different screen sizes
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Zaarouri Abdelmounime**

Built with ❤️ using Streamlit and PyMuPDF.

## 🌐 Live Demo

> Coming soon on Streamlit Cloud...

---

**Experience the future of PDF image extraction with our modern, dynamic, and responsive single-page application!**
