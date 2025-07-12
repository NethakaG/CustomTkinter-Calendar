import tkinter as tk
import customtkinter as ctk
from datetime import datetime, date, timedelta
import calendar
from typing import Optional, Callable

class CTkDatePicker(ctk.CTkFrame):
    """
    Modern, compact, and intuitive date picker widget for CustomTkinter.
    Features a redesigned calendar popup inspired by modern web UI.
    """
    def __init__(self,
                 master: any,
                 width: int = 200,
                 date_format: str = "%Y-%m-%d",
                 command: Optional[Callable] = None,
                 **kwargs):

        super().__init__(master, width=width, **kwargs)

        self.configure(fg_color="transparent")
        self._date_format = date_format
        self._command = command
        self._selected_date: Optional[date] = None
        self._calendar_window: Optional[ctk.CTkToplevel] = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._entry = ctk.CTkEntry(self, placeholder_text="")
        self._entry.grid(row=0, column=0, sticky="ew")
        self._entry.bind("<Button-1>", self._show_calendar)

        self._clear_button = ctk.CTkButton(
            self, text="✕", width=30, height=30,
            command=self._clear_date, fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )
        
        self.winfo_toplevel().bind("<Configure>", self._update_calendar_position, add="+")

    def _update_clear_button(self):
        """Show or hide the clear button based on whether a date is selected."""
        if self._selected_date:
            self._clear_button.grid(row=0, column=1, padx=(5,0))
        else:
            self._clear_button.grid_forget()

    def _clear_date(self):
        """Clears the selected date and updates the entry."""
        self.set(None)
        if self._command:
            self._command(None)

    def _update_calendar_position(self, event=None):
        """Ensure the calendar popup follows the main window."""
        if self._calendar_window and self._calendar_window.winfo_exists():
            x = self._entry.winfo_rootx()
            y = self._entry.winfo_rooty() + self._entry.winfo_height() + 2
            self._calendar_window.geometry(f"+{x}+{y}")

    def _show_calendar(self, event=None):
        """Create and display the calendar popup."""
        if self._calendar_window is not None:
            return

        self._calendar_window = ctk.CTkToplevel(self)
        self._calendar_window.wm_overrideredirect(True)
        self._update_calendar_position()

        calendar_widget = _CTkCalendarPopup(
            self._calendar_window,
            command=self._on_date_selected,
            selected_date=self._selected_date
        )
        calendar_widget.pack()
        
        self._calendar_window.grab_set()
        self._calendar_window.bind("<Escape>", self._hide_calendar)
        self.winfo_toplevel().bind("<ButtonPress>", self._check_click_outside, add="+")

    def _check_click_outside(self, event):
        """Close calendar if a click occurs outside of it."""
        if self._calendar_window:
            if not self._calendar_window.winfo_containing(event.x_root, event.y_root):
                self._hide_calendar()

    def _hide_calendar(self, event=None):
        """Destroy the calendar popup."""
        if self._calendar_window:
            self._calendar_window.grab_release()
            self._calendar_window.destroy()
            self._calendar_window = None
            self.winfo_toplevel().unbind("<ButtonPress>")

    def _on_date_selected(self, selected_date: date):
        """Handle date selection from the calendar."""
        self.set(selected_date)
        self._hide_calendar()
        if self._command:
            self._command(selected_date)

    def get(self) -> Optional[date]:
        """Returns the selected date as a datetime.date object, or None."""
        return self._selected_date

    def set(self, new_date: Optional[date]):
        """Sets the selected date. Accepts a datetime.date object or None to clear."""
        if new_date is not None and not isinstance(new_date, date):
            raise ValueError("new_date must be a datetime.date object or None")

        self._selected_date = new_date
        self._entry.delete(0, "end")
        if self._selected_date:
            self._entry.insert(0, self._selected_date.strftime(self._date_format))
        
        self._update_clear_button()


