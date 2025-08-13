from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciScintilla, QsciLexerPerl, QsciLexerPython
import sys
from pathlib import Path
import subprocess
import os
import webbrowser
from datetime import datetime
import json
import pyjokes
import requests
import re
from Bio import SeqIO
from io import StringIO

# Set up environment variables for custom interpreters
def setup_custom_interpreters():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    perl_path = os.path.join(base_dir, 'interpretor', 'perl', 'perl', 'bin')
    python_path = os.path.join(base_dir, 'interpretor', 'python')
    
    # Add to PATH
    if perl_path not in os.environ['PATH']:
        os.environ['PATH'] = perl_path + os.pathsep + os.environ['PATH']
    if python_path not in os.environ['PATH']:
        os.environ['PATH'] = python_path + os.pathsep + os.environ['PATH']
    
    # Set specific environment variables
    os.environ['PERL5LIB'] = os.path.join(base_dir, 'interpretor', 'perl', 'perl', 'lib')
    os.environ['PYTHONPATH'] = python_path

# Call setup at module level
setup_custom_interpreters()

class SettingsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
                font-size:12px;
                outline:none;
                border:none;
            }
            QLabel {
                color: #D3D3D3;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
            }
            QGroupBox {
                color: #D3D3D3;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QCheckBox {
                color: #D3D3D3;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #3c3c3c;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border: 1px solid #3498db;
            }
        ''')
        self.setMaximumWidth(400)
        self.setMinimumWidth(200)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Create scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        # Create widget to hold all settings
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(15)
        
        # Account Settings
        account_group = QGroupBox("Account")
        account_layout = QVBoxLayout()
        
        # User profile
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Profile Picture:")
        self.profile_pic = QLabel()
        self.profile_pic.setFixedSize(50, 50)
        self.profile_pic.setStyleSheet("background-color: #3c3c3c; border-radius: 25px;")
        change_pic_btn = QPushButton("Change")
        change_pic_btn.clicked.connect(self.change_profile_picture)
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.profile_pic)
        profile_layout.addWidget(change_pic_btn)
        account_layout.addLayout(profile_layout)
        
        # User info
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        account_layout.addLayout(name_layout)
        
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        account_layout.addLayout(email_layout)
        
        account_group.setLayout(account_layout)
        settings_layout.addWidget(account_group)
        
        # Editor Settings
        editor_group = QGroupBox("Editor")
        editor_layout = QVBoxLayout()
        
        # Font settings
        font_layout = QHBoxLayout()
        font_label = QLabel("Font Size:")
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_size)
        editor_layout.addLayout(font_layout)
        
        # Tab settings
        tab_layout = QHBoxLayout()
        tab_label = QLabel("Tab Size:")
        self.tab_size = QSpinBox()
        self.tab_size.setRange(2, 8)
        self.tab_size.setValue(4)
        tab_layout.addWidget(tab_label)
        tab_layout.addWidget(self.tab_size)
        editor_layout.addLayout(tab_layout)
        
        # Editor features
        self.word_wrap = QCheckBox("Word Wrap")
        self.line_numbers = QCheckBox("Show Line Numbers")
        self.auto_indent = QCheckBox("Auto Indent")
        self.highlight_line = QCheckBox("Highlight Current Line")
        
        editor_layout.addWidget(self.word_wrap)
        editor_layout.addWidget(self.line_numbers)
        editor_layout.addWidget(self.auto_indent)
        editor_layout.addWidget(self.highlight_line)
        
        editor_group.setLayout(editor_layout)
        settings_layout.addWidget(editor_group)
        
        # Theme Settings
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()
        
        # Theme selection
        theme_select_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "High Contrast"])
        theme_select_layout.addWidget(theme_label)
        theme_select_layout.addWidget(self.theme_combo)
        theme_layout.addLayout(theme_select_layout)
        
        # Custom colors
        color_group = QGroupBox("Custom Colors")
        color_layout = QVBoxLayout()
        
        # Background color
        bg_layout = QHBoxLayout()
        bg_label = QLabel("Background:")
        self.bg_color = QPushButton()
        self.bg_color.setFixedSize(30, 30)
        self.bg_color.setStyleSheet("background-color: #21252b;")
        bg_layout.addWidget(bg_label)
        bg_layout.addWidget(self.bg_color)
        color_layout.addLayout(bg_layout)
        
        # Text color
        text_layout = QHBoxLayout()
        text_label = QLabel("Text Color:")
        self.text_color = QPushButton()
        self.text_color.setFixedSize(30, 30)
        self.text_color.setStyleSheet("background-color: #D3D3D3;")
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_color)
        color_layout.addLayout(text_layout)
        
        color_group.setLayout(color_layout)
        theme_layout.addWidget(color_group)
        
        theme_group.setLayout(theme_layout)
        settings_layout.addWidget(theme_group)
        
        # Terminal Settings
        terminal_group = QGroupBox("Terminal")
        terminal_layout = QVBoxLayout()
        
        # Shell selection
        shell_layout = QHBoxLayout()
        shell_label = QLabel("Default Shell:")
        self.shell_combo = QComboBox()
        self.shell_combo.addItems(["Command Prompt", "PowerShell", "Git Bash"])
        shell_layout.addWidget(shell_label)
        shell_layout.addWidget(self.shell_combo)
        terminal_layout.addLayout(shell_layout)
        
        # Terminal features
        self.terminal_bell = QCheckBox("Enable Terminal Bell")
        self.terminal_cursor = QCheckBox("Blinking Cursor")
        
        terminal_layout.addWidget(self.terminal_bell)
        terminal_layout.addWidget(self.terminal_cursor)
        
        terminal_group.setLayout(terminal_layout)
        settings_layout.addWidget(terminal_group)
        
        # Git Settings
        git_group = QGroupBox("Git")
        git_layout = QVBoxLayout()
        
        # Git configuration
        git_name_layout = QHBoxLayout()
        git_name_label = QLabel("Git Username:")
        self.git_name = QLineEdit()
        git_name_layout.addWidget(git_name_label)
        git_name_layout.addWidget(self.git_name)
        git_layout.addLayout(git_name_layout)
        
        git_email_layout = QHBoxLayout()
        git_email_label = QLabel("Git Email:")
        self.git_email = QLineEdit()
        git_email_layout.addWidget(git_email_label)
        git_email_layout.addWidget(self.git_email)
        git_layout.addLayout(git_email_layout)
        
        git_group.setLayout(git_layout)
        settings_layout.addWidget(git_group)
        
        # Add save and reset buttons
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_settings)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(reset_button)
        settings_layout.addLayout(buttons_layout)
        
        # Set the scroll area's widget
        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Load saved settings
        self.load_settings()
    
    def change_profile_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Profile Picture",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.profile_pic.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def save_settings(self):
        # Here you would implement saving settings to a configuration file
        QMessageBox.information(self, "Success", "Settings saved successfully!")
    
    def reset_settings(self):
        # Here you would implement resetting settings to defaults
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to default?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.load_settings()  # Reload default settings
            QMessageBox.information(self, "Success", "Settings reset to default!")
    
    def load_settings(self):
        # Here you would implement loading settings from a configuration file
        # For now, just set some default values
        self.name_input.setText("")
        self.email_input.setText("")
        self.font_size.setValue(12)
        self.tab_size.setValue(4)
        self.word_wrap.setChecked(True)
        self.line_numbers.setChecked(True)
        self.auto_indent.setChecked(True)
        self.highlight_line.setChecked(True)
        self.theme_combo.setCurrentText("Dark")
        self.shell_combo.setCurrentText("Command Prompt")
        self.terminal_bell.setChecked(True)
        self.terminal_cursor.setChecked(True)
        self.git_name.setText("")
        self.git_email.setText("")

class AddPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
                font-size:12px;
                outline:none;
                border:none;
            }
        ''')
        self.setMaximumWidth(400)
        self.setMinimumWidth(200)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add some example options
        title = QLabel("Create New")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # New file button
        new_file_btn = QPushButton("New File")
        new_file_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        layout.addWidget(new_file_btn)
        
        # New Perl module button
        new_perl_btn = QPushButton("New Perl Module")
        new_perl_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        layout.addWidget(new_perl_btn)
        
        # New Python file button
        new_python_btn = QPushButton("New Python File")
        new_python_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        layout.addWidget(new_python_btn)
        
        layout.addStretch()
        self.setLayout(layout)

class CommandPromptEmulator(QTextEdit):
    """
    Widget that emulates the Windows Command Prompt functionality
    """
    command_executed = pyqtSignal(str)
    
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings
        
        # Set appearance to match CMD
        self.setFont(QFont("Consolas", 10))
        self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        
        # Initialize command process
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.SeparateChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_process_finished)
        
        # Get custom interpreter paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.python_interpreter = os.path.join(base_dir, 'interpretor', 'python', 'python.exe')
        self.perl_interpreter = os.path.join(base_dir, 'interpretor', 'perl', 'perl', 'bin', 'perl.exe')
        
        # Flag to track if a process is running and waiting for input
        self.process_running = False
        self.waiting_for_input = False
        
        # Text selection tracking
        self.selecting_text = False
        
        # Command history
        self.command_history = []
        self.history_index = -1
        
        # Current command being typed
        self.current_command = ""
        self.current_input = ""
        
        # Current working directory
        self.current_directory = self.settings.get('openMainFolder', '') if self.settings else ''
        
        # To keep track of the current command line's position
        self.command_line_position = 0
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
        
        # Start the command prompt
        self.initialize_command_prompt()
        
    def setup_shortcuts(self):
        """Set up keyboard shortcuts for copy and paste"""
        # We'll handle copy in the keyPressEvent method to preserve selection
        # Copy shortcut
        self.copy_shortcut = QShortcut(QKeySequence.Copy, self)
        self.copy_shortcut.activated.connect(self.copy_selected_text)
        
        # Paste shortcut
        self.paste_shortcut = QShortcut(QKeySequence.Paste, self)
        self.paste_shortcut.activated.connect(self.handle_paste)
        
    def copy_selected_text(self):
        """Copy selected text without losing selection"""
        if self.textCursor().hasSelection():
            QApplication.clipboard().setText(self.textCursor().selectedText())
            # Don't clear selection after copying
    
    def handle_paste(self):
        """Custom paste handler to ensure paste works properly in the terminal"""
        # Only paste if we're in the editable area or if a process is waiting for input
        if self.process_running and self.waiting_for_input:
            # Direct paste for running processes
            self.paste()
        else:
            # For command prompt, ensure cursor is at the right position then paste
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.paste()
        
    def initialize_command_prompt(self):
        """Initialize the command prompt with the welcome message and first prompt"""
        # Display Windows CMD-like header
        self.append("Microsoft Windows [Version 10.0.22621.1848]")
        self.append("(c) Microsoft Corporation. All rights reserved.")
        self.append("")
        
        # Check if no folder is open
        if self.settings and not self.settings.get('openMainFolder'):
            self.append("Welcome to NucleoIDE!")
            self.append("")
            self.append("To get started:")
            self.append("1. Click on the folder icon in the sidebar")
            self.append("2. Select 'Open Folder' to open a project directory")
            self.append("3. Or use the 'Open Folder' button in the file explorer")
            self.append("")
            self.append("Once you open a folder, you can:")
            self.append("- Create and edit files")
            self.append("- Run your code")
            self.append("- Use the terminal in your project directory")
            self.append("")
            # Don't show prompt if no folder is open
            return
        
        self.display_prompt()
        
    def display_prompt(self):
        """Display the command prompt with current directory"""
        if not self.current_directory:
            self.append(">")
        else:
            self.append(f"{self.current_directory}>")
        # Save the position of the current command line
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.command_line_position = cursor.position()
        self.moveCursor(QTextCursor.End)
        self.process_running = False
        self.waiting_for_input = False
        
    def handle_stdout(self):
        """Handle standard output from the process"""
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        if data:
            # Check if the process might be waiting for input
            if data.rstrip().endswith(':') or data.rstrip().endswith('?'):
                self.waiting_for_input = True
                
            # Only remove trailing whitespace if it's not just whitespace
            if data.strip():
                self.append(data.rstrip())
            else:
                self.append(data)
                
        self.moveCursor(QTextCursor.End)
        # Update command line position after adding output
        cursor = self.textCursor()
        self.command_line_position = cursor.position()
        
    def handle_stderr(self):
        """Handle standard error from the process"""
        data = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
        if data:
            # Use a different color for errors
            current_format = self.currentCharFormat()
            error_format = QTextCharFormat()
            error_format.setForeground(QColor("red"))
            self.setCurrentCharFormat(error_format)
            
            # Only remove trailing whitespace if it's not just whitespace
            if data.strip():
                self.append(data.rstrip())
            else:
                self.append(data)
            
            # Restore the original format
            self.setCurrentCharFormat(current_format)
        self.moveCursor(QTextCursor.End)
        # Update command line position after adding error output
        cursor = self.textCursor()
        self.command_line_position = cursor.position()
        
    def handle_process_finished(self, exit_code, exit_status):
        """Handle when the process finishes"""
        self.process_running = False
        self.waiting_for_input = False
        
        if exit_code != 0:
            self.append(f"Process exited with code {exit_code}")
        self.display_prompt()
        
    def execute_command(self, command):
        """Execute the given command with custom interpreter handling"""
        if not command.strip():
            self.display_prompt()
            return
            
        # If we're waiting for input to a running process
        if self.process_running and self.waiting_for_input:
            self.process.write((command + "\n").encode('utf-8'))
            self.waiting_for_input = False
            return
            
        # Add command to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Handle pip commands
        if command.lower().startswith('pip '):
            self.process.start(self.python_interpreter, ['-m', 'pip'] + command.split()[1:])
            self.process_running = True
            return
            
        # Handle cpan commands
        if command.lower().startswith('cpan '):
            self.process.start(self.perl_interpreter, ['-MCPAN', '-e'] + [' '.join(command.split()[1:])])
            self.process_running = True
            return
            
        # Handle Python file execution
        if command.lower().endswith('.py'):
            self.process.start(self.python_interpreter, [command])
            self.process_running = True
            return
            
        # Handle Perl file execution
        if command.lower().endswith('.pl'):
            self.process.start(self.perl_interpreter, [command])
            self.process_running = True
            return
            
        # Special handling for WSL command
        if command.lower() == "wsl" or command.lower().startswith("wsl "):
            self.append("WSL is not supported in this terminal environment.")
            self.append("Please use the Windows Command Prompt or PowerShell separately for WSL operations.")
            self.display_prompt()
            return
        
        # Handle built-in commands
        if command.lower().startswith("cd ") or command.lower() == "cd":
            self.change_directory(command[3:].strip() if " " in command else "")
        elif command.lower() == "cls":
            self.clear()
            self.display_prompt()
            return
        elif command.lower() == "exit":
            self.clear()
            self.display_prompt()
        else:
            # Execute external command
            try:
                if sys.platform == "win32":
                    self.process.start("cmd.exe", ["/c", command])
                else:
                    self.process.start("/bin/bash", ["-c", command])
                self.process_running = True
            except Exception as e:
                self.append(f"Error executing command: {str(e)}")
                self.display_prompt()
                
    def change_directory(self, new_dir):
        """Change the current directory (no project root restriction)"""
        try:
            # Handle empty cd command (show current directory)
            if not new_dir:
                self.append(self.current_directory)
                self.display_prompt()
                return
                
            # Handle cd to drive letter
            if len(new_dir) == 2 and new_dir[1] == ':':
                new_dir += '\\'
                
            # Handle parent directory navigation
            if new_dir == '..':
                parent_dir = os.path.dirname(self.current_directory)
                os.chdir(parent_dir)
                self.current_directory = os.getcwd()
                self.display_prompt()
                return

            # For other directory changes
            new_abs_path = os.path.abspath(os.path.join(self.current_directory, new_dir))
            os.chdir(new_abs_path)
            self.current_directory = os.getcwd()
            self.display_prompt()
        except Exception as e:
            self.append(f"\nError: The system cannot find the path specified: {new_dir}")
            self.append("")
            self.display_prompt()
        
    def mousePressEvent(self, event):
        """Handle mouse click events"""
        # If no folder is open, don't process mouse events
        if self.settings and not self.settings.get('openMainFolder'):
                return
            
        super().mousePressEvent(event)
        
        # Ensure cursor is after the prompt if not selecting text
        if not self.selecting_text:
            self.ensure_cursor_at_command_line()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events for text selection"""
        if event.buttons() & Qt.LeftButton:
            # If mouse is being dragged with left button, we're selecting text
            self.selecting_text = True
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        super().mouseReleaseEvent(event)
        
        # If we just finished a selection, keep it; otherwise ensure cursor position
        if self.selecting_text:
            # Check if there's actually a selection
            if not self.textCursor().hasSelection():
                self.selecting_text = False
                self.ensure_cursor_at_command_line()
        else:
            self.ensure_cursor_at_command_line()
    
    def ensure_cursor_at_command_line(self):
        """Ensures the cursor is positioned at the command input area"""
        cursor = self.textCursor()
        cursor_pos = cursor.position()
        
        # If cursor is before the command line position, move it to the end
        if cursor_pos < self.command_line_position:
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            
    def keyPressEvent(self, event):
        """Handle key press events"""
        # If no folder is open, don't process any key events
        if self.settings and not self.settings.get('openMainFolder'):
            return
            
        # Handle text selection copy if Ctrl+C is pressed
        if event.matches(QKeySequence.Copy):
            if self.textCursor().hasSelection():
                # Store the current selection
                cursor = self.textCursor()
                selected_text = cursor.selectedText()
                
                # Copy to clipboard
                QApplication.clipboard().setText(selected_text)
                
                # Restore the selection
                cursor.setPosition(cursor.selectionStart())
                cursor.setPosition(cursor.selectionEnd(), QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
                return
                
        # Handle keyboard selections (Shift+Arrow keys)
        if event.modifiers() & Qt.ShiftModifier:
            if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End):
                # If shift is held with navigation keys, we're selecting text
                self.selecting_text = True
                super().keyPressEvent(event)
                return
                
        # Reset selection mode when any key is pressed (unless it's just a modifier key)
        # Don't reset selection when Ctrl, Shift, Alt, Meta are pressed to allow keyboard shortcuts
        if event.key() not in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            # Only reset selection mode if we're not using a keyboard shortcut
            # Don't reset if Ctrl is held (to allow Ctrl+C to work)
            if not (event.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)):
                self.selecting_text = False
            
        # If we're in WSL mode or waiting for input, handle differently
        if self.process_running and self.waiting_for_input:
            if event.key() == Qt.Key_Return:
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.setTextCursor(cursor)
                
                # Get the current line
                cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
                current_line = cursor.selectedText()
                
                # Send the line as input to the process
                self.append("")  # New line
                self.process.write((current_line + "\n").encode('utf-8'))
                return
                
            # For regular input, just let most keys through
            super().keyPressEvent(event)
            return
            
        # Normal command line handling
        # Get current line text
        cursor = self.textCursor()
        current_position = cursor.position()
        
        # Move to end of document then to start of line to get current line
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        current_line = cursor.selectedText()
        
        # Calculate prompt and boundaries
        prompt = f"{self.current_directory}>"
        prompt_length = len(prompt)
        
        # Get the absolute position of the start of the line plus prompt length
        start_pos = self.document().findBlockByLineNumber(self.textCursor().blockNumber()).position()
        # More accurate calculation of editable position
        accurate_editable_start = start_pos + prompt_length
        
        if event.key() == Qt.Key_Return:
            # Execute command on Enter
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)  # Ensure cursor is at the end
            
            # Extract command (text after prompt)
            if prompt_length < len(current_line):
                command = current_line[prompt_length:].strip()
            else:
                command = ""
                
            self.append("")  # New line
            self.execute_command(command)
            
        elif event.key() == Qt.Key_Up:
            # Navigate command history (up)
            if self.history_index > 0:
                self.history_index -= 1
                self.replace_command_line(self.command_history[self.history_index])
                
        elif event.key() == Qt.Key_Down:
            # Navigate command history (down)
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.replace_command_line(self.command_history[self.history_index])
            elif self.history_index == len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                self.replace_command_line("")
                
        elif event.key() == Qt.Key_Tab:
            # Tab completion (simplified)
            if prompt_length < len(current_line):
                command = current_line[prompt_length:].strip()
                # Here you would implement tab completion logic
            
        elif event.key() == Qt.Key_Backspace:
            # Only prevent backspacing if we're exactly at the prompt boundary
            # Get the current cursor to accurately check if we're at the first character position
            current_cursor = self.textCursor()
            current_cursor_pos = current_cursor.position()
            
            # Get the current line text again to ensure we have up-to-date info
            cursor_for_line = self.textCursor()
            cursor_for_line.movePosition(QTextCursor.End)
            cursor_for_line.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            current_line_text = cursor_for_line.selectedText()
            
            # Check if the current text after prompt has only one character
            # and if we're trying to delete that character
            command_text = current_line_text[prompt_length:] if len(current_line_text) > prompt_length else ""
            
            # Only block backspace if we're at the boundary between prompt and command
            if current_cursor_pos <= accurate_editable_start:
                return
                
            super().keyPressEvent(event)
            
        elif event.key() == Qt.Key_Left:
            # Prevent moving cursor into the prompt
            # Get accurate cursor position
            cursor_pos = self.textCursor().position()
            
            # Only block if we'd move into the prompt area
            if cursor_pos <= accurate_editable_start:
                return
            super().keyPressEvent(event)
            
        elif event.key() == Qt.Key_Home:
            # Move to start of command, not start of line
            try:
                cursor = self.textCursor()
                # Use movePosition instead of setPosition to avoid out-of-range errors
                cursor.movePosition(QTextCursor.StartOfLine)
                for _ in range(prompt_length):
                    cursor.movePosition(QTextCursor.Right)
                self.setTextCursor(cursor)
            except Exception as e:
                print(f"Error in Home key handling: {e}")
            return
            
        elif current_position < accurate_editable_start:
            # If cursor is in prompt area, move it to the editable area
            try:
                cursor = self.textCursor()
                # Use movePosition instead of setPosition to avoid out-of-range errors
                cursor.movePosition(QTextCursor.StartOfLine)
                for _ in range(prompt_length):
                    cursor.movePosition(QTextCursor.Right)
                self.setTextCursor(cursor)
            except Exception as e:
                print(f"Error in cursor positioning: {e}")
                
            # If it's a printable character, insert it
            if event.text() and event.text().isprintable():
                super().keyPressEvent(event)
        else:
            # Allow normal editing for other keys
            super().keyPressEvent(event)
            
    def contextMenuEvent(self, event):
        """Handle right-click events"""
        # If no folder is open, don't process right-click
        if self.settings and not self.settings.get('openMainFolder'):
            return
            
        # Get clipboard content
        clipboard = QApplication.clipboard()
        text_to_paste = clipboard.text()
        
        if text_to_paste:
            # Ensure cursor is at the right position
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            
            # Insert the text
            self.insertPlainText(text_to_paste)
            
        # Prevent the default context menu
        event.accept()
        
    def clear_and_reset(self):
        """Clear the terminal and reset the prompt"""
        self.clear()
        self.initialize_command_prompt()
            
    def replace_command_line(self, new_command):
        """Replace the current command line with a new command"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        prompt = f"{self.current_directory}>"
        cursor.removeSelectedText()
        cursor.insertText(prompt + new_command)
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perl Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set standard panel width
        self.STANDARD_PANEL_WIDTH = 300
        
        # Track active panel button
        self.active_button = None
        
        # Get the absolute path to settings.json using os.path
        self.settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        
        # Set cache paths
        self.output_cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_cache.txt')
        self.terminal_cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'terminal_cache.txt')
        
        # Load settings
        try:
            with open(self.settings_path, 'r') as file:
                self.settingsJson = json.load(file)
        except FileNotFoundError:
            # Create default settings if file doesn't exist
            self.settingsJson = {
                "theme": "dark",
                "themeColors": {
                    "sideBar": "#1a1a1a"
                },
                "openfiles": [],
                "openMainFolder": ""
            }
            with open(self.settings_path, 'w') as file:
                json.dump(self.settingsJson, file, indent=2)
        
        # Initialize variables
        self.current_file = None
        self.process_output = None
        self.tab_file_map = {}
        self.modified_tabs = set()
        self.original_content = {}
        self.loading_file = False
        
        # Initialize panels
        self.settings_panel = SettingsPanel(self)
        self.add_panel = AddPanel(self)
        self.biotools_panel = BioToolsPanel(self)
        self.chatbot_panel = ChatbotPanel(self)
        self.git_panel = GitPanel(self)
        
        # Set fixed width for all panels
        self.settings_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        self.add_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        self.biotools_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        self.chatbot_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        self.git_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        
        # Hide panels initially
        self.settings_panel.hide()
        self.add_panel.hide()
        self.biotools_panel.hide()
        self.chatbot_panel.hide()
        self.git_panel.hide()
        
        # Initialize UI
        self.init_ui()
        self.set_up_menu()
        self.set_up_shortcuts()
        
        # Set theme based on settings
        if self.settingsJson['theme'] == 'light':
            self.light_action.setChecked(True)
            self.dark_action.setChecked(False)
        elif self.settingsJson['theme'] == 'dark':
            self.light_action.setChecked(False)
            self.dark_action.setChecked(True)
        
        # Load previously open files and directory
        self.load_open_files()
        self.load_last_directory()
        
        # Load output and terminal cache
        self.load_output_and_terminal_cache()
        
        # Show welcome message
        self.show_hello_message()

    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def set_up_shortcuts(self):
        """Set up keyboard shortcuts"""
        hello_shortcut = QShortcut(QKeySequence("Ctrl+J"), self)
        hello_shortcut.activated.connect(self.show_hello_message)

    def show_hello_message(self):
        """Show a random joke message"""
        joke = pyjokes.get_joke()
        self.statusBar().showMessage(f"{joke}", 30000)

    def load_open_files(self):
        """Load files that were open when the application was last closed"""
        if 'openfiles' in self.settingsJson and self.settingsJson['openfiles']:
            for file_path in self.settingsJson['openfiles']:
                if os.path.exists(file_path):
                    self.set_new_tab(Path(file_path))
                else:
                    # File no longer exists, remove it from settings
                    self.settingsJson['openfiles'].remove(file_path)
                    with open(self.settings_path, 'w') as file:
                        json.dump(self.settingsJson, file, indent=2)

    def save_open_files(self):
        """Save currently open files to settings.json"""
        open_files = []
        for index in range(self.tab_view.count()):
            if index in self.tab_file_map and self.tab_file_map[index] is not None:
                open_files.append(self.tab_file_map[index])
        
        self.settingsJson['openfiles'] = open_files
        with open(self.settings_path, 'w') as file:
            json.dump(self.settingsJson, file, indent=2)

    def init_ui(self):
        self.setWindowTitle("NucleoIDE")
        # Use get_resource_path for icons and resources
        logo_path = self.get_resource_path("src/icons/logo.png")
        self.setWindowIcon(QIcon(logo_path))
        # Load stylesheet using get_resource_path
        self.window_font = QFont("Courier New", 12) 
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        # Create main container
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Add menu bar to main layout
        self.set_up_menu()
        
        # Set up body
        self.set_up_body()
        main_layout.addWidget(self.body_frame, 1)
        # Set up status bar
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "Good Morning"
        elif 12 <= current_hour < 17:
            greeting = "Good Afternoon"
        elif 17 <= current_hour < 21:
            greeting = "Good Evening"
        else:
            greeting = "Good Night"
        self.statusBar().showMessage(f"Hi there, {greeting}",10000)
        self.statusBar().setStyleSheet('''
                                        QStatusBar {
                                            background-color: black;
                                            color: white;
                                            padding-left:10px;
                                            min-height:25px;
                                        }
                                        ''')
        # Set central widget
        self.setCentralWidget(central_widget)
        # Remove the fixed size to allow maximizing
        self.setMinimumSize(800, 600)
        
        self.show()
    
    def set_up_menu(self):
        # Create menu bar
        menubar = self.menuBar()
        
        # Style the menu bar
        menubar.setStyleSheet('''
            QMenuBar {
                background-color: #596477;
                color: white;
                font-size: 16px;
                font-family: 'Courier New';
            }
            QMenuBar::item {
                color: white;
            }
            QMenuBar::item:selected {
                background-color: grey;
                color: white;
            }
            QMenu {
                background-color: #596477;
                color: white;
            }
            QMenu::item {
                background-color: #596477;
                color: white;
            }
            QMenu::item:selected {
                background-color: grey;
            }
            QMenu::item:disabled {
                color: gray;
            }
        ''')
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # New file action
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Open folder action
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.setShortcut("Ctrl+K, Ctrl+O")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        # Save file action
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save as action
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Undo action
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # Redo action
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut action
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        # Paste action
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Theme submenu
        theme_menu = view_menu.addMenu("Theme")
        
        # Light theme action
        self.light_action = QAction("Light", self)
        self.light_action.setCheckable(True)
        self.light_action.triggered.connect(self.set_light_theme)
        theme_menu.addAction(self.light_action)
        
        # Dark theme action
        self.dark_action = QAction("Dark", self)
        self.dark_action.setCheckable(True)
        self.dark_action.triggered.connect(self.set_dark_theme)
        theme_menu.addAction(self.dark_action)
        
        # Run menu
        run_menu = menubar.addMenu("Run")
        
        # Run code action
        run_action = QAction("Run Code", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_hide_settings_panel)
        tools_menu.addAction(settings_action)
        
        # Add action
        add_action = QAction("Add", self)
        add_action.triggered.connect(self.show_hide_add_panel)
        tools_menu.addAction(add_action)
        
        # BioTools action
        biotools_action = QAction("BioTools", self)
        biotools_action.triggered.connect(self.show_hide_biotools_panel)
        tools_menu.addAction(biotools_action)
        
        # Chatbot action
        chatbot_action = QAction("Chatbot", self)
        chatbot_action.triggered.connect(self.show_hide_chatbot_panel)
        tools_menu.addAction(chatbot_action)
        
        # Git action
        git_action = QAction("Git", self)
        git_action.triggered.connect(self.show_hide_git_panel)
        tools_menu.addAction(git_action)

    def set_light_theme(self):
        self.settingsJson['themeColors']['sideBar'] = "#4f596a"
        self.settingsJson['theme'] = "light"
        with open(self.settings_path, 'w') as file:
            json.dump(self.settingsJson, file, indent=2)
        self.side_bar.setStyleSheet(f'''
            background-color:{self.settingsJson['themeColors']['sideBar']};
        ''') 
        self.light_action.setChecked(True)
        self.dark_action.setChecked(False)

    def set_dark_theme(self):
        self.settingsJson['themeColors']['sideBar'] = "#1a1a1a"
        self.settingsJson['theme'] = "dark"
        with open(self.settings_path, 'w') as file:
            json.dump(self.settingsJson, file, indent=2)
        self.side_bar.setStyleSheet(f'''
            background-color:{self.settingsJson['themeColors']['sideBar']};
        ''') 
        self.dark_action.setChecked(True)
        self.light_action.setChecked(False)

    def get_editor(self) -> QsciScintilla:
        editor = QsciScintilla()
        editor.setUtf8(True)
        editor.setFont(self.window_font)

        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        editor.setIndentationGuides(True)
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)

        # EOL
        editor.setEolMode(QsciScintilla.EolWindows)
        editor.setEolVisibility(False)

        # We'll connect the textChanged signal later in set_new_tab
        # This prevents the signal from triggering during initial file loading
        
        # Determine lexer based on file extension
        current_index = self.tab_view.currentIndex()
        file_path = None
        
        # First try to get file path from tab_file_map
        if current_index in self.tab_file_map:
            file_path = self.tab_file_map[current_index]
        # Fallback to current_file
        elif self.current_file:
            file_path = str(self.current_file)
            
        # Set lexer based on file extension
        if file_path and file_path.endswith('.py'):
            # Python lexer
            lexer = QsciLexerPython()
            lexer.setFont(self.window_font)
            lexer.setDefaultFont(self.window_font)
            
            lexer.setColor(QColor("#ffffff"))
            lexer.setColor(QColor("#FF0000"), QsciLexerPython.Keyword)
            lexer.setColor(QColor("#008000"), QsciLexerPython.Comment)
            lexer.setColor(QColor("#008000"), QsciLexerPython.DoubleQuotedString)
            lexer.setColor(QColor("#008000"), QsciLexerPython.SingleQuotedString)
            lexer.setColor(QColor(255, 165, 0), QsciLexerPython.Identifier)
            lexer.setColor(QColor("pink"), QsciLexerPython.Operator)
            lexer.setColor(QColor("cyan"), QsciLexerPython.ClassName)
            lexer.setColor(QColor("yellow"), QsciLexerPython.FunctionMethodName)
            
            lexer.setDefaultPaper(QColor("#2f343e"))
            lexer.setPaper(QColor("#2f343e"))
        else:
            # Default to Perl lexer
            lexer = QsciLexerPerl()
            lexer.setFont(self.window_font) 
            lexer.setDefaultFont(self.window_font) 
            
            lexer.setColor(QColor(255, 165, 0), QsciLexerPerl.Identifier)
            lexer.setColor(QColor("#ffffff"))
            lexer.setColor(QColor("#FF0000"), QsciLexerPerl.Keyword) 
            lexer.setColor(QColor("#008000"), QsciLexerPerl.Comment)
            lexer.setColor(QColor("#008000"), QsciLexerPerl.POD)
            lexer.setColor(QColor("#008000"), QsciLexerPerl.DoubleQuotedString)
            lexer.setColor(QColor("#008000"), QsciLexerPerl.DoubleQuotedString)  
            lexer.setColor(QColor("green"), QsciLexerPerl.Scalar) 
            lexer.setColor(QColor("green"), QsciLexerPerl.Hash)        
            lexer.setColor(QColor(255, 165, 0), QsciLexerPerl.Array)
            lexer.setColor(QColor("pink"), QsciLexerPerl.Operator)
            
            lexer.setDefaultPaper(QColor("#2f343e"))
            lexer.setPaper(QColor("#2f343e"))

        editor.setMarginsBackgroundColor(QColor("#2f343e"))
        editor.setMarginsForegroundColor(QColor("white"))
        
        editor.setLexer(lexer)
        editor.setMarginType(0, QsciScintilla.NumberMargin)
        
        editor.setMarginWidth(0, "00000")
        editor.setCaretForegroundColor(QColor("white")) 
        editor.setCaretLineVisible(True) 
        editor.setCaretLineBackgroundColor(QColor("#363b45")) 
        return editor

    def is_binary(self, path):
        '''
        Check if file is binary or a known non-text type by extension, but allow images
        '''
        # List of known image file extensions
        image_exts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg']
        # List of known non-text file extensions (excluding images)
        non_text_exts = [
            '.pdf', '.exe', '.dll', '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.wav', '.ogg', '.bin', '.obj', '.class', '.so', '.dylib', '.psd', '.ai', '.eps', '.ttf', '.otf', '.woff', '.woff2', '.apk', '.iso', '.img', '.msi', '.cab', '.sys', '.dat', '.db', '.sqlite', '.mdb', '.accdb', '.ppt', '.pptx', '.xls', '.xlsx', '.doc', '.docx', '.rtf', '.chm', '.swf', '.fla', '.jar', '.crx', '.xpi', '.vbs', '.scr', '.msu', '.msp', '.bat', '.com', '.pif', '.cpl', '.msc', '.lnk', '.tmp', '.torrent', '.sav']
        ext = os.path.splitext(str(path))[1].lower()
        if ext in image_exts:
            return False  # Allow images
        if ext in non_text_exts:
            return True
        try:
            with open(path, 'rb') as f:
                return b'\0' in f.read(1024)
        except Exception:
            return True  # If we can't read the file, treat as binary

    def check_for_modifications(self, index):
        """Check if content has been modified compared to original/saved version"""
        if index == -1 or self.loading_file:
            return
        
        editor = self.tab_view.widget(index)
        if not editor:
            return
            
        current_content = editor.text()
        
        # For untitled files, any content means it's modified
        if index not in self.tab_file_map or self.tab_file_map[index] is None:
            if current_content.strip():  # If there's any non-whitespace content
                self.mark_tab_as_modified(index)
            else:
                self.mark_tab_as_saved(index)
            return
            
        # For existing files, compare with original content
        if index in self.original_content:
            if current_content != self.original_content[index]:
                self.mark_tab_as_modified(index)
            else:
                self.mark_tab_as_saved(index)

    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()

        if is_new_file:
            new_tab_index = self.tab_view.addTab(editor, "untitled")
            self.tab_file_map[new_tab_index] = None  # No file associated yet
            self.original_content[new_tab_index] = ""  # Empty content for new files
            self.setWindowTitle("untitled")
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(new_tab_index)
            self.current_file = None
            editor.textChanged.connect(lambda: self.check_for_modifications(new_tab_index))
            return

        if not path.is_file():
            return

        # Handle image files
        image_exts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg']
        ext = os.path.splitext(str(path))[1].lower()
        if ext in image_exts:
            try:
                viewer = ImageViewer(str(path))
                new_tab_index = self.tab_view.addTab(viewer, path.name)
                self.tab_file_map[new_tab_index] = str(path.absolute())
                self.original_content[new_tab_index] = None  # Not used for images
                self.tab_view.setCurrentIndex(new_tab_index)
                self.setWindowTitle(path.name)
                self.statusBar().showMessage(f"Opened image: {path.name}", 2000)
                return
            except Exception as e:
                self.statusBar().showMessage(f"Error displaying image: {str(e)}", 4000)
            return
        
        if self.is_binary(path):
            self.statusBar().showMessage("This file is not readable as text.", 4000)
            return

        # Check if the file is already open in a tab
        for i in range(self.tab_view.count()):
            if i in self.tab_file_map and self.tab_file_map[i] == str(path.absolute()):
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        self.current_file = path
        editor = self.get_editor()  # Now that current_file is set, get_editor will use the right lexer
        
        # Try different encodings to read the file
        encodings = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']
        original_content = None
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    original_content = f.read()
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.statusBar().showMessage(f"Error reading file: {str(e)}", 2000)
                return
        
        if original_content is None:
            self.statusBar().showMessage("Could not read file with any supported encoding", 2000)
            return
        
        new_tab_index = self.tab_view.addTab(editor, path.name)
        self.tab_file_map[new_tab_index] = str(path.absolute())  # Store the file path
        self.original_content[new_tab_index] = original_content  # Store for comparison
        
        # Set loading flag to prevent modification marking during file loading
        self.loading_file = True
        editor.setText(original_content)
        self.loading_file = False
        
        # Explicitly ensure the tab is not marked as modified
        if new_tab_index in self.modified_tabs:
            self.mark_tab_as_saved(new_tab_index)
        
        self.setWindowTitle(path.name)
        self.tab_view.setCurrentIndex(new_tab_index)
        
        # Connect the textChanged signal with specific tab index
        editor.textChanged.connect(lambda: self.check_for_modifications(new_tab_index))
        
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

    def set_up_body(self):
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet('''
            QToolBar {
                background-color: #596477;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: #596477;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #6B7A8F;
            }
            QToolButton:pressed {
                background-color: #4A5568;
            }
        ''')
        
        # Add run button
        run_button = QToolButton()
        run_button.setIcon(QIcon(self.get_resource_path('icons/run.png')))
        run_button.setToolTip('Run Code (F5)')
        run_button.clicked.connect(self.run_code)
        toolbar.addWidget(run_button)
        
        # Add toolbar to main layout
        main_layout.addWidget(toolbar)
        
        # Create horizontal splitter for left and right panels
        hsplitter = QSplitter(Qt.Horizontal)
        
        # Create left panel (file tree)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Create file tree
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setStyleSheet('''
            QTreeView {
                background-color: #2D3748;
                color: white;
                border: none;
                font-family: 'Courier New';
                font-size: 14px;
            }
            QTreeView::item {
                padding: 5px;
            }
            QTreeView::item:selected {
                background-color: #4A5568;
            }
            QTreeView::item:hover {
                background-color: #4A5568;
            }
        ''')
        
        # Create file system model
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.tree_view.setModel(self.file_model)
        
        # Hide unnecessary columns
        for i in range(1, 4):
            self.tree_view.hideColumn(i)
        
        # Add tree view to left panel
        left_layout.addWidget(self.tree_view)
        
        # Create right panel (editor and output)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Create tab widget for editor
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.tab_widget.setStyleSheet('''
            QTabWidget::pane {
                border: none;
                background-color: #2D3748;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #4A5568;
                color: white;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-family: 'Courier New';
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #596477;
            }
            QTabBar::tab:hover {
                background-color: #6B7A8F;
            }
            QTabBar::close-button {
                image: url(icons/close.png);
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background-color: #E53E3E;
                border-radius: 2px;
            }
        ''')
        
        # Add tab widget to right panel
        right_layout.addWidget(self.tab_widget)
        
        # Create bottom panel (output and terminal)
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        # Create tab widget for bottom panel
        self.bottom_tab_widget = QTabWidget()
        self.bottom_tab_widget.setTabsClosable(True)
        self.bottom_tab_widget.tabCloseRequested.connect(self.toggle_output_panel)
        self.bottom_tab_widget.currentChanged.connect(self.handle_bottom_panel_tab_change)
        self.bottom_tab_widget.setStyleSheet('''
            QTabWidget::pane {
                border: none;
                background-color: #2D3748;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #4A5568;
                color: white;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-family: 'Courier New';
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #596477;
            }
            QTabBar::tab:hover {
                background-color: #6B7A8F;
            }
            QTabBar::close-button {
                image: url(icons/close.png);
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background-color: #E53E3E;
                border-radius: 2px;
            }
        ''')
        
        # Create output text edit
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_text.customContextMenuRequested.connect(self.show_output_context_menu)
        self.output_text.setStyleSheet('''
            QTextEdit {
                background-color: #2D3748;
                color: white;
                border: none;
                font-family: 'Courier New';
                font-size: 14px;
                padding: 10px;
            }
        ''')
        
        # Create terminal emulator
        self.terminal = CommandPromptEmulator(self, self.settingsJson)
        self.terminal.setStyleSheet('''
            QTextEdit {
                background-color: #2D3748;
                color: white;
                border: none;
                font-family: 'Courier New';
                font-size: 14px;
                padding: 10px;
            }
        ''')
        
        # Add output and terminal to bottom tab widget
        self.bottom_tab_widget.addTab(self.output_text, "Output")
        self.bottom_tab_widget.addTab(self.terminal, "Terminal")
        
        # Add bottom tab widget to bottom panel
        bottom_layout.addWidget(self.bottom_tab_widget)
        
        # Add panels to splitter
        hsplitter.addWidget(left_panel)
        hsplitter.addWidget(right_panel)
        
        # Set initial sizes
        hsplitter.setSizes([200, 600])
        
        # Add splitter to main layout
        main_layout.addWidget(hsplitter)
        
        # Add bottom panel to main layout
        main_layout.addWidget(bottom_panel)
        
        # Set main widget as central widget
        self.setCentralWidget(main_widget)
        
        # Load last directory
        self.load_last_directory()
        
        # Load output and terminal cache
        self.load_output_and_terminal_cache()

    def show_output_context_menu(self, position):
        """Show context menu for output panel"""
        context_menu = QMenu()
        clear_action = context_menu.addAction("Clear Output")
        copy_action = context_menu.addAction("Copy")
        select_all_action = context_menu.addAction("Select All")
        
        # Connect actions to functions
        clear_action.triggered.connect(self.clear_output)
        copy_action.triggered.connect(self.output_widget.copy)
        select_all_action.triggered.connect(self.output_widget.selectAll)
        
        # Show the menu at the cursor position
        context_menu.exec_(self.output_widget.mapToGlobal(position))

    def execute_command(self):
        command = self.input_field.text().strip()
        if command:
            self.process.write((command + "\n").encode('utf-8'))
            self.output_area.appendPlainText(f"> {command}")  
            self.input_field.clear()

    def read_output(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8')
        self.output_area.appendPlainText(output)

    def read_error(self):
        error = self.process.readAllStandardError().data().decode('utf-8')
        self.output_area.appendPlainText(error)

    def close_tab(self, index):
        # Check for unsaved changes
        if index in self.modified_tabs:
            tab_text = self.tab_view.tabText(index)
            if tab_text.startswith('• '):
                tab_text = tab_text[2:]  # Remove the dot for display
                
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"The file '{tab_text}' has unsaved changes. Do you want to save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                # Save the current tab before closing
                current_tab = self.tab_view.currentIndex()
                self.tab_view.setCurrentIndex(index)
                saved = self.save_file()
                # If saving was cancelled, don't close the tab
                if not saved:
                    return
                self.tab_view.setCurrentIndex(current_tab)
            elif reply == QMessageBox.Cancel:
                return  # Don't close the tab
        
        # Remove the file path from our mapping
        if index in self.tab_file_map:
            del self.tab_file_map[index]
        
        # Remove from modified tabs set if present
        if index in self.modified_tabs:
            self.modified_tabs.remove(index)
            
        # Remove from original content
        if index in self.original_content:
            del self.original_content[index]
            
        # Remap indices after tab is closed
        new_map = {}
        new_modified = set()
        new_original = {}
        for i in range(self.tab_view.count()):
            if i >= index and i+1 in self.tab_file_map:
                new_map[i] = self.tab_file_map[i+1]
            elif i in self.tab_file_map:
                new_map[i] = self.tab_file_map[i]
                
            # Update modified tabs indices
            if i >= index and i+1 in self.modified_tabs:
                new_modified.add(i)
            elif i in self.modified_tabs:
                new_modified.add(i)
                
            # Update original content
            if i >= index and i+1 in self.original_content:
                new_original[i] = self.original_content[i+1]
            elif i in self.original_content:
                new_original[i] = self.original_content[i]
                
        self.tab_file_map = new_map
        self.modified_tabs = new_modified
        self.original_content = new_original
        
        self.tab_view.removeTab(index)

    def show_hide_tab(self):
        if self.tree_frame.isVisible():
            self.tree_frame.hide()
            self.folder_button.setChecked(False)
        else:
            self.tree_frame.show()
            self.folder_button.setChecked(True)
            # Hide other panels and uncheck their buttons
            if self.settings_panel.isVisible():
                self.settings_panel.hide()
            if self.add_panel.isVisible():
                self.add_panel.hide()
            if self.biotools_panel.isVisible():
                self.biotools_panel.hide()
                self.biotools_button.setChecked(False)
            if self.chatbot_panel.isVisible():
                self.chatbot_panel.hide()
                self.chatbot_button.setChecked(False)
            if self.git_panel.isVisible():
                self.git_panel.hide()
                self.git_button.setChecked(False)

    def show_hide_settings_panel(self):
        if self.settings_panel.isVisible():
            self.settings_panel.hide()
            self.settings_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        else:
            self.settings_panel.show()
            self.settings_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
            self.add_panel.hide()
            self.biotools_panel.hide()
            self.chatbot_panel.hide()
            self.git_panel.hide()

    def show_hide_add_panel(self):
        if self.add_panel.isVisible():
            self.add_panel.hide()
            self.add_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        else:
            self.add_panel.show()
            self.add_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
            self.settings_panel.hide()
            self.biotools_panel.hide()
            self.chatbot_panel.hide()
            self.git_panel.hide()

    def show_hide_biotools_panel(self):
        if self.biotools_panel.isVisible():
            self.biotools_panel.hide()
            self.biotools_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        else:
            self.biotools_panel.show()
            self.biotools_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
            self.settings_panel.hide()
            self.add_panel.hide()
            self.chatbot_panel.hide()
            self.git_panel.hide()

    def show_hide_chatbot_panel(self):
        if self.chatbot_panel.isVisible():
            self.chatbot_panel.hide()
            self.chatbot_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        else:
            self.chatbot_panel.show()
            self.chatbot_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
            self.settings_panel.hide()
            self.add_panel.hide()
            self.biotools_panel.hide()
            self.git_panel.hide()

    def show_hide_git_panel(self):
        if self.git_panel.isVisible():
            self.git_panel.hide()
            self.git_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
        else:
            self.git_panel.show()
            self.git_panel.setFixedWidth(self.STANDARD_PANEL_WIDTH)
            self.settings_panel.hide()
            self.add_panel.hide()
            self.biotools_panel.hide()
            self.chatbot_panel.hide()

    def tree_view_context_menu(self, pos):
        index = self.tree_view.indexAt(pos)
        menu = QMenu()
        
        if not index.isValid():
            # Handle empty area click
            new_file_action = menu.addAction("New File")
            new_file_action.triggered.connect(lambda: self.create_new_file(self.tree_view.rootIndex()))
            
            new_folder_action = menu.addAction("New Folder")
            new_folder_action.triggered.connect(lambda: self.create_new_folder(self.tree_view.rootIndex()))
            
            menu.exec_(self.tree_view.viewport().mapToGlobal(pos))
            return
            
        # Handle file/folder click
        path = self.model.filePath(index)
        
        # Check if it's a directory
        if os.path.isdir(path):
            # Add new file/folder options for directories
            new_file_action = menu.addAction("New File")
            new_file_action.triggered.connect(lambda: self.create_new_file(index))
            
            new_folder_action = menu.addAction("New Folder")
            new_folder_action.triggered.connect(lambda: self.create_new_folder(index))
            
            menu.addSeparator()
        
        # Add rename action
        rename_action = menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.rename_file_or_folder(index))
        
        # Add delete action
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_file_or_folder(index))
        
        menu.addSeparator()
        
        # Add copy path options
        copy_full_path_action = menu.addAction("Copy Full Path")
        copy_full_path_action.triggered.connect(lambda: self.copy_path_to_clipboard(path, full_path=True))
        
        copy_relative_path_action = menu.addAction("Copy Relative Path")
        copy_relative_path_action.triggered.connect(lambda: self.copy_path_to_clipboard(path, full_path=False))
        
        menu.exec_(self.tree_view.viewport().mapToGlobal(pos))

    def create_new_file(self, parent_index):
        """Create a new file in the selected directory"""
        try:
            # Get the directory path
            if parent_index.isValid():
                dir_path = self.model.filePath(parent_index)
            else:
                dir_path = self.model.rootPath()
            
            # Create a dialog to get the file name
            file_name, ok = QInputDialog.getText(
                self,
                "New File",
                "Enter file name:",
                text="untitled.txt"
            )
            
            if ok and file_name:
                # Create the full path
                file_path = os.path.join(dir_path, file_name)
                
                # Check if the file already exists
                if os.path.exists(file_path):
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"A file with the name '{file_name}' already exists."
                    )
                    return
                
                # Create the file
                with open(file_path, 'w') as f:
                    pass
                
                # Update the model to reflect the change
                self.model.setRootPath(self.model.rootPath())
                
                # Open the new file in a tab
                self.set_new_tab(Path(file_path))
                
                self.statusBar().showMessage(f"Created new file: {file_name}", 2000)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create file: {str(e)}"
            )

    def create_new_folder(self, parent_index):
        """Create a new folder in the selected directory"""
        try:
            # Get the directory path
            if parent_index.isValid():
                dir_path = self.model.filePath(parent_index)
            else:
                dir_path = self.model.rootPath()
            
            # Create a dialog to get the folder name
            folder_name, ok = QInputDialog.getText(
                self,
                "New Folder",
                "Enter folder name:",
                text="New Folder"
            )
            
            if ok and folder_name:
                # Create the full path
                folder_path = os.path.join(dir_path, folder_name)
                
                # Check if the folder already exists
                if os.path.exists(folder_path):
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"A folder with the name '{folder_name}' already exists."
                    )
                    return
                
                # Create the folder
                os.makedirs(folder_path)
                
                # Update the model to reflect the change
                self.model.setRootPath(self.model.rootPath())
                
                self.statusBar().showMessage(f"Created new folder: {folder_name}", 2000)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create folder: {str(e)}"
            )

    def copy_path_to_clipboard(self, path, full_path=True):
        """Copy file/folder path to clipboard"""
        try:
            if full_path:
                # Copy absolute path
                path_to_copy = os.path.abspath(path)
            else:
                # Copy path relative to the current root directory
                root_path = self.model.rootPath()
                path_to_copy = os.path.relpath(path, root_path)
            
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(path_to_copy)
            
            # Show success message
            self.statusBar().showMessage(f"Path copied to clipboard: {path_to_copy}", 2000)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to copy path: {str(e)}"
            )

    def rename_file_or_folder(self, index):
        """Handle renaming of files and folders"""
        if not index.isValid():
            return
            
        path = self.model.filePath(index)
        old_name = os.path.basename(path)
        
        # Create a dialog to get the new name
        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "Enter new name:",
            text=old_name
        )
        
        if ok and new_name and new_name != old_name:
            try:
                # Get the directory path
                dir_path = os.path.dirname(path)
                # Create the new full path
                new_path = os.path.join(dir_path, new_name)
                
                # Check if the new name already exists
                if os.path.exists(new_path):
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"A file or folder with the name '{new_name}' already exists."
                    )
                    return
                
                # Rename the file or folder
                os.rename(path, new_path)
                
                # Update the model to reflect the change
                self.model.setRootPath(self.model.rootPath())
                
                # If the renamed file is open in a tab, update the tab
                for tab_index in range(self.tab_view.count()):
                    if tab_index in self.tab_file_map and self.tab_file_map[tab_index] == path:
                        self.tab_file_map[tab_index] = new_path
                        self.tab_view.setTabText(tab_index, new_name)
                        break
                
                self.statusBar().showMessage(f"Renamed to {new_name}", 2000)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to rename: {str(e)}"
                )

    def delete_file_or_folder(self, index):
        """Handle deletion of files and folders"""
        if not index.isValid():
            return
            
        path = self.model.filePath(index)
        name = os.path.basename(path)
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Check if it's a file or directory
                if os.path.isfile(path):
                    # If the file is open in a tab, close it first
                    for tab_index in range(self.tab_view.count()):
                        if tab_index in self.tab_file_map and self.tab_file_map[tab_index] == path:
                            self.close_tab(tab_index)
                            break
                    os.remove(path)
                else:
                    # For directories, use shutil.rmtree to remove recursively
                    import shutil
                    shutil.rmtree(path)
                
                # Update the model to reflect the change
                self.model.setRootPath(self.model.rootPath())
                
                self.statusBar().showMessage(f"Deleted {name}", 2000)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to delete: {str(e)}"
                )

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)

    def new_file(self):
        self.loading_file = True  # Prevent modification marking during setup
        self.set_new_tab(None, is_new_file=True)
        self.loading_file = False

    def save_file(self):
        current_index = self.tab_view.currentIndex()
        if current_index == -1:
            return False  # No open tabs
            
        editor = self.tab_view.currentWidget()
        
        # Check if this is an unsaved file
        if current_index not in self.tab_file_map or self.tab_file_map[current_index] is None:
            return self.save_as()
        
        # Get the file path from our mapping
        file_path = self.tab_file_map[current_index]
        file_obj = Path(file_path)
        
        # Save the file
        current_content = editor.text()
        file_obj.write_text(current_content)
        
        # Update the original content for this tab
        self.original_content[current_index] = current_content
        
        self.statusBar().showMessage(f"Saved {file_obj.name}", 2000)
        
        # Mark the tab as saved (remove the dot)
        self.mark_tab_as_saved(current_index)
        
        # Update current_file to match the active tab
        self.current_file = file_obj
        return True

    def save_as(self):
        current_index = self.tab_view.currentIndex()
        if current_index == -1:
            return False  # No open tabs
            
        editor = self.tab_view.currentWidget()
        if editor is None:
            return False
        
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == "":
            self.statusBar().showMessage("Cancelled", 2000)
            return False
        
        path = Path(file_path)
        current_content = editor.text()
        path.write_text(current_content)
        
        # Update tab text and mapping
        tab_text = path.name
        
        # Set loading flag to prevent triggering modification detection
        self.loading_file = True
        self.tab_view.setTabText(current_index, tab_text)
        self.loading_file = False
        
        self.tab_file_map[current_index] = str(path.absolute())
        
        # Update the original content for this tab
        self.original_content[current_index] = current_content
        
        # Mark the tab as saved
        self.mark_tab_as_saved(current_index)
        
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path
        return True


    def open_file(self):
        ops=QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        new_file, _ =QFileDialog.getOpenFileName(self,"Choose a File","","All Files (*);;Perl Files (*.pl)",options=ops)

        if new_file=='':
            self.statusBar().showMessage("Cancelled",2000)
            return

        f=Path(new_file)
        self.set_new_tab(f)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            # Close all open tabs
            while self.tab_view.count() > 0:
                self.close_tab(0)
            
            # Clear the tab file map and modified tabs
            self.tab_file_map.clear()
            self.modified_tabs.clear()
            self.original_content.clear()
            
            # Reset the current file
            self.current_file = None
            
            # Convert to absolute path and normalize
            folder = os.path.abspath(folder)
            
            # Update the model
            self.model.setRootPath(folder)
            self.tree_view.setRootIndex(self.model.index(folder))
            self.tree_view.show()
            self.open_folder_btn.hide()
            
            # Update settings
            self.settingsJson['openMainFolder'] = folder
            with open(self.settings_path, 'w') as file:
                json.dump(self.settingsJson, file, indent=2)
            
            # Update terminal
            if hasattr(self, 'cmd_widget'):
                self.cmd_widget.settings = self.settingsJson
                self.cmd_widget.current_directory = folder
                self.cmd_widget.clear_and_reset()
            
            self.statusBar().showMessage(f"Opened folder: {folder}")
            self.save_last_directory()

    def undo(self):
        editor=self.tab_view.currentWidget()
        if editor is not None:
            editor.undo()

    def redo(self):
        editor=self.tab_view.currentWidget()
        if editor is not None:
            editor.redo()

    def cut(self):
        editor=self.tab_view.currentWidget()
        if editor is not None:
            editor.cut()

    def copy(self):
        editor=self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()
    
    def paste(self):
        editor=self.tab_view.currentWidget()
        if editor is not None:
            editor.paste()

    def open_welcome_page(self):
        file_path = self.get_resource_path("src/app_pages/about.html")
        if os.path.exists(file_path):
            webbrowser.open(f"file://{file_path}")
        else:
            self.statusBar().showMessage("Welcome Web Page missing")

    def run_code(self):
        if not (self.bottom_panel.isVisible()):
            self.toggle_output_panel()  # Use the toggle method for consistency
        self.bottom_panel.setCurrentWidget(self.output_widget)
        current_index = self.tab_view.currentIndex()
        if current_index == -1:
            self.output_widget.append("\n\nNo file open to run.")
            return

        # Always save the current file before running
        saved = self.save_file()
        if not saved:
            # If save was cancelled, don't run the code
            self.statusBar().showMessage("Code execution cancelled - file not saved", 3000)
            return

        file_name = self.tab_view.tabText(current_index)
        # Remove the dot if it's an unsaved file (in case user chose "Run without saving")
        if file_name.startswith('• '):
            file_name = file_name[2:]
            
        if self.current_file and self.current_file.name == file_name:
            file_path = str(self.current_file.absolute())
        else:
            file_path = os.path.abspath(os.path.join(os.getcwd(), file_name))

        try:
            # Create a temporary file for Perl with unbuffered stdout
            temp_perl_file = None
            
            # Determine which interpreter to use based on file extension
            if file_path.endswith(".pl"):
                # Use the Perl interpreter from src/interpretor/perl/perl/bin
                interpreter = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interpretor", "perl", "perl", "bin", "perl.exe")
                if not os.path.exists(interpreter):
                    self.output_widget.append("\n\nError: Perl interpreter not found at " + interpreter)
                    return
                
                # For Perl, we'll create a temporary file with autoflush enabled
                import tempfile
                with open(file_path, 'r') as original_file:
                    content = original_file.read()
                
                # Create temp file with STDOUT autoflush
                temp_perl_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pl', mode='w')
                autoflush_code = """
# Added by NucleoIDE for real-time output
use IO::Handle;
STDOUT->autoflush(1);
STDERR->autoflush(1);
"""
                # Add autoflush code right after "use" statements if any, or at the beginning
                if "use " in content:
                    # Find the last 'use' statement
                    lines = content.split('\n')
                    last_use_idx = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith('use '):
                            last_use_idx = i
                    
                    # Insert autoflush after the last use statement
                    lines.insert(last_use_idx + 1, autoflush_code)
                    modified_content = '\n'.join(lines)
                else:
                    # Add to the beginning of the file
                    modified_content = autoflush_code + content
                
                temp_perl_file.write(modified_content)
                temp_perl_file.close()
                
                # Use the temporary file instead
                interpreter_args = [temp_perl_file.name]
                
            elif file_path.endswith(".py"):
                # Use the Python interpreter from src/interpretor/python
                interpreter = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interpretor", "python", "python.exe")
                if not os.path.exists(interpreter):
                    self.output_widget.append("\n\nError: Python interpreter not found at " + interpreter)
                    return
                # Add -u flag to Python to force unbuffered output
                interpreter_args = ["-u", file_path]
            else:
                self.output_widget.append("\n\nUnsupported file type. Only .pl (Perl) and .py (Python) files can be executed.")
                return

            # Add a separator line between executions
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.output_widget.append("\n\n" + "=" * 50)
            self.output_widget.append(f"[{current_time}] Running {os.path.basename(interpreter)}: {file_path}")
            self.output_widget.append("=" * 50 + "\n")
            QApplication.processEvents()  # Force immediate update
            
            # Set up process for live output
            if self.process_output is not None and self.process_output.state() == QProcess.Running:
                # If there's already a process running, inform the user
                self.output_widget.append("A process is already running. Please wait for it to complete or terminate it.")
                # Clean up temp file if it exists
                if temp_perl_file and os.path.exists(temp_perl_file.name):
                    os.unlink(temp_perl_file.name)
                return
                
            # Create a new process for this run
            self.process_output = QProcess(self)
            
            # Store temp file reference for cleanup
            self.temp_perl_file = temp_perl_file
            
            # Configure for real-time output
            self.process_output.setProcessChannelMode(QProcess.MergedChannels)  # Merge stdout and stderr
            self.process_output.setReadChannel(QProcess.StandardOutput)  # Set read channel to standard output
            
            # Connect signals for real-time output
            self.process_output.readyReadStandardOutput.connect(self.handle_output)
            self.process_output.readyReadStandardError.connect(self.handle_error)
            self.process_output.finished.connect(self.process_finished)
            
            # Create and show the terminate button
            if not hasattr(self, 'terminate_button') or self.terminate_button is None:
                # Create a new button if it doesn't exist
                self.terminate_button = QPushButton("Stop")
                self.terminate_button.setStyleSheet('''
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                ''')
                self.terminate_button.clicked.connect(self.terminate_process)
            
            # Show the terminate button
            self.bottom_panel.setCornerWidget(self.terminate_button, Qt.TopRightCorner)
            self.terminate_button.show()
            
            # Start the process with proper arguments
            self.process_output.start(interpreter, interpreter_args)
            
            # Print command for debugging
            if file_path.endswith(".pl"):
                self.statusBar().showMessage(f"Running: {os.path.basename(interpreter)} (with autoflush enabled)", 5000)
            else:
                self.statusBar().showMessage(f"Running: {os.path.basename(interpreter)} {' '.join(interpreter_args)}", 5000)

        except Exception as e:
            self.output_widget.append(f"\n\nExecution failed:\n{str(e)}")
            # Clean up temp file if it exists
            if temp_perl_file and os.path.exists(temp_perl_file.name):
                os.unlink(temp_perl_file.name)
    
    def handle_output(self):
        """Handle standard output from the process with improved real-time display"""
        try:
            # Get output data
            data = self.process_output.readAllStandardOutput().data()
            # Try different encodings
            try:
                output = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    output = data.decode('cp1252')
                except UnicodeDecodeError:
                    output = data.decode('utf-8', errors='replace')
            # Append text to output widget
            if output:
                self.output_widget.moveCursor(QTextCursor.End)
                self.output_widget.insertPlainText(output)
                self.output_widget.ensureCursorVisible()
                # Append to OutputCache file
                try:
                    with open(self.output_cache_path, 'a', encoding='utf-8') as f:
                        f.write(output)
                except Exception:
                    pass
                # Force UI update immediately
                QApplication.processEvents()
        except Exception as e:
            # Log any errors that occur during output handling
            print(f"Error handling process output: {e}")
    
    def handle_error(self):
        """Handle standard error from the process with improved real-time display"""
        try:
            # Get error data
            data = self.process_output.readAllStandardError().data()
            # Try different encodings
            try:
                error = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    error = data.decode('cp1252')
                except UnicodeDecodeError:
                    error = data.decode('utf-8', errors='replace')
            # Append error text in red to output widget
            if error:
                cursor = self.output_widget.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.output_widget.setTextCursor(cursor)
                # Use red color for errors
                error_format = QTextCharFormat()
                error_format.setForeground(QColor("red"))
                cursor.setCharFormat(error_format)
                cursor.insertText(error)
                # Reset format to default
                cursor.setCharFormat(QTextCharFormat())
                self.output_widget.ensureCursorVisible()
                # Append to OutputCache file
                try:
                    with open(self.output_cache_path, 'a', encoding='utf-8') as f:
                        f.write(error)
                except Exception:
                    pass
                # Force UI update immediately
                QApplication.processEvents()
        except Exception as e:
            # Log any errors that occur during error handling
            print(f"Error handling process error output: {e}")
            
    def process_finished(self):
        exit_code = self.process_output.exitCode()
        self.output_widget.append(f"\n[Done] Exit Code: {exit_code}")
        self.output_widget.ensureCursorVisible()
        
        # Remove the terminate button when process finishes and show the clear output button
        if hasattr(self, 'terminate_button'):
            self.terminate_button.hide()
            
        # Show clear output button instead
        if not hasattr(self, 'clear_output_button') or self.clear_output_button is None:
            self.clear_output_button = QPushButton("Clear Output")
            self.clear_output_button.setStyleSheet('''
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            ''')
            self.clear_output_button.clicked.connect(self.clear_output)
        
        self.bottom_panel.setCornerWidget(self.clear_output_button, Qt.TopRightCorner)
        self.clear_output_button.show()
        
        # Clean up temporary Perl file if it exists
        if hasattr(self, 'temp_perl_file') and self.temp_perl_file and os.path.exists(self.temp_perl_file.name):
            try:
                os.unlink(self.temp_perl_file.name)
                self.temp_perl_file = None
            except Exception as e:
                print(f"Error cleaning up temporary file: {e}")
            
        # Update status bar
        self.statusBar().showMessage("Process completed.", 3000)

    def tab_changed(self, index):
        """Update current_file when the user switches tabs"""
        if index == -1:
            self.current_file = None
            self.setWindowTitle("NucleoIDE")
            return
            
        if index in self.tab_file_map and self.tab_file_map[index] is not None:
            self.current_file = Path(self.tab_file_map[index])
            self.setWindowTitle(self.current_file.name)
        else:
            self.current_file = None
            self.setWindowTitle("untitled")

    def mark_tab_as_modified(self, index):
        """Mark a tab as having unsaved changes by adding a dot to the tab name"""
        if index == -1:
            return
        
        # Get the current tab text without any modification indicator
        tab_text = self.tab_view.tabText(index)
        if tab_text.startswith('• '):
            return  # Already marked as modified
        
        # Add the tab to our set of modified tabs
        self.modified_tabs.add(index)
        
        # Update the tab text to show it's modified
        self.tab_view.setTabText(index, f'• {tab_text}')

    def mark_tab_as_saved(self, index):
        """Remove the modification indicator from a tab name"""
        if index == -1 or index not in self.modified_tabs:
            return
        
        tab_text = self.tab_view.tabText(index)
        if tab_text.startswith('• '):
            # Remove the indicator
            self.tab_view.setTabText(index, tab_text[2:])
            
        # Remove from the set of modified tabs
        if index in self.modified_tabs:
            self.modified_tabs.remove(index)

    def toggle_output_panel(self):
        if self.bottom_panel.isVisible():
            self.bottom_panel.hide()
        else:
            self.bottom_panel.show()
            self.bottom_panel.setCurrentWidget(self.output_widget)
            
            # Add a "Clear Output" button if not already present
            if not hasattr(self, 'clear_output_button') or self.clear_output_button is None:
                self.clear_output_button = QPushButton("Clear Output")
                self.clear_output_button.setStyleSheet('''
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                ''')
                self.clear_output_button.clicked.connect(self.clear_output)
            
    def toggle_command_prompt(self):
        if self.bottom_panel.isVisible() and self.bottom_panel.currentWidget() == self.cmd_widget:
            self.bottom_panel.hide()
        else:
            self.bottom_panel.show()
            self.bottom_panel.setCurrentWidget(self.cmd_widget)

    def clear_output(self):
        """Clear the output panel"""
        self.output_widget.clear()
        self.statusBar().showMessage("Output panel cleared", 2000)

    def terminate_process(self):
        """Terminate the currently running process"""
        if self.process_output and self.process_output.state() == QProcess.Running:
            # Ask for confirmation
            reply = QMessageBox.question(
                self, 
                "Terminate Process",
                "Are you sure you want to terminate the running process?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Try to terminate gracefully first
                self.process_output.terminate()
                # Give it a chance to terminate gracefully
                if not self.process_output.waitForFinished(500):
                    # If it doesn't terminate in time, kill it
                    self.process_output.kill()
                
                self.output_widget.append("\n\n[Process terminated by user]")
                
                # Remove the terminate button
                if hasattr(self, 'terminate_button'):
                    self.terminate_button.hide()
                    self.bottom_panel.setCornerWidget(None)

    def closeEvent(self, event):
        """Handle window close event"""
        # Check if there are any unsaved changes
        if self.modified_tabs:
            unsaved_tabs = []
            for index in self.modified_tabs:
                tab_text = self.tab_view.tabText(index)
                if tab_text.startswith('• '):
                    tab_text = tab_text[2:]  # Remove the dot for display
                unsaved_tabs.append(tab_text)
                
            # If there are unsaved changes, prompt the user
            if unsaved_tabs:
                if len(unsaved_tabs) == 1:
                    # Single file unsaved
                    reply = QMessageBox.question(
                        self,
                        "Unsaved Changes",
                        f"The file '{unsaved_tabs[0]}' has unsaved changes. Do you want to save before closing?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                    )
                    
                    if reply == QMessageBox.Save:
                        # Find the index in modified_tabs and save it
                        for index in self.modified_tabs:
                            self.tab_view.setCurrentIndex(index)
                            self.save_file()
                            break
                    elif reply == QMessageBox.Cancel:
                        event.ignore()
                        return
                else:
                    # Multiple files unsaved
                    message = "The following files have unsaved changes:\n\n"
                    for tab in unsaved_tabs:
                        message += f"• {tab}\n"
                    message += "\nDo you want to save them before closing?"
                    
                    reply = QMessageBox.question(
                        self,
                        "Unsaved Changes",
                        message,
                        QMessageBox.SaveAll | QMessageBox.Discard | QMessageBox.Cancel
                    )
                    
                    if reply == QMessageBox.SaveAll:
                        # Save all modified tabs
                        for index in sorted(self.modified_tabs):
                            self.tab_view.setCurrentIndex(index)
                            self.save_file()
                    elif reply == QMessageBox.Cancel:
                        event.ignore()
                        return
        
        # Save open files and current directory before closing
        self.save_open_files()
        self.save_last_directory()
        
        # Continue with the close event if not cancelled
        event.accept()

    # Add a method to handle bottom panel tab changes
    def handle_bottom_panel_tab_change(self, index):
        """Update the corner widget based on the active bottom panel tab"""
        # Remove any existing corner widgets
        self.bottom_panel.setCornerWidget(None)
        
        # Check which tab is active
        current_widget = self.bottom_panel.widget(index)
        
        if current_widget == self.output_widget:
            # If it's the output tab and we have a running process
            if hasattr(self, 'process_output') and self.process_output and self.process_output.state() == QProcess.Running:
                # Show the terminate button
                if hasattr(self, 'terminate_button'):
                    self.bottom_panel.setCornerWidget(self.terminate_button, Qt.TopRightCorner)
                    self.terminate_button.show()
            else:
                # Show the clear output button
                if not hasattr(self, 'clear_output_button') or self.clear_output_button is None:
                    self.clear_output_button = QPushButton("Clear Output")
                    self.clear_output_button.setStyleSheet('''
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            padding: 5px 10px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    ''')
                    self.clear_output_button.clicked.connect(self.clear_output)
                self.bottom_panel.setCornerWidget(self.clear_output_button, Qt.TopRightCorner)
                self.clear_output_button.show()

    def load_last_directory(self):
        """Load the last open directory from settings"""
        try:
            with open(self.settings_path, 'r') as f:
                settings = json.load(f)
                last_dir = settings.get('openMainFolder')
                if last_dir and os.path.exists(last_dir):
                    # If there's a valid saved directory, open it
                    self.model.setRootPath(last_dir)
                    self.tree_view.setRootIndex(self.model.index(last_dir))
                    self.tree_view.show()
                    self.open_folder_btn.hide()
                    self.statusBar().showMessage(f"Loaded last directory: {last_dir}")
                else:
                    # If no valid directory is saved, show Open Folder button
                    self.tree_view.hide()
                    self.open_folder_btn.show()
                    self.statusBar().showMessage("No directory loaded")
        except Exception as e:
            print(f"Error loading last directory: {e}")
            # If there's an error, show Open Folder button
            self.tree_view.hide()
            self.open_folder_btn.show()
            self.statusBar().showMessage("Error loading last directory")

    def save_last_directory(self):
        """Save the current directory to settings.json"""
        # Only save if we have a valid directory open
        if self.tree_view.isVisible():
            current_dir = self.model.filePath(self.tree_view.rootIndex())
            if current_dir:
                self.settingsJson['openMainFolder'] = current_dir
                with open(self.settings_path, 'w') as file:
                    json.dump(self.settingsJson, file, indent=2)

    def load_output_and_terminal_cache(self):
        # Load Output tab content
        if os.path.exists(self.output_cache_path):
            try:
                with open(self.output_cache_path, 'r', encoding='utf-8') as f:
                    self.output_widget.setPlainText(f.read())
            except Exception:
                pass
        # Load Terminal tab content
        if os.path.exists(self.terminal_cache_path):
            try:
                with open(self.terminal_cache_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.cmd_widget.setPlainText(content)
                    # Always show the shell prompt at the end
                    last_line = content.splitlines()[-1] if content.splitlines() else ''
                    prompt = f"{self.cmd_widget.current_directory}>" if self.cmd_widget.current_directory else ">"
                    if not last_line.strip().endswith(prompt):
                        self.cmd_widget.append(prompt)
            except Exception:
                pass

class ImageViewer(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)
        self.scale_factor = 1.0

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.pixmap)
        self.label.setBackgroundRole(QPalette.Base)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.label.setScaledContents(True)  # REMOVE THIS: do not auto-fit

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.label)
        self.scroll.setWidgetResizable(True)

        # Zoom controls
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setToolTip("Zoom In (Ctrl + Mouse Wheel Up, Ctrl + '+')")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setToolTip("Zoom Out (Ctrl + Mouse Wheel Down, Ctrl + '-')")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.reset_btn = QPushButton("⟳")
        self.reset_btn.setToolTip("Reset Zoom")
        self.reset_btn.clicked.connect(self.reset_zoom)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.zoom_in_btn)
        btn_layout.addWidget(self.zoom_out_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(btn_layout)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def zoom_in(self):
        self.set_scale(self.scale_factor * 1.25)

    def zoom_out(self):
        self.set_scale(self.scale_factor * 0.8)

    def reset_zoom(self):
        self.set_scale(1.0)

    def set_scale(self, scale):
        if self.pixmap.isNull():
            return
        self.scale_factor = max(0.05, min(scale, 20.0))
        size = self.pixmap.size() * self.scale_factor
        scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.resize(scaled_pixmap.size())

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() in (Qt.Key_Plus, Qt.Key_Equal):  # Ctrl + +
                self.zoom_in()
                event.accept()
                return
            elif event.key() == Qt.Key_Minus:  # Ctrl + -
                self.zoom_out()
                event.accept()
                return
        super().keyPressEvent(event)

class BioToolsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
                font-size:12px;
                outline:none;
                border:none;
            }
        ''')
        self.setMaximumWidth(400)
        self.setMinimumWidth(200)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add title
        title = QLabel("BioTools")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Add bioinformatics tools buttons
        global_alignment_btn = QPushButton("Global Sequence Alignment")
        local_alignment_btn = QPushButton("Local Sequence Alignment")
        
        # Style the buttons
        button_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        '''
        global_alignment_btn.setStyleSheet(button_style)
        local_alignment_btn.setStyleSheet(button_style)
        
        # Connect buttons to open alignment tabs
        global_alignment_btn.clicked.connect(lambda: self.open_alignment_tab("global"))
        local_alignment_btn.clicked.connect(lambda: self.open_alignment_tab("local"))
        
        layout.addWidget(global_alignment_btn)
        layout.addWidget(local_alignment_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def open_alignment_tab(self, alignment_type):
        # Get the main window instance
        main_window = self.window()
        if not isinstance(main_window, MainWindow):
            return
            
        # Create new alignment widget
        alignment_widget = SequenceAlignmentWidget(alignment_type)
        
        # Add new tab
        tab_name = f"{alignment_type.title()} Alignment"
        tab_index = main_window.tab_view.addTab(alignment_widget, tab_name)
        main_window.tab_view.setCurrentIndex(tab_index)

class GitPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
                font-size:12px;
                outline:none;
                border:none;
            }
            QTreeWidget {
                background-color: #21252b;
                border: none;
                color: #D3D3D3;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:hover {
                background-color: #2c313a;
            }
            QTreeWidget::item:selected {
                background-color: #373e4a;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: #D3D3D3;
            }
        ''')
        self.setMaximumWidth(400)
        self.setMinimumWidth(200)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add title
        title = QLabel("Source Control")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Repository info
        repo_info = QLabel("No repository selected")
        repo_info.setStyleSheet("color: #95a5a6;")
        layout.addWidget(repo_info)
        
        # Changes section
        changes_label = QLabel("Changes")
        changes_label.setStyleSheet("font-weight: bold; color: #D3D3D3;")
        layout.addWidget(changes_label)
        
        # Changes tree
        self.changes_tree = QTreeWidget()
        self.changes_tree.setHeaderLabels(["File", "Status"])
        self.changes_tree.setColumnWidth(0, 200)
        self.changes_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        layout.addWidget(self.changes_tree)
        
        # Staging area
        staging_label = QLabel("Staged Changes")
        staging_label.setStyleSheet("font-weight: bold; color: #D3D3D3;")
        layout.addWidget(staging_label)
        
        self.staging_tree = QTreeWidget()
        self.staging_tree.setHeaderLabels(["File", "Status"])
        self.staging_tree.setColumnWidth(0, 200)
        self.staging_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        layout.addWidget(self.staging_tree)
        
        # Commit message
        commit_label = QLabel("Commit Message")
        commit_label.setStyleSheet("font-weight: bold; color: #D3D3D3;")
        layout.addWidget(commit_label)
        
        self.commit_message = QTextEdit()
        self.commit_message.setPlaceholderText("Enter commit message...")
        self.commit_message.setMaximumHeight(100)
        layout.addWidget(self.commit_message)
        
        # Buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stage/Unstage buttons
        self.stage_button = QPushButton("Stage")
        self.stage_button.clicked.connect(self.stage_selected)
        self.unstage_button = QPushButton("Unstage")
        self.unstage_button.clicked.connect(self.unstage_selected)
        
        # Commit button
        self.commit_button = QPushButton("Commit")
        self.commit_button.clicked.connect(self.commit_changes)
        
        buttons_layout.addWidget(self.stage_button)
        buttons_layout.addWidget(self.unstage_button)
        buttons_layout.addWidget(self.commit_button)
        
        layout.addWidget(buttons_container)
        
        # Repository actions
        repo_actions = QWidget()
        repo_layout = QHBoxLayout(repo_actions)
        repo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.clone_button = QPushButton("Clone Repository")
        self.clone_button.clicked.connect(self.clone_repository)
        
        self.init_button = QPushButton("Initialize Repository")
        self.init_button.clicked.connect(self.init_repository)
        
        repo_layout.addWidget(self.clone_button)
        repo_layout.addWidget(self.init_button)
        
        layout.addWidget(repo_actions)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Initialize with some example changes
        self.update_changes_list()
    
    def update_changes_list(self):
        """Update the changes list with example files"""
        self.changes_tree.clear()
        
        # Example changes
        changes = [
            ("src/main.py", "Modified"),
            ("src/icons/new_icon.svg", "Added"),
            ("src/css/style.qss", "Modified"),
            ("README.md", "Deleted")
        ]
        
        for file, status in changes:
            item = QTreeWidgetItem([file, status])
            if status == "Modified":
                item.setForeground(1, QColor("#f1c40f"))  # Yellow for modified
            elif status == "Added":
                item.setForeground(1, QColor("#2ecc71"))  # Green for added
            elif status == "Deleted":
                item.setForeground(1, QColor("#e74c3c"))  # Red for deleted
            self.changes_tree.addTopLevelItem(item)
    
    def stage_selected(self):
        """Stage selected files"""
        selected_items = self.changes_tree.selectedItems()
        for item in selected_items:
            # Move item from changes to staging
            self.staging_tree.addTopLevelItem(self.changes_tree.takeTopLevelItem(
                self.changes_tree.indexOfTopLevelItem(item)))
    
    def unstage_selected(self):
        """Unstage selected files"""
        selected_items = self.staging_tree.selectedItems()
        for item in selected_items:
            # Move item from staging back to changes
            self.changes_tree.addTopLevelItem(self.staging_tree.takeTopLevelItem(
                self.staging_tree.indexOfTopLevelItem(item)))
    
    def commit_changes(self):
        """Commit staged changes"""
        if self.staging_tree.topLevelItemCount() == 0:
            QMessageBox.warning(self, "No Changes", "No changes staged for commit.")
            return
            
        commit_message = self.commit_message.toPlainText().strip()
        if not commit_message:
            QMessageBox.warning(self, "No Message", "Please enter a commit message.")
            return
            
        # Here you would implement the actual git commit
        QMessageBox.information(self, "Success", "Changes committed successfully!")
        self.staging_tree.clear()
        self.commit_message.clear()
    
    def clone_repository(self):
        """Clone a repository"""
        url, ok = QInputDialog.getText(self, "Clone Repository", 
                                     "Enter repository URL:")
        if ok and url:
            # Here you would implement the actual git clone
            QMessageBox.information(self, "Success", 
                                  f"Repository cloned successfully: {url}")
    
    def init_repository(self):
        """Initialize a new repository"""
        reply = QMessageBox.question(self, "Initialize Repository",
                                   "Initialize a new Git repository in the current directory?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Here you would implement the actual git init
            QMessageBox.information(self, "Success", 
                                  "Git repository initialized successfully!")

class CompactTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumHeight(60)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
            }
        """)

class SendButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Send")
        self.setFixedSize(60, 30)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)

class ChatArea(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
            }
        """)
        self.setMinimumHeight(300)
        
    def add_message(self, sender, message, is_user=False):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Format the message
        if is_user:
            # User message (right-aligned)
            cursor.insertHtml(f'<div style="text-align: right; margin: 10px 0;">'
                            f'<span style="color: #3498db;">{sender}</span> '
                            f'<span style="color: #95a5a6;">{timestamp}</span><br>'
                            f'<span style="background-color: #3498db; color: white; '
                            f'padding: 5px 10px; border-radius: 10px; display: inline-block;">'
                            f'{message}</span></div>')
        else:
            # Assistant message (left-aligned)
            cursor.insertHtml(f'<div style="text-align: left; margin: 10px 0;">'
                            f'<span style="color: #e74c3c;">{sender}</span> '
                            f'<span style="color: #95a5a6;">{timestamp}</span><br>'
                            f'<span style="background-color: #2d2d2d; color: white; '
                            f'padding: 5px 10px; border-radius: 10px; display: inline-block; '
                            f'border: 1px solid #3c3c3c;">{message}</span></div>')
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

class ApiWorker(QThread):
    response_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_url, data=None, params=None):
        super().__init__()
        self.api_url = api_url
        self.data = data
        self.params = params
        self.is_running = True
        
    def run(self):
        try:
            import requests
            if self.data:
                response = requests.post(self.api_url, json=self.data, params=self.params)
            else:
                response = requests.get(self.api_url, params=self.params)
            
            if response.status_code == 200:
                self.response_received.emit(response.json())
            else:
                error_msg = response.json().get('error', 'Unknown error occurred')
                self.error_occurred.emit(error_msg)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.is_running = False
    
    def stop(self):
        self.is_running = False
        self.wait()  # Wait for the thread to finish

class ChatbotPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_url = "http://192.168.1.12:6000"
        self.current_worker = None
        self.workers = []  # Keep track of all workers
        self.setup_ui()
    
    def cleanup_workers(self):
        """Clean up any running workers"""
        for worker in self.workers:
            if worker.isRunning():
                worker.stop()
        self.workers.clear()
    
    def create_worker(self, api_url, data=None, params=None):
        """Create and track a new worker"""
        worker = ApiWorker(api_url, data, params)
        self.workers.append(worker)
        return worker
    
    def closeEvent(self, event):
        """Handle cleanup when the panel is closed"""
        self.cleanup_workers()
        super().closeEvent(event)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        header.setFixedHeight(50)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Title with icon
        title_layout = QHBoxLayout()
        icon_label = QLabel("🤖")
        icon_label.setStyleSheet("font-size: 20px;")
        title_label = QLabel("AI Coding Assistant")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
            }
        """)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.setSpacing(10)
        
        # Add copy chat button
        copy_chat_btn = QPushButton("📋 Copy Chat")
        copy_chat_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        copy_chat_btn.clicked.connect(self.copy_entire_chat)
        header_layout.addLayout(title_layout)
        header_layout.addWidget(copy_chat_btn)
        
        layout.addWidget(header)
        
        # Chat container
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        # Chat area
        self.chat_area = ChatArea()
        chat_layout.addWidget(self.chat_area)
        
        # Add welcome message
        welcome_text = """
Welcome to the AI Coding Assistant! I can help you with:
- Code explanations and analysis
- Debugging assistance
- Algorithm design and optimization
- Best practices and patterns
- Code reviews and suggestions
- And much more!

Feel free to ask any coding questions!
"""
        self.chat_area.add_message("Assistant", welcome_text)
        
        # Input container
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-top: 1px solid #3c3c3c;
            }
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # Infinite progress
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1e1e1e;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 2px;
            }
        """)
        self.progress_bar.hide()
        input_layout.addWidget(self.progress_bar)
        
        # Message input and send button
        message_container = QWidget()
        message_layout = QHBoxLayout(message_container)
        message_layout.setContentsMargins(0, 5, 0, 0)
        message_layout.setSpacing(10)
        
        # Text input
        self.input_box = CompactTextEdit()
        self.input_box.setPlaceholderText("Ask a coding question...")
        self.input_box.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 18px;
                padding: 8px 15px;
                font-size: 14px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        message_layout.addWidget(self.input_box)
        
        # Send button
        self.send_button = SendButton()
        self.send_button.clicked.connect(self.send_message)
        message_layout.addWidget(self.send_button)
        
        input_layout.addWidget(message_container)
        
        # Help text
        help_text = QLabel("Press Shift+Enter for a new line, Enter to send")
        help_text.setStyleSheet("color: #95a5a6; font-size: 11px; margin-top: 5px;")
        help_text.setAlignment(Qt.AlignRight)
        input_layout.addWidget(help_text)
        
        chat_layout.addWidget(input_container)
        layout.addWidget(chat_container)
        
        # Connect signals
        self.input_box.installEventFilter(self)
        
        # Set size policy for responsiveness
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def copy_entire_chat(self):
        """Copy the entire chat history to clipboard"""
        chat_text = []
        # Get all message widgets from the container
        for i in range(self.chat_area.layout.count() - 1):  # -1 to exclude the stretch
            widget = self.chat_area.layout.itemAt(i).widget()
            if isinstance(widget, MessageWidget):
                # Get sender and content from the message widget
                sender = widget.findChild(QLabel).text()  # First label is the sender
                content = ""
                # Collect all text content from the message
                for child in widget.findChildren(QLabel):
                    if child != widget.findChild(QLabel):  # Skip the sender label
                        content += child.text() + "\n"
                chat_text.append(f"{sender}: {content.strip()}")
        
        # Join all messages with newlines
        full_chat = "\n\n".join(chat_text)
        clipboard = QApplication.clipboard()
        clipboard.setText(full_chat)
        QToolTip.showText(self.mapToGlobal(self.rect().center()), "Chat copied to clipboard!")
    
    def eventFilter(self, obj, event):
        if obj is self.input_box and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)
    
    def send_message(self):
        user_message = self.input_box.toPlainText().strip()
        if not user_message:
            return
        
        # Disable input while waiting for response
        self.input_box.setReadOnly(True)
        self.send_button.setEnabled(False)
        self.progress_bar.show()
        
        # Add user message to chat
        self.chat_area.add_message("You", user_message, is_user=True)
        
        # Clear the input box
        self.input_box.clear()
        
        # Create worker thread for API call
        self.current_worker = self.create_worker(
            f"{self.api_url}/chat",
            {"message": user_message}
        )
        self.current_worker.response_received.connect(self.handle_response)
        self.current_worker.error_occurred.connect(self.handle_error)
        self.current_worker.finished.connect(self.request_finished)
        self.current_worker.start()
    
    def handle_response(self, response_data):
        reply = response_data.get("response", "No response from server")
        self.chat_area.add_message("Assistant", reply)
    
    def handle_error(self, error_message):
        self.chat_area.add_message("System", f"⚠️ {error_message}")
    
    def request_finished(self):
        # Re-enable input after response
        self.input_box.setReadOnly(False)
        self.send_button.setEnabled(True)
        self.progress_bar.hide()
        self.input_box.setFocus()
        
        # Clean up worker
        if self.current_worker:
            self.current_worker.stop()
            self.workers.remove(self.current_worker)
            self.current_worker = None

class SequenceAlignmentWidget(QWidget):
    def __init__(self, alignment_type="global", parent=None):
        super().__init__(parent)
        self.alignment_type = alignment_type
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Set up monospace font
        monospace_font = QFont("Courier New", 12)
        
        # Title
        title = QLabel(f"{self.alignment_type.title()} Sequence Alignment")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Sequence 1 input
        seq1_label = QLabel("Sequence 1:")
        seq1_label.setStyleSheet("color: white;")
        self.seq1_input = QTextEdit()
        self.seq1_input.setFont(monospace_font)
        self.seq1_input.setPlaceholderText("Enter first sequence (e.g., ATGCATGC)")
        self.seq1_input.setMaximumHeight(100)
        self.seq1_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Courier New';
            }
        """)
        layout.addWidget(seq1_label)
        layout.addWidget(self.seq1_input)
        
        # Sequence 2 input
        seq2_label = QLabel("Sequence 2:")
        seq2_label.setStyleSheet("color: white;")
        self.seq2_input = QTextEdit()
        self.seq2_input.setFont(monospace_font)
        self.seq2_input.setPlaceholderText("Enter second sequence (e.g., ATGCTAGC)")
        self.seq2_input.setMaximumHeight(100)
        self.seq2_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Courier New';
            }
        """)
        layout.addWidget(seq2_label)
        layout.addWidget(self.seq2_input)
        
        # Run button
        self.run_button = QPushButton("Run Alignment")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.run_button.clicked.connect(self.run_alignment)
        layout.addWidget(self.run_button)
        
        # Results area
        results_label = QLabel("Alignment Results:")
        results_label.setStyleSheet("color: white;")
        self.results_area = QTextEdit()
        self.results_area.setFont(monospace_font)
        self.results_area.setReadOnly(True)
        self.results_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Courier New';
            }
        """)
        layout.addWidget(results_label)
        layout.addWidget(self.results_area)
        
        self.setLayout(layout)
    
    def contains_digit_underscore_or_dot(self, string):
        return any(c.isdigit() or c in ['_', '.'] for c in string)
    
    def retrieve_ncbi_sequence(self, accession_number):
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession_number}&rettype=fasta&retmode=text"
        response = requests.get(url)
        if response.status_code == 200:
            fasta_data = response.text
            fasta_io = StringIO(fasta_data)
            seq_record = next(SeqIO.parse(fasta_io, "fasta"))
            return str(seq_record.seq)
        else:
            raise Exception(f"Error fetching sequence for {accession_number}: {response.status_code}")
    
    def perform_global_alignment(self, seq1, seq2, gap_penalty=-2):
        len1 = len(seq1)
        len2 = len(seq2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(1, len1 + 1):
            matrix[i][0] = matrix[i-1][0] + gap_penalty
        for j in range(1, len2 + 1):
            matrix[0][j] = matrix[0][j-1] + gap_penalty

        match_score = 1
        mismatch_penalty = -1
        gap_open_penalty = -10
        gap_extend_penalty = -0.5

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                match = match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty
                diagonal_score = matrix[i-1][j-1] + match

                left_score = matrix[i][j-1] + (gap_extend_penalty if j > 1 and matrix[i][j-1] == matrix[i][j-2] + gap_extend_penalty else gap_open_penalty)
                up_score = matrix[i-1][j] + (gap_extend_penalty if i > 1 and matrix[i-1][j] == matrix[i-2][j] + gap_extend_penalty else gap_open_penalty)

                matrix[i][j] = max(diagonal_score, left_score, up_score)

        return self.traceback_global(seq1, seq2, matrix, gap_penalty)
    
    def traceback_global(self, seq1, seq2, matrix, gap_penalty):
        i = len(seq1)
        j = len(seq2)
        aligned_seq1 = ""
        aligned_seq2 = ""
        alignment_score = matrix[i][j]

        while i > 0 or j > 0:
            current_score = matrix[i][j]
            diagonal_score = matrix[i-1][j-1] if i > 0 and j > 0 else float('-inf')
            left_score = matrix[i][j-1] if j > 0 else float('-inf')
            up_score = matrix[i-1][j] if i > 0 else float('-inf')

            if i > 0 and j > 0 and current_score == diagonal_score + (1 if seq1[i-1] == seq2[j-1] else 0):
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                i -= 1
                j -= 1
            elif j > 0 and current_score == left_score + gap_penalty:
                aligned_seq1 = '-' + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                j -= 1
            else:
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = '-' + aligned_seq2
                i -= 1

        return aligned_seq1, aligned_seq2, alignment_score
    
    def smith_waterman(self, seq1, seq2, match_score=1, mismatch_penalty=-1, gap_penalty=-1):
        len1, len2 = len(seq1), len(seq2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        max_score = 0
        max_i, max_j = 0, 0

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                match = matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
                delete = matrix[i - 1][j] + gap_penalty
                insert = matrix[i][j - 1] + gap_penalty
                score = max(0, match, delete, insert)
                matrix[i][j] = score
                if score > max_score:
                    max_score = score
                    max_i, max_j = i, j

        aligned_seq1, aligned_seq2 = "", ""
        i, j = max_i, max_j
        while matrix[i][j] != 0:
            if seq1[i - 1] == seq2[j - 1] and matrix[i][j] == matrix[i - 1][j - 1] + match_score:
                aligned_seq1 = seq1[i - 1] + aligned_seq1
                aligned_seq2 = seq2[j - 1] + aligned_seq2
                i -= 1
                j -= 1
            elif matrix[i][j] == matrix[i - 1][j] + gap_penalty:
                aligned_seq1 = seq1[i - 1] + aligned_seq1
                aligned_seq2 = "-" + aligned_seq2
                i -= 1
            else:
                aligned_seq1 = "-" + aligned_seq1
                aligned_seq2 = seq2[j - 1] + aligned_seq2
                j -= 1

        return aligned_seq1, aligned_seq2, max_score
    
    def format_alignment_output(self, seq1, seq2, score, alignment_type):
        output = []
        line_length = 60
        
        if alignment_type == "global":
            output.append(f"GLOBAL ALIGNMENT SCORE: {score}\n")
        else:
            output.append(f"LOCAL ALIGNMENT SCORE: {score}\n")
        
        while seq1:
            substr_seq1 = seq1[:line_length]
            substr_seq2 = seq2[:line_length]
            alignment_line = ''.join('|' if substr_seq1[i] == substr_seq2[i] else ' ' for i in range(len(substr_seq1)))
            
            output.append(f"Sequence 1: {substr_seq1}")
            output.append(f"            {alignment_line}")
            output.append(f"Sequence 2: {substr_seq2}\n")
            
            seq1 = seq1[line_length:]
            seq2 = seq2[line_length:]
        
        return '\n'.join(output)
    
    def run_alignment(self):
        try:
            # Get sequences from input boxes
            seq1 = self.seq1_input.toPlainText().strip()
            seq2 = self.seq2_input.toPlainText().strip()
            
            if not seq1 or not seq2:
                self.results_area.setText("Please enter both sequences.")
                return
            
            # Handle NCBI accession numbers
            if self.contains_digit_underscore_or_dot(seq1):
                seq1 = self.retrieve_ncbi_sequence(seq1)
            if self.contains_digit_underscore_or_dot(seq2):
                seq2 = self.retrieve_ncbi_sequence(seq2)
            
            # Perform alignment based on type
            if self.alignment_type == "global":
                aligned_seq1, aligned_seq2, score = self.perform_global_alignment(seq1, seq2)
            else:  # local alignment
                aligned_seq1, aligned_seq2, score = self.smith_waterman(seq1, seq2)
            
            # Format and display results
            output = self.format_alignment_output(aligned_seq1, aligned_seq2, score, self.alignment_type)
            self.results_area.setText(output)
            
        except Exception as e:
            self.results_area.setText(f"Error: {str(e)}")

class MessageWidget(QFrame):
    """Widget for displaying a single message (user or assistant)"""
    def __init__(self, sender, content, is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setup_ui(sender, content)
        
    def setup_ui(self, sender, content):
        # Set frame style
        if self.is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #3498db;
                    border-radius: 10px;
                    padding: 0;
                    margin: 10px 0;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border-radius: 10px;
                    padding: 0;
                    margin: 10px 0;
                }
            """)
            
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)
        
        # Sender label with icon
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel()
        if self.is_user:
            icon_label.setText("👤")  # User icon
        else:
            icon_label.setText("🤖")  # Bot icon
        icon_label.setStyleSheet("font-size: 16px; margin-right: 5px;")
        header_layout.addWidget(icon_label)
        
        # Sender name
        sender_label = QLabel(sender)
        font = QFont()
        font.setBold(True)
        sender_label.setFont(font)
        sender_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        header_layout.addWidget(sender_label)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Process and add content
        self.process_content(content, main_layout)
    
    def process_content(self, content, layout):
        # Split content by code blocks
        parts = content.split("```")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Regular text
                if part.strip():
                    text_label = QLabel(part.strip())
                    text_label.setWordWrap(True)
                    text_label.setStyleSheet("color: #ffffff; font-size: 14px; line-height: 1.5;")
                    text_label.setTextFormat(Qt.RichText)
                    layout.addWidget(text_label)
            else:  # Code block
                if part.strip():
                    # Split language and code
                    lang_code = part.split("\n", 1)
                    language = lang_code[0].strip() if len(lang_code) > 1 else ""
                    code = lang_code[1] if len(lang_code) > 1 else part
                    
                    # Create code container
                    code_container = QFrame()
                    code_container.setStyleSheet("""
                        QFrame {
                            background-color: #1e1e1e;
                            border-radius: 5px;
                            padding: 10px;
                        }
                    """)
                    code_layout = QVBoxLayout(code_container)
                    code_layout.setContentsMargins(10, 10, 10, 10)
                    
                    # Add language label if specified
                    if language:
                        lang_label = QLabel(language)
                        lang_label.setStyleSheet("color: #95a5a6; font-size: 12px;")
                        code_layout.addWidget(lang_label)
                    
                    # Add code editor
                    code_editor = SyntaxHighlightedEditor(code.strip(), language)
                    code_layout.addWidget(code_editor)
                    
                    # Add copy button
                    copy_btn = CopyButton(code.strip())
                    copy_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            padding: 5px 10px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
                    code_layout.addWidget(copy_btn, alignment=Qt.AlignRight)
                    
                    layout.addWidget(code_container)

class SyntaxHighlightedEditor(QsciScintilla):
    """Editor widget with syntax highlighting for code blocks"""
    def __init__(self, code_content, language, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMarginWidth(0, 0)  # Hide line numbers
        self.setMarginWidth(1, 0)  # Hide folding margin
        self.setMarginWidth(2, 0)  # Hide any other margins
        
        # Set font
        font = QFont("Consolas", 12)
        self.setFont(font)
        
        # Set colors
        self.setPaper(QColor("#1e1e1e"))
        self.setCaretForegroundColor(QColor("#ffffff"))
        
        # Set lexer based on language
        if language.lower() in ["python", "py"]:
            lexer = QsciLexerPython(self)
        elif language.lower() in ["perl", "pl"]:
            lexer = QsciLexerPerl(self)
        
        lexer.setFont(font)
        lexer.setPaper(QColor("#1e1e1e"))
        lexer.setColor(QColor("#ffffff"))  # Default text color
        
        # Set lexer colors
        if isinstance(lexer, QsciLexerPython):
            lexer.setColor(QColor("#569cd6"), QsciLexerPython.Keyword)
            lexer.setColor(QColor("#ce9178"), QsciLexerPython.DoubleQuotedString)
            lexer.setColor(QColor("#ce9178"), QsciLexerPython.SingleQuotedString)
            lexer.setColor(QColor("#6a9955"), QsciLexerPython.Comment)
            lexer.setColor(QColor("#dcdcaa"), QsciLexerPython.FunctionMethodName)
        elif isinstance(lexer, QsciLexerPerl):
            lexer.setColor(QColor("#569cd6"), QsciLexerPerl.Keyword)
            lexer.setColor(QColor("#ce9178"), QsciLexerPerl.DoubleQuotedString)
            lexer.setColor(QColor("#ce9178"), QsciLexerPerl.SingleQuotedString)
            lexer.setColor(QColor("#6a9955"), QsciLexerPerl.Comment)
            
        self.setLexer(lexer)
        
        # Set the code content
        self.setText(code_content)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumHeight(100)
        self.setMaximumHeight(400)

class ChatArea(QScrollArea):
    """Scrollable area containing all messages"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #3c3c3c;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Container for messages
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignTop)
        
        # Add stretch at the end to keep messages at the top
        self.layout.addStretch()
        
        self.setWidget(self.container)
    
    def add_message(self, sender, content, is_user=False):
        # Remove stretch
        self.layout.removeItem(self.layout.itemAt(self.layout.count() - 1))
        
        # Add new message
        message_widget = MessageWidget(sender, content, is_user)
        self.layout.addWidget(message_widget)
        
        # Add stretch back
        self.layout.addStretch()
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
        return message_widget

class CompactTextEdit(QTextEdit):
    """Custom compact text edit for input more like a chatbot"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d9d9e3;
                border-radius: 18px;
                padding: 8px 15px;
                background-color: #ffffff;
                font-size: 14px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 1px solid #6e6e80;
            }
        """)
        # Set a smaller default size
        self.setMinimumHeight(40)
        self.setMaximumHeight(80)
        
    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(40)  # Default height more like a chat input
        return size

class SendButton(QPushButton):
    """Custom send button with animations"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Send")
        self.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 18px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)

class CopyButton(QPushButton):
    """Custom button for copying code content to clipboard"""
    def __init__(self, code_content, parent=None):
        super().__init__(parent)
        self.code_content = code_content
        self.setIcon(QIcon.fromTheme("edit-copy"))
        self.setToolTip("Copy to clipboard")
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                border-radius: 3px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e1e4e8;
            }
            QPushButton:pressed {
                background-color: #d1d5da;
            }
        """)
        self.clicked.connect(self.copy_to_clipboard)
        
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_content)
        # Show a brief tooltip to confirm copy
        QToolTip.showText(self.mapToGlobal(self.rect().bottomRight()), "Copied!")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())


