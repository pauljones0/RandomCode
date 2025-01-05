# NCURSES-DVD-Screensaver

A simple terminal-based DVD screensaver animation using NCURSES library. The program displays a "DVD" text that bounces around your terminal window, similar to the classic DVD player screensaver.

## Prerequisites

- GCC compiler
- NCURSES library
- Make

## Building

```bash
make
```

## Running

```bash
./demo
```

## Controls

- Press F1 to exit the program.

## Configuration

- The program is configurable via the following constants in the `demo.c` file:
  - `DELAY`: The delay between each frame in microseconds.
  - `MODX`: The horizontal speed modifier.
  - `MODY`: The vertical speed modifier.
  - `DVD_TEXT`: The text to display as the "DVD" logo.
  - `DVD_WIDTH`: The width of the "DVD" text.
