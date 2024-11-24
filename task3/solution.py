def appearance(intervals: dict[str, list[int]]) -> int:
    overlap, top = 0, intervals['lesson'][0]
    for pupil_start, pupil_end in zip(intervals['pupil'][::2], intervals['pupil'][1::2]):
        if pupil_start >= top: top = pupil_start
        if pupil_end >= top:
            for tutor_start, tutor_end in zip(intervals['tutor'][::2], intervals['tutor'][1::2]):
                if tutor_start < pupil_end and min(pupil_end, tutor_end) >= top:
                    overlap += min(pupil_end, tutor_end, intervals['lesson'][1]) - max(pupil_start, tutor_start, top)
                    top = min(pupil_end, tutor_end, intervals['lesson'][1])
    return overlap
