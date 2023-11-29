def convert_duration_to_minutes(duration_str):
    """
    Convert the input duration string to the corresponding\
        duration in minutes asynchronously.

    Args:
        duration_str (str): A string representing the duration in\
            the format 'Xm', 'Xh', or 'Xd', where 'X' is an integer
        value and 'm', 'h', and 'd' represent minutes, hours,\
            and days, respectively.

    Returns:
        int: The total duration in minutes calculated\
            from the input duration string.

    Raises:
        ValueError: If the input duration format is invalid or the duration\
            value is not a valid integer.

    Example Usage:
        Input: '60m'
        Output: 60

        Input: '2h'
        Output: 120

        Input: '1d'
        Output: 1440
    """
    duration_mapping = {
        "m": 1,
        "h": 60,
        "d": 1440,
    }  # Mapping of time units to minutes
    unit = duration_str[-1]  # Extract the time unit from the duration string
    if unit not in duration_mapping:
        raise ValueError(
            "Invalid duration format. Valid formats include 'm' for minutes,\
                'h' for hours, and 'd' for days."
        )

    try:
        duration = (
            int(duration_str[:-1]) * duration_mapping[unit]
        )  # Calculate the total duration in minutes
    except ValueError:
        raise ValueError(
            "Invalid duration value. Please provide a valid integer\
                for the duration."
        )

    return int(
        duration
    )  # Ensure that the duration is returned as an integer value
