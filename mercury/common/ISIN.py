import string

# from https://github.com/mmcloughlin/luhn
def luhn_checksum(numeric_string):
    """
    Compute the Luhn checksum for the provided string of digits. Note this
    assumes the check digit is in place.
    """
    digits = list(map(int, numeric_string))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10

class ISIN(str):
    def check(self):
        """
        Check if the provided string is a valid ISIN.
        """
        if len(self) != 12:
            return False

        numeric_isin = ''
        numeric_isin += string.ascii_letters.index(self[0])%26 + 10
        numeric_isin += string.ascii_letters.index(self[1])%26 + 10
        numeric_isin += self[2:]

        return (luhn_checksum(numeric_isin) == 0)
