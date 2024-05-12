#!/usr/bin/python3
"""Función Main"""
from src.engine.game_engine import GameEngine

start_scene = "main_menu"

if __name__ == "__main__":
    engine = GameEngine()
    engine.run(start_scene=start_scene)
