def generate_dob_age() -> tuple:
    """
    - Create a function `generate_dob_age` that generates a random date of birth in format of `date/month/year` and calculates the corresponding age.
    - the year should be between 18 to 80 years ago
    """
    current_year = datetime.now().year
    year = random.randint(current_year - 80, current_year - 18)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = f"{day}/{month}/{year}"
    age = current_year - year
    return dob, age