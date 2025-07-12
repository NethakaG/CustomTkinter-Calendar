# CTkCalendar - Modern Date Picker for CustomTkinter

A modern, compact, and intuitive date picker widget for CustomTkinter applications. This unofficial extension provides a sleek calendar dropdown that integrates seamlessly with your CTk apps.

## Features

- **Modern Design**: Clean, minimalist interface that matches CustomTkinter's aesthetic
- **Compact Calendar View**: Space-efficient popup calendar with intuitive navigation
- **Multi-View Navigation**: Switch between day, month, and year views
- **Flexible Date Formatting**: Customize how dates are displayed
- **Easy Integration**: Drop-in replacement for basic date input needs
- **Keyboard Support**: ESC key to close, click outside to dismiss
- **Clear Functionality**: Built-in clear button for easy date removal

## Installation

Simply download `CTkCalendar.py` and place it in your project directory.

**Requirements:**
- Python 3.6+
- CustomTkinter
- tkinter (usually included with Python)

## Quick Start

```python
import customtkinter as ctk
from CTkCalendar import CTkDatePicker

# Create your CTk app
app = ctk.CTk()
app.geometry("400x300")

# Callback function for date selection
def on_date_selected(selected_date):
    print(f"Selected: {selected_date}")

# Create the date picker
date_picker = CTkDatePicker(
    app,
    command=on_date_selected,
    date_format="%Y-%m-%d"
)
date_picker.pack(pady=20, padx=20, fill="x")

app.mainloop()
```

## Usage

### Basic Usage

```python
# Simple date picker
date_picker = CTkDatePicker(parent_frame)

# Get the selected date
selected_date = date_picker.get()  # Returns datetime.date object or None

# Set a date programmatically
from datetime import date
date_picker.set(date(2024, 12, 25))

# Clear the selection
date_picker.set(None)
```

### Parameters

- `master`: Parent widget
- `width`: Widget width (default: 200)
- `date_format`: Date display format (default: "%Y-%m-%d")
- `command`: Callback function called when date is selected
- `**kwargs`: Additional CustomTkinter frame parameters

### Date Formats

Common date format examples:
- `"%Y-%m-%d"` → 2024-03-15
- `"%B %d, %Y"` → March 15, 2024
- `"%d/%m/%Y"` → 15/03/2024
- `"%m-%d-%Y"` → 03-15-2024

## Why I Built This

CustomTkinter is an excellent modern UI library for Python, but it doesn't include a built-in date picker widget. I needed one for my projects and wanted something that:

- Matches CTk's modern aesthetic
- Is lightweight and easy to integrate
- Provides intuitive navigation (day/month/year views)
- Works seamlessly with existing CTk applications

## Screenshots

*The calendar features a clean, modern design with:*
- Compact popup that doesn't overwhelm your UI
- Clear visual indicators for today's date and selected date
- Smooth navigation between different time periods
- Responsive hover effects and modern button styling

## Contributing

This is currently a personal project for my portfolio. While I'm not accepting contributions at the moment, feel free to fork and modify for your own needs!

## License

This project is provided as-is for educational and personal use. It's an unofficial extension for CustomTkinter.

## Acknowledgments

- Built for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
- Inspired by modern web date picker interfaces

--------------------------------------

*This is an unofficial third-party widget and is not affiliated with the CustomTkinter project.*
