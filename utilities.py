from datetime import date, timedelta

#  Generats todays date
today = date.today()


# Generats any date depending on what the amount of days backwards yuu pick using the timedelta(days backwards) function
def generat_date(days_backwards):
    generated_date = today - timedelta(int(days_backwards))
    return generated_date