class _CTkCalendarPopup(ctk.CTkFrame):
    """Internal class for the compact, modern calendar view."""
    
    def __init__(self, master, command, selected_date: Optional[date] = None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=220, corner_radius=8)
        self._command = command
        self._selected_date = selected_date
        self._view_date = (selected_date or date.today()).replace(day=1)
        self._today = date.today()
        
        self._current_view = "days"

        self._create_widgets()
        self._update_view()

    def _create_widgets(self):
        self._header = ctk.CTkFrame(self, fg_color="transparent")
        self._header.pack(fill="x", padx=5, pady=5)
        self._header.grid_columnconfigure(1, weight=1)

        self._prev_button = ctk.CTkButton(self._header, text="<", width=30, command=self._prev)
        self._prev_button.grid(row=0, column=0)
        self._month_year_button = ctk.CTkButton(self._header, fg_color="transparent", hover=False, command=self._show_month_year_view)
        self._month_year_button.grid(row=0, column=1, sticky="ew")
        self._next_button = ctk.CTkButton(self._header, text=">", width=30, command=self._next)
        self._next_button.grid(row=0, column=2)

        self._view_container = ctk.CTkFrame(self, fg_color="transparent")
        self._view_container.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        self._day_frame = ctk.CTkFrame(self._view_container, fg_color="transparent")
        for i in range(7):
            self._day_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(self._day_frame, text=calendar.day_abbr[i][0]).grid(row=0, column=i)

        self._month_frame = ctk.CTkFrame(self._view_container, fg_color="transparent")
        for i in range(4):
            self._month_frame.grid_rowconfigure(i, weight=1)
            self._month_frame.grid_columnconfigure(i, weight=1)

        self._year_frame = ctk.CTkScrollableFrame(self._view_container, fg_color="transparent")

    def _update_view(self):
        if self._current_view == "days":
            self._month_year_button.configure(text=f"{calendar.month_name[self._view_date.month]} {self._view_date.year}")
            self._show_day_view()
        elif self._current_view == "months":
            self._month_year_button.configure(text=str(self._view_date.year), command=self._show_year_view)
            self._show_month_view()
        elif self._current_view == "years":
            start_year = self._view_date.year - 7
            end_year = self._view_date.year + 7
            self._month_year_button.configure(text=f"{start_year} - {end_year}", state="disabled")
            self._show_year_view()
    
    def _show_day_view(self):
        self._month_frame.pack_forget()
        self._year_frame.pack_forget()
        self._day_frame.pack(fill="both", expand=True)

        for widget in self._day_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        cal = calendar.Calendar()
        for r, week in enumerate(cal.monthdatescalendar(self._view_date.year, self._view_date.month), start=1):
            for c, day_date in enumerate(week):
                btn = ctk.CTkButton(
                    self._day_frame, text=str(day_date.day), width=30, height=30,
                    corner_radius=15, command=lambda d=day_date: self._command(d)
                )
                
                in_month = day_date.month == self._view_date.month
                fg = ctk.ThemeManager.theme["CTkButton"]["fg_color"] if day_date == self._selected_date else "transparent"
                text_color = "white" if day_date == self._selected_date else "gray50" if not in_month else ctk.ThemeManager.theme["CTkLabel"]["text_color"]
                border_width = 1 if day_date == self._today else 0
                
                btn.configure(fg_color=fg, text_color=text_color, border_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], border_width=border_width)
                btn.grid(row=r, column=c, padx=1, pady=1)

    def _show_month_view(self):
        self._day_frame.pack_forget()
        self._year_frame.pack_forget()
        self._month_frame.pack(fill="both", expand=True)

        for widget in self._month_frame.winfo_children():
            widget.destroy()
        
        for i, month in enumerate(calendar.month_abbr[1:]):
            btn = ctk.CTkButton(self._month_frame, text=month, command=lambda m=i+1: self._select_month(m))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")

    def _show_year_view(self):
        self._day_frame.pack_forget()
        self._month_frame.pack_forget()
        self._year_frame.pack(fill="both", expand=True)

        for widget in self._year_frame.winfo_children():
            widget.destroy()
        
        start_year = self._view_date.year - 100
        end_year = self._view_date.year + 100
        year_range = list(range(start_year, end_year + 1))
        
        for i, year in enumerate(year_range):
            btn = ctk.CTkButton(self._year_frame, text=str(year), command=lambda y=year: self._select_year(y))
            btn.pack(fill="x", padx=5, pady=2)
        
        try:
            target_index = year_range.index(self._view_date.year)
            total_items = len(year_range)
            fraction = target_index / total_items if total_items > 0 else 0
            
            self._year_frame.after(50, lambda: self._year_frame._parent_canvas.yview_moveto(fraction))
        except ValueError:
            pass

    def _show_month_year_view(self):
        self._current_view = "months" if self._current_view == "days" else "years"
        self._update_view()

    def _select_month(self, month):
        self._view_date = self._view_date.replace(month=month)
        self._current_view = "days"
        self._month_year_button.configure(command=self._show_month_year_view)
        self._update_view()

    def _select_year(self, year):
        self._view_date = self._view_date.replace(year=year)
        self._current_view = "months"
        self._month_year_button.configure(state="normal")
        self._update_view()

    def _prev(self):
        if self._current_view == "days":
            self._view_date = (self._view_date - timedelta(days=1)).replace(day=1)
        elif self._current_view == "months":
            self._view_date = self._view_date.replace(year=self._view_date.year - 1)
        self._update_view()

    def _next(self):
        if self._current_view == "days":
            self._view_date = (self._view_date + timedelta(days=32)).replace(day=1)
        elif self._current_view == "months":
            self._view_date = self._view_date.replace(year=self._view_date.year + 1)
        self._update_view()


if __name__ == "__main__":
    
    ctk.set_appearance_mode("system")
    root = ctk.CTk()
    root.title("Modern CTkDatePicker")
    root.geometry("400x200")
    root.grid_columnconfigure(0, weight=1)

    def print_date(selected_date):
        print("Selected Date:", selected_date)

    label = ctk.CTkLabel(root, text="Select a Date", font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(pady=20)

    date_picker = CTkDatePicker(root, command=print_date, date_format="%B %d, %Y")
    date_picker.pack(padx=20, fill="x")

    root.mainloop()
