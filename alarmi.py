from posljiMail import posljiemail

prejemniki = ['furbek.celarc@gmail.com', 'rom.celarc@gmail.com']
meja1 = 40
meja2 = 36
poslano1 = False
poslano2 = False

def preveriMrzloVodo(t1):
    global poslano2
    global poslano1
    if (t1 < meja1):
        if (not poslano1):
            text = """Voda ima manj kot""" + str(meja1) +""" stopinj. Pocasi bo potrebno zakurit.
                
                Trenutna temperatura v bojlerju je: """ + str(t1) + """
                Lp, Tvoja Kurilnica
                """
            for prejemnik in prejemniki:
                posljiemail(prejemnik, text)
        poslano1 = True
    if (t1 < meja2):
        if (not poslano2):
            text = """Voda je MRZLA!!!!
                Ima manj kot""" + str(meja2) +""" stopinj. 

                                
                Trenutna temperatura v bojlerju je: """ + str(t1) + """
                Lp, Tvoja Kurilnica
                """
            for prejemnik in prejemniki:
                posljiemail(prejemnik, text)
        poslano2 = True
    if (t1 > meja1):
        poslano1 = False
        poslano2 = False