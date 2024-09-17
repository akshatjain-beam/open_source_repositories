def generate_dob_age() -> tuple:
    month = random.randint(1, 12)
    if month == 2:  # if month is feb
        day = random.randint(1, 28)
    elif month in [4, 6, 9, 11]:  # if month has 30 days
        day = random.randint(1, 30)
    elif month in [1, 3, 5, 7, 8, 10, 12]:  # if month has 31 days
        day = random.randint(1, 31)

    current_year = datetime.now().year
    year = random.randint(current_year - 80, current_year - 18)

    dob = datetime(day=day, month=month, year=year)
    age = (datetime.now() - dob).days // 365
    dob = dob.strftime("%d/%m/%Y")

    return dob, age