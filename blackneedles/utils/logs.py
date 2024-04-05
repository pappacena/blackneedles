from typing import List


def replace_repeated_lines(
    log: List[str],
    old_log: List[str],
) -> List[str]:
    """
    Returns only the new lines from the log, removing the repeated ones.

    A line is considered repeated if the line itself and the 5 lines before it
    are the same as the last 5 lines of the old log.
    """
    if not len(old_log):
        return log
    back_check = 5
    last_old_log_block = old_log[-back_check:]
    last_old_log_line = last_old_log_block[-1]
    for i, line in enumerate(log):
        if line != last_old_log_line:
            continue
        block = log[max(i - back_check + 1, 0) : i + 1]
        if block == last_old_log_block:
            return log[i + 1 :]
    return log
