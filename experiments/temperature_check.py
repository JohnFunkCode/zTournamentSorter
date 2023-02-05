#to test ChatGPT's ability to create unit tests
def temperature_check(temp):
    if temp > 80:
        return "it's hot"
    elif temp < 40:
        return "it's cold"
    else:
        return "it's mild"
