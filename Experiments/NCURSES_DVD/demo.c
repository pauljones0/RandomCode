#include <ncurses.h>
#include <unistd.h>
#include <stdbool.h>

// Constants for configuration
#define DELAY 500000
#define MODX 3
#define MODY 2
#define DVD_TEXT "DVD"
#define DVD_WIDTH 3  // Length of DVD_TEXT

typedef struct {
    int x;
    int y;
    int direction_x;
    int direction_y;
} DvdPosition;

void init_ncurses(void) {
    initscr();
    noecho();
    curs_set(FALSE);
    nodelay(stdscr, TRUE);
    keypad(stdscr, TRUE);
}

void update_position(DvdPosition *pos, int max_x, int max_y) {
    int next_x = pos->x + pos->direction_x;
    int next_y = pos->y + pos->direction_y;

    // Handle horizontal bounds
    if (next_x + DVD_WIDTH >= max_x) {
        pos->direction_x = -1 * MODX;
    } else if (next_x < 0) {
        pos->direction_x = 1 * MODX;
    }
    pos->x += pos->direction_x;

    // Handle vertical bounds
    if (next_y >= max_y) {
        pos->direction_y = -1 * MODY;
    } else if (next_y < 0) {
        pos->direction_y = 1 * MODY;
    }
    pos->y += pos->direction_y;
}

int main(int argc, char *argv[]) {
    int max_y = 0, max_x = 0;
    int ch;
    DvdPosition dvd = {
        .x = 0,
        .y = 0,
        .direction_x = 1 * MODX,
        .direction_y = 1 * MODY
    };

    init_ncurses();
    
    // Set initial position to center of screen
    dvd.x = COLS/2;
    dvd.y = LINES/2;

    while (true) {
        getmaxyx(stdscr, max_y, max_x);
        clear();

        mvprintw(dvd.y, dvd.x, DVD_TEXT);
        refresh();

        usleep(DELAY);

        update_position(&dvd, max_x, max_y);

        if ((ch = getch()) == KEY_F(1)) {
            break;
        }
    }

    endwin();
    return 0;
}