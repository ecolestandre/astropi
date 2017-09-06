#MISSION 2 : détection de la mise en route des moteurs-fusées
# pour la remise sur une orbite plus haute avec alerte pour les astronautes
# Ecole de Saint-André d'Embrun, Hautes-Alpes, France
# Classe des CE1, CE2, CM1 et CM2

#import du module SenseHat
from sense_hat import SenseHat

#import du module time
import time
 
sense = SenseHat()

#définition des couleurs pour l'affichage Leds du Sense Hat
vert = (0, 255, 0)
rouge = (255, 0, 0)
bleu = (0, 0, 255)
jaune = (255, 255, 0)
orange = (237, 127, 16)
noir = (0, 0, 0)
blanc = (255, 255, 255)
violet = (102, 0, 153)
rose = (253, 108, 158)
gris = (96, 96, 96)
brun = (91, 60, 17)

#image Sense Hat signalant la mise en route des moteurs fusées orange
moteuroui = [blanc, blanc, blanc, rouge, blanc, blanc, blanc, blanc,
             blanc, blanc, rouge, rouge, rouge, blanc, blanc, blanc,
             blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
             blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
             blanc, blanc, gris, gris, gris, blanc, blanc, blanc,
             blanc, gris, gris, gris, gris, gris, blanc, blanc,
             blanc, gris, orange, orange, orange, gris, blanc, blanc,
             blanc, blanc, orange, orange, orange, blanc, blanc, blanc]

#image Sense Hat signalant la mise en route des moteurs fusées rouge
moteuroui2 = [blanc, blanc, blanc, rouge, blanc, blanc, blanc, blanc,
             blanc, blanc, rouge, rouge, rouge, blanc, blanc, blanc,
             blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
             blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
             blanc, blanc, gris, gris, gris, blanc, blanc, blanc,
             blanc, gris, gris, gris, gris, gris, blanc, blanc,
             blanc, gris, rouge, rouge, rouge, gris, blanc, blanc,
             blanc, blanc, rouge, rouge, rouge, blanc, blanc, blanc]

#image Sense Hat signalant l'absence d'accélération = moteurs fusées au repos orbite stable
moteurnon = [blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,
         blanc, blanc, blanc, rouge, blanc, blanc, blanc, blanc,
         blanc, blanc, rouge, rouge, rouge, blanc, blanc, blanc,
         blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
         blanc, blanc, gris, bleu, gris, blanc, blanc, blanc,
         blanc, blanc, gris, gris, gris, blanc, blanc, blanc,
         blanc, gris, gris, gris, gris, gris, blanc, blanc,
         blanc, gris, blanc, blanc, blanc, gris, blanc, blanc,]

#image Sense Hat signalant une décélération
chute = [blanc, blanc, gris, blanc, blanc, blanc, gris, blanc,
         blanc, blanc, gris, gris, gris, gris, gris, blanc,
         blanc, blanc, blanc, gris, gris, gris, blanc, blanc,
         blanc, blanc, blanc, gris, bleu, gris, blanc, blanc,
         blanc, blanc, blanc, gris, bleu, gris, blanc, blanc,
         blanc, blanc, blanc, rouge, rouge, rouge, blanc, blanc,
         blanc, blanc, blanc, blanc, rouge, blanc, blanc, blanc,
         blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc]

#image Sense Hat alerte astronaute
danger = [bleu, bleu, bleu, bleu, bleu, bleu, bleu, bleu,
          bleu, bleu, bleu, rouge, rouge, bleu, bleu, bleu,
          bleu, bleu, rouge, gris, gris, rouge, bleu, bleu,
          bleu, bleu, rouge, gris, gris, rouge, bleu, bleu,
          bleu, rouge, rouge, gris, gris, rouge, rouge, bleu,
          bleu, rouge, rouge, rouge, rouge, rouge, rouge, bleu,
          rouge, rouge, rouge, gris, gris, rouge, rouge, rouge,
          rouge, rouge, rouge, rouge, rouge, rouge, rouge, rouge]
          
          


#effacer leds Sense Hat
sense.clear()

#ouverture d'un fichier nommé moteurfusee pour ajouter les données générales x, y, z
fichier1 = open("moteurfusee.csv", "a")

#pour écrire dans le fichier le nom des colonnes
fichier1.write("Date, Accélération x y z \n")

#ouverture d'un fichier nommé moteurfuseeactif pour ne garder que les données notant la mise en route des moteurs fusées
fichier2 = open("moteurfuseeactif.csv", "a")

#pour écrire dans le fichier le nom des colonnes
fichier2.write("Date, Accélération x y z \n")
            


# heure de départ du test
timedepart = time.time()

#durée du test en secondes
#timesortie = 60*2 #pour nos tests sur deux minutes...
#timesortie de 85 min pour l'ISS
timesortie = 60*85

#répéter jusqu'à ce qu'on atteigne 1h25min de test
while time.time() < timedepart + timesortie:
    
    #relevé du capteur accélération
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    #arrondi au nombre entier
    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)
    
    #affichage dans le shell
    print("x={0}, y={1}, z={2}".format(x, y, z))

    #écrire les données générales dans le fichier moteurfusee
    fichier1.write(time.strftime('%d %m %y %T'))
    fichier1.write(",")
    fichier1.write(str(acceleration))
    fichier1.write("\n")

        
    # test s'il n'y a pas d'accélération
    if x == 0 or y == 0 or z == 0:
        
        #affichages Leds sur le Sense Hat de l'image moteurarret + 1 seconde
        sense.set_pixels(moteurnon)
        time.sleep(1)
        
        #affichage Leds sur le Sense Hat de l'accélération sur les 3 axes
        sense.show_message("x:{0}, y:{1}, z:{2}".format(x, y, z), text_colour = vert, scroll_speed=0.03)

    #test s'il y a une accélération
    elif x > 1 or y > 1 or z > 1:
                             
        #écrire les données dans le fichier moteuractif
        fichier2.write(time.strftime('%d %m %y %T'))
        fichier2.write(",")
        fichier2.write(str(acceleration))
        fichier2.write("\n")
        
        #affichage dans le shell signalant l'accélération
        print("Accélération en cours mise en route des moteurs-fusées")

        #affichage Leds sur le Sense Hat de l'image des moteurs fusées en route + danger + 1 seconde
        sense.set_pixels(moteuroui)
        time.sleep(1)
        sense.set_pixels(moteuroui2)
        time.sleep(1)
        sense.set_pixels(danger)
        time.sleep(2)
        
    else:
        #affiche finalement que l'ISS perd de l'altitude dans le shell
        print("L'ISS a tendance à descendre...")
        #affiche Leds Sense Hat pour la perte d'altitude
        sense.set_pixels(chute)

# fermeture des 2 fichiers
fichier2.close()
fichier1.close()


