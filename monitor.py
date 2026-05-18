import psutil
import curses
import time

def draw_bar(window, y, x, label, value, width=30):
    percent = min(value, 100)
    fill = int((percent / 100) * width)

    if percent < 50:
        color = curses.color_pair(2)  # green
    elif percent < 80:
        color = curses.color_pair(3)  # yellow
    else:
        color = curses.color_pair(4)  # red

    bar = "[" + ("#" * fill).ljust(width) + "]"

    window.addstr(y, x, f"{label}: ")
    window.addstr(bar, color)
    window.addstr(f" {percent:.1f}%")


def draw_monitor(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    # colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    prev_net = psutil.net_io_counters()

    while True:
        stdscr.clear()

        # CPU & RAM
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent

        stdscr.addstr(1, 2, "🔥 LIVE SYSTEM MONITOR", curses.color_pair(1))

        draw_bar(stdscr, 3, 2, "CPU", cpu)
        draw_bar(stdscr, 5, 2, "RAM", ram)

        # Network
        net = psutil.net_io_counters()
        sent = (net.bytes_sent - prev_net.bytes_sent) / 1024 / 1024
        recv = (net.bytes_recv - prev_net.bytes_recv) / 1024 / 1024
        prev_net = net

        stdscr.addstr(7, 2, f"NET Sent: {sent:.2f} MB | Recv: {recv:.2f} MB")

        stdscr.addstr(9, 2, "Press CTRL+C to exit")

        stdscr.refresh()
        time.sleep(0.5)


if __name__ == "__main__":
    curses.wrapper(draw_monitor)