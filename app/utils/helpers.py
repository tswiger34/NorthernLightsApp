# Validates that the string is formatted correctly
def validate_string(value, var_name, logger):
    if not value or not isinstance(value, str):
        logger.error(f"{var_name} is invalid or missing.")
        raise ValueError(f"{var_name} must be a valid string. Instead received type {type(value)} and a value of {value}")
