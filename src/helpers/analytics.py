class AnalyticsResult:
    def __init__(self, process_time, depres_per_second):
        self.process_time = process_time
        self.depres_per_second = depres_per_second


def format_process_time(process_time):
    seconds = int(process_time)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def calc_depres_analyzed_per_sec(process_time, count_depres_analyzed):
    seconds = int(process_time)

    return int(count_depres_analyzed / seconds)


def calc_analytics(start_time, end_time, count_depres_analyzed):
    process_time = end_time - start_time
    formated_process_time = format_process_time(process_time)
    depres_per_second = calc_depres_analyzed_per_sec(
        process_time, count_depres_analyzed
    )

    return AnalyticsResult(formated_process_time, depres_per_second)
