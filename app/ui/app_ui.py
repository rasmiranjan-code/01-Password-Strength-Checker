"""
Main application UI.

This module creates the main graphical user interface for the
Password Strength Checker using the customtkinter library.
"""

from __future__ import annotations

import random
import string

import customtkinter as ctk

from app.config import Settings
from app.core import PasswordAnalyzer
from app.models import PasswordAnalysisResult
from app.utils.logger import get_logger


logger = get_logger(__name__)

# --- Professional Dark "Hacker" Theme ---
BG_COLOR = "#0D1117"          # GitHub-dark style near-black background
CARD_COLOR = "#161B22"        # Slightly lighter panel color
BORDER_COLOR = "#30363D"      # Subtle border
ACCENT_GREEN = "#39FF14"      # Neon green (primary accent)
ACCENT_GREEN_DIM = "#1F8B2C"  # Dimmer green for secondary elements
ACCENT_RED = "#FF073A"        # Neon red (danger)
ACCENT_ORANGE = "#FFA500"     # Warning
TEXT_MUTED = "#8B949E"        # Muted grey-blue text (not flat grey)

FONT_FAMILY = "Consolas"
FONT_SM = (FONT_FAMILY, 12)
FONT_MD = (FONT_FAMILY, 14)
FONT_MD_BOLD = (FONT_FAMILY, 14, "bold")
FONT_LG_BOLD = (FONT_FAMILY, 16, "bold")
FONT_TITLE = (FONT_FAMILY, 26, "bold")

MATRIX_CHARS = string.ascii_uppercase + string.digits + "@#$%&*+=<>/\\|"


class MatrixRain(ctk.CTkCanvas):
    """A Canvas widget that renders an animated 'Matrix digital rain' effect."""

    def __init__(self, master, width: int, height: int, font_size: int = 14, **kwargs) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg=BG_COLOR,
            highlightthickness=0,
            **kwargs,
        )
        self.width = width
        self.height = height
        self.font_size = font_size
        self.col_width = font_size
        self.num_columns = max(1, width // self.col_width)

        # Each column tracks the y-position (in rows) of the head of its stream
        self.drops = [random.randint(-20, 0) for _ in range(self.num_columns)]
        # Track trailing character ids per column for cleanup
        self._column_ids: list[list[int]] = [[] for _ in range(self.num_columns)]

        self._running = True
        self._animate()

    def stop(self) -> None:
        self._running = False

    def _random_char(self) -> str:
        return random.choice(MATRIX_CHARS)

    def _animate(self) -> None:
        if not self._running:
            return

        for col in range(self.num_columns):
            x = col * self.col_width
            row = self.drops[col]
            y = row * self.font_size

            if 0 <= y < self.height:
                char = self._random_char()
                # Bright leading character
                cid = self.create_text(
                    x, y, text=char, fill=ACCENT_GREEN,
                    font=(FONT_FAMILY, self.font_size, "bold"), anchor="nw",
                )
                self._column_ids[col].append(cid)

                # Fade older characters in this column into dim green, then remove
                ids = self._column_ids[col]
                if len(ids) > 18:
                    old_id = ids.pop(0)
                    self.delete(old_id)
                # Dim the second-to-last character to simulate a trail
                if len(ids) >= 2:
                    self.itemconfig(ids[-2], fill=ACCENT_GREEN_DIM)

            # Reset the drop to the top randomly once it passes the bottom
            if y > self.height and random.random() > 0.975:
                self.drops[col] = random.randint(-20, 0)
                for cid in self._column_ids[col]:
                    self.delete(cid)
                self._column_ids[col] = []
            else:
                self.drops[col] += 1

        self.after(60, self._animate)


class AppUI(ctk.CTk):
    """
    Main application window.
    """

    def __init__(self) -> None:
        super().__init__()
        self.analyzer = PasswordAnalyzer()
        self._setup_window()
        self._create_widgets()
        self._animate_title()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        logger.info("AppUI initialized successfully.")

    def _on_close(self) -> None:
        """Stop background animation and close the window cleanly."""
        self.matrix_bg.stop()
        self.destroy()

    def _setup_window(self) -> None:
        """Configure the main application window."""
        self.title(Settings.APP_NAME)
        self.geometry("520x680")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.configure(fg_color=BG_COLOR)

        # --- Animated Matrix-style hacker background ---
        self.matrix_bg = MatrixRain(self, width=520, height=680, font_size=14)
        self.matrix_bg.place(x=0, y=0, relwidth=1, relheight=1)

    def _create_widgets(self) -> None:
        """Create and arrange all UI widgets."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=24, pady=24, fill="both", expand=True)

        # --- Title ---
        self.title_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=FONT_TITLE,
            text_color=ACCENT_GREEN,
        )
        self.title_label.pack(pady=(0, 22))

        # --- Password Input Card ---
        input_card = ctk.CTkFrame(
            main_frame, fg_color=CARD_COLOR, corner_radius=10,
            border_width=1, border_color=BORDER_COLOR,
        )
        input_card.pack(fill="x", pady=(0, 16))

        entry_label = ctk.CTkLabel(
            input_card, text="PASSWORD", font=FONT_SM,
            text_color=TEXT_MUTED, anchor="w",
        )
        entry_label.pack(fill="x", padx=16, pady=(14, 4))

        self.password_entry = ctk.CTkEntry(
            input_card,
            placeholder_text="Type a password to analyze...",
            border_color=ACCENT_GREEN_DIM,
            fg_color="#0D1117",
            text_color=ACCENT_GREEN,
            font=FONT_MD,
            height=38,
            corner_radius=8,
            show="*",
        )
        self.password_entry.pack(fill="x", padx=16, pady=(0, 16))
        self.password_entry.bind("<KeyRelease>", self._on_password_change)

        # --- Strength Card ---
        strength_card = ctk.CTkFrame(
            main_frame, fg_color=CARD_COLOR, corner_radius=10,
            border_width=1, border_color=BORDER_COLOR,
        )
        strength_card.pack(fill="x", pady=(0, 16))

        self.strength_label = ctk.CTkLabel(
            strength_card, text="Strength: —", font=FONT_MD_BOLD,
            text_color=ACCENT_GREEN, anchor="w",
        )
        self.strength_label.pack(fill="x", padx=16, pady=(14, 8))

        self.strength_bar = ctk.CTkProgressBar(
            strength_card, height=10, corner_radius=6,
            progress_color=ACCENT_GREEN, fg_color="#0D1117",
        )
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x", padx=16, pady=(0, 16))

        # --- Analysis Details Card ---
        details_card = ctk.CTkFrame(
            main_frame, fg_color=CARD_COLOR, corner_radius=10,
            border_width=1, border_color=BORDER_COLOR,
        )
        details_card.pack(fill="x", pady=(0, 16))

        details_title = ctk.CTkLabel(
            details_card, text="ANALYSIS", font=FONT_SM,
            text_color=TEXT_MUTED, anchor="w",
        )
        details_title.pack(fill="x", padx=16, pady=(14, 6))

        self.score_label = self._make_detail_row(details_card, "Score:", "0/100")
        self.entropy_label = self._make_detail_row(details_card, "Entropy:", "0.0 bits")
        self.crack_time_label = self._make_detail_row(details_card, "Est. Crack Time:", "—")
        self.pwned_label = self._make_detail_row(details_card, "Breach Check:", "—", pad_bottom=16)

        # --- Recommendations Card ---
        rec_card = ctk.CTkFrame(
            main_frame, fg_color=CARD_COLOR, corner_radius=10,
            border_width=1, border_color=BORDER_COLOR,
        )
        rec_card.pack(fill="both", expand=True)

        recommendations_title = ctk.CTkLabel(
            rec_card, text=">> RECOMMENDATIONS", font=FONT_LG_BOLD,
            text_color=ACCENT_GREEN, anchor="w",
        )
        recommendations_title.pack(fill="x", padx=16, pady=(14, 8))

        self.recommendations_frame = ctk.CTkFrame(rec_card, fg_color="transparent")
        self.recommendations_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self._reset_ui()

    def _make_detail_row(self, parent, label_text: str, value_text: str, pad_bottom: int = 4) -> ctk.CTkLabel:
        """Create a label:value row and return the value label for later updates."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, pad_bottom))

        ctk.CTkLabel(
            row, text=label_text, font=FONT_MD, text_color=TEXT_MUTED, width=140, anchor="w",
        ).pack(side="left")

        value_label = ctk.CTkLabel(
            row, text=value_text, font=FONT_MD_BOLD, text_color=ACCENT_GREEN, anchor="w",
        )
        value_label.pack(side="left", fill="x", expand=True)
        return value_label

    def _animate_title(self, index=0) -> None:
        """Animate the title with a typing effect."""
        full_text = Settings.APP_NAME
        if index < len(full_text):
            self.title_label.configure(text=self.title_label.cget("text") + full_text[index])
            self.after(100, self._animate_title, index + 1)
        else:
            self.title_label.configure(text=full_text + "_")

    def _on_password_change(self, event=None) -> None:
        """Callback triggered when the password input changes."""
        password = self.password_entry.get()
        if not password:
            self._reset_ui()
            return

        result = self.analyzer.analyze(password)
        self._update_ui(result)

    def _update_ui(self, result: PasswordAnalysisResult) -> None:
        """Update the UI with the analysis results."""
        score_percent = result.score / 100
        self.strength_bar.set(score_percent)
        self.strength_label.configure(text=f"Strength: {result.strength}")

        if result.score >= Settings.SCORE_STRONG:
            bar_color = ACCENT_GREEN
        elif result.score >= Settings.SCORE_MEDIUM:
            bar_color = ACCENT_ORANGE
        else:
            bar_color = ACCENT_RED

        self.strength_bar.configure(progress_color=bar_color)
        self.strength_label.configure(text_color=bar_color)

        self.score_label.configure(text=f"{result.score}/100", text_color=bar_color)
        self.entropy_label.configure(text=f"{result.entropy} bits ({result.entropy_level})")

        self.crack_time_label.configure(text=result.estimated_crack_time)

        if result.pwned_count > 0:
            pwned_text = f"Found in {result.pwned_count:,} breaches!"
            pwned_color = ACCENT_RED
        else:
            pwned_text = "Not found in any known breaches."
            pwned_color = ACCENT_GREEN
        self.pwned_label.configure(text=pwned_text, text_color=pwned_color)

        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        if result.recommendations:
            for tip in result.recommendations:
                rec_label = ctk.CTkLabel(
                    self.recommendations_frame,
                    text=f"• {tip}",
                    font=FONT_MD,
                    text_color=ACCENT_GREEN,
                    wraplength=430,
                    justify="left",
                    anchor="w",
                )
                rec_label.pack(anchor="w", pady=3, fill="x")
        else:
            rec_label = ctk.CTkLabel(
                self.recommendations_frame,
                text="Looks solid — no recommendations.",
                font=(FONT_FAMILY, 12, "italic"),
                text_color=TEXT_MUTED,
                anchor="w",
            )
            rec_label.pack(anchor="w", pady=3, fill="x")

    def _reset_ui(self) -> None:
        """Reset the UI to its initial state."""
        self.strength_bar.set(0)
        self.strength_bar.configure(progress_color=ACCENT_GREEN)
        self.strength_label.configure(text="Strength: —", text_color=ACCENT_GREEN)
        self.score_label.configure(text="0/100", text_color=ACCENT_GREEN)
        self.entropy_label.configure(text="0.0 bits", text_color=ACCENT_GREEN)
        self.crack_time_label.configure(text="—", text_color=ACCENT_GREEN)
        self.pwned_label.configure(text="—", text_color=ACCENT_GREEN)

        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        initial_label = ctk.CTkLabel(
            self.recommendations_frame,
            text="Enter a password above to see live analysis.",
            font=(FONT_FAMILY, 12, "italic"),
            text_color=TEXT_MUTED,
            anchor="w",
        )
        initial_label.pack(anchor="w", pady=3, fill="x")