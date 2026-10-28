"""Module de lecture audio pour l'ecoute directe et le mini-lecteur."""

import os
from pathlib import Path
import threading
import time
from typing import Optional

# Configuration pygame pour masquer le bandeau d'accueil
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


def play_audio_direct(audio_path: Path) -> None:
    """Joue un fichier audio de maniere synchrone en console."""
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(str(audio_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
    finally:
        pygame.mixer.quit()


def launch_mini_player(
    audio_path: Path, 
    title: str = "Lecteur vocal", 
    subtitle: str = "Synthese en cours"
) -> None:
    """Affiche une mini-fenetre Windows legere pour le controle de lecture contextuelle."""
    import tkinter as tk
    from tkinter import ttk

    pygame.mixer.init()
    pygame.mixer.music.load(str(audio_path))

    root = tk.Tk()
    root.title(title)
    root.geometry("380x190")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    is_playing = [True]

    header_label = ttk.Label(
        root, 
        text=title, 
        font=("Segoe UI", 11, "bold"), 
        wraplength=340
    )
    header_label.pack(pady=(12, 4), padx=16)

    sub_label = ttk.Label(
        root, 
        text=subtitle, 
        font=("Segoe UI", 9), 
        foreground="#555555",
        wraplength=340
    )
    sub_label.pack(pady=(0, 12), padx=16)

    status_var = tk.StringVar(value="Lecture en cours...")
    status_label = ttk.Label(
        root, 
        textvariable=status_var, 
        font=("Segoe UI", 9, "italic")
    )
    status_label.pack(pady=(0, 10))

    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=4)

    def toggle_play():
        if is_playing[0]:
            pygame.mixer.music.pause()
            is_playing[0] = False
            status_var.set("En pause")
            play_btn.config(text="Reprendre")
        else:
            pygame.mixer.music.unpause()
            is_playing[0] = True
            status_var.set("Lecture en cours...")
            play_btn.config(text="Pause")

    def restart_play():
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
        is_playing[0] = True
        status_var.set("Lecture en cours...")
        play_btn.config(text="Pause")

    def on_close():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        root.destroy()

    play_btn = ttk.Button(btn_frame, text="Pause", command=toggle_play, width=12)
    play_btn.grid(row=0, column=0, padx=6)

    restart_btn = ttk.Button(btn_frame, text="Recommencer", command=restart_play, width=12)
    restart_btn.grid(row=0, column=1, padx=6)

    close_btn = ttk.Button(btn_frame, text="Fermer", command=on_close, width=10)
    close_btn.grid(row=0, column=2, padx=6)

    # Demarrage de la lecture
    pygame.mixer.music.play()

    # Raccourci barre d'espace pour basculer Pause / Lecture (conforme EXPERIENCE.md)
    root.bind("<space>", lambda event: toggle_play())
    root.bind("<Escape>", lambda event: on_close())

    def check_playback():
        if is_playing[0] and not pygame.mixer.music.get_busy():
            status_var.set("Lecture terminee")
            play_btn.config(state="disabled")
        else:
            root.after(300, check_playback)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.after(300, check_playback)
    root.mainloop()
