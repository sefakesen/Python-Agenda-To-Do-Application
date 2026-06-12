import re

def tarih_dogrula(tarih_metni):
    """
    Kullanıcının girdiği tarihin GG/AA/YYYY formatında olup olmadığını Regex ile kontrol eder.
    """
    desen = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
    if re.match(desen, tarih_metni):
        return True
    return False