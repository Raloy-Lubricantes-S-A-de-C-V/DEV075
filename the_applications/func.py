from itertools import count
from the_applications import conexion

# bd_apps = selecciona_basedatos.inicia_odoo()
def aqui_ando(n="1",t=""):
    print("**************************************************************")
    print("{} ACA ANDO : {}".format(n,t))
    print("**************************************************************")

def format_qty(d,t):
    d = str(d)
    if "." in d :
        sprte = d.split(".")
        rvrse = sprte[0][::-1]
        if len(sprte[1]) == 2:
            decimal = sprte[1]
        elif len(sprte[1]) == 1:
            decimal = "{}0".format(sprte[1])
        else:
            decimal = "00"
    else:
        rvrse = d[::-1]
    c = 1
    word = ''
    for r in rvrse:
        print(c,' - ', r)
        if c == 3:
            print(',')
            word = "{}{}{}".format(word, r, ',')
            c = 0
        else:
            word = "{}{}".format(word, r)
        c = c + 1

    if t == "float":
        word = "{}.{}".format(word.strip(',')[::-1], decimal)
    elif  t == "number":
        word = "{}".format(word.strip(',')[::-1])
    elif t == "money":
        word = "${}.{}".format(word.strip(',')[::-1], decimal)
    else:
        word = "{}".format(word.strip(',')[::-1])
    return word
