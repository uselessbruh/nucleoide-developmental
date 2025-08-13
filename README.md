# Perl Editor - Advanced Code Editor with AI Integration

<img src="src/icons/logo.png" alt="Perl Editor Logo" width="200"/>

## Overview

Perl Editor is a sophisticated, feature-rich code editor built with Python and PyQt5, specifically designed for Perl development but with extensive support for multiple programming languages. The IDE combines traditional code editing capabilities with modern AI-powered assistance and bioinformatics tools.

## 🚀 Features

### Core Editor Features
- **Multi-language Syntax Highlighting**: Support for Perl, Python, and other programming languages
- **Tabbed Interface**: Manage multiple files simultaneously with an intuitive tabbed interface
- **Advanced Text Editing**: Built on QScintilla for professional-grade text editing capabilities
- **File Explorer**: Integrated file tree view for easy project navigation
- **Customizable Themes**: Light and dark theme support with customizable color schemes

### AI-Powered Coding Assistant 🤖
- **Intelligent Code Assistance**: Built-in AI chatbot for coding help and guidance
- **Real-time Code Analysis**: Get explanations, debugging help, and optimization suggestions
- **Algorithm Design Support**: Assistance with algorithm design and implementation
- **Best Practices**: Code review suggestions and best practice recommendations
- **Multi-language Support**: AI assistance for various programming languages

### Bioinformatics Tools 🧬
- **Sequence Alignment**: Global and local sequence alignment tools
- **Bio Data Processing**: Integrated bioinformatics utilities
- **Scientific Computing**: Specialized tools for biological data analysis

### Version Control Integration
- **Git Panel**: Integrated Git support with visual interface
- **Repository Management**: Clone, initialize, and manage Git repositories
- **Change Tracking**: Visual representation of file changes and staging
- **Commit Management**: Easy commit workflow with message editing

### Terminal Integration
- **Command Prompt Emulator**: Built-in terminal emulation
- **Multiple Shell Support**: Command Prompt, PowerShell, and Git Bash
- **Custom Interpreters**: Support for custom Perl and Python interpreters
- **Output Caching**: Persistent terminal and output history

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PyQt5 5.15.11
- QScintilla 2.14.1
- Additional dependencies listed in `project.toml`

### Quick Start
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt` (if available) or install packages from `project.toml`
3. Run the application: `python src/main.py`

## 🔧 Backend AI Support

**Note**: The `backend/` folder contains the AI server components that power the intelligent coding assistant. This backend is included in the releases and provides the core AI functionality for the IDE.

### Backend Features
- Local AI server for coding assistance
- Phi-3-mini-4k-instruct model integration
- Real-time response processing
- Secure local processing (no data sent to external servers)

The backend runs on `http://192.168.1.12:6000` by default and provides REST API endpoints for the AI chat functionality.

## 📋 Configuration

The editor supports extensive customization through:
- **Settings Panel**: Configure editor preferences, themes, and behavior
- **Theme Customization**: Modify colors, fonts, and UI elements
- **Interpreter Settings**: Configure custom Perl and Python interpreters
- **Git Configuration**: Set up Git username and preferences

## 🐛 Known Issues & Limitations

⚠️ **Please Note**: This project is currently in development and contains several bugs and incomplete features:

- Some bioinformatics tools may not function correctly
- Git integration has limited functionality 
- Terminal emulator may have compatibility issues on some systems
- AI backend requires proper network configuration
- File handling edge cases may cause unexpected behavior
- Theme switching may not update all UI elements immediately

## 🚧 Development Status

This is an **experimental version** with ongoing development. Many features are still being refined and improved.

## 🔮 Future Plans

**Exciting News**: A new repository with a completely redesigned codebase is in development! This upcoming version will feature:

- **Enhanced User Experience**: Completely redesigned interface with improved usability
- **Better Performance**: Optimized codebase for faster response times
- **Expanded AI Features**: More sophisticated AI assistance capabilities
- **Improved Stability**: Bug fixes and comprehensive testing
- **Enhanced Bioinformatics Suite**: More powerful scientific computing tools
- **Better Git Integration**: Full-featured version control support

**The new version will be available in the releases section of the upcoming repository.**

## 📁 Project Structure

```
Perl_editor/
├── src/
│   ├── main.py              # Main application entry point
│   ├── settings.json        # User preferences
│   ├── theme.json          # Theme configurations
│   ├── app_pages/          # HTML pages for about/help
│   ├── components/         # Reusable UI components
│   ├── contentCache/       # Output and terminal cache
│   ├── icons/              # Application icons and images
│   ├── panels/             # Side panel implementations
│   └── utils/              # Utility functions
├── backend/                # AI server (included in releases)
├── project.toml            # Project configuration
└── .gitignore             # Git ignore rules
```

## 🤝 Contributing

While this version is being superseded by a new codebase, contributions and feedback are still welcome! Please note that major development efforts are focused on the upcoming redesigned version.

**We encourage developers to enhance and build upon this project!** Feel free to:
- Fix bugs and improve existing features
- Add new functionality and tools
- Enhance the user interface
- Optimize performance
- Extend bioinformatics capabilities
- Improve AI integration

Your contributions can help make this IDE even better for the coding community!

## 📄 License

This project is licensed under the MIT License. See the `LICENCE` file for details.

The MIT License allows you to freely use, modify, and distribute this software, making it perfect for both personal and commercial projects.

## 🔗 Links & Resources

- **Bioinformatics Tools**: Integrated Bio package support for sequence analysis
- **AI Model**: Utilizes Phi-3-mini-4k-instruct for coding assistance
- **Framework**: Built with PyQt5 for cross-platform compatibility

---

**Disclaimer**: This software is provided as-is for educational and development purposes. Please test thoroughly before using in production environments.

**Stay tuned for the new and improved version coming soon!** 🎉
