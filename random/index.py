from random import randint


def blum_blum_shub(n, m):
    """
    Generates a random number between 0 and n-1
    """
    a = randint(0, n-1)
    b = randint(0, n-1)
    while a == 0:
        a = randint(0, n-1)
    while b == 0:
        b = randint(0, n-1)
    return (a**b) % n   # modulo n

# FIPS 140-2 test blum blum shub


def test_blum_blum_shub(n, m):
    """
    Tests the blum blum shub function
    """
    for i in range(0, m):
        a = blum_blum_shub(n, m)
        if a < 0 or a >= n:
            print("Error: a = %d" % a)
            return False
    return True


print(test_blum_blum_shub(2**16, 100))

def difference_in_days_between_two_dates(date1, date2):
    """
    Returns the difference in days between two dates
    """
    return (date2 - date1).days # timedelta


