#MISSION 1 : détection des astronautes dans le module Columbus
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

#image Sense Hat signalant une augmentation de l'humidité
hplus = [blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, rouge, blanc,
         bleu, blanc, blanc, bleu, blanc, rouge, rouge, rouge,
         bleu, bleu, bleu, bleu, blanc, blanc, rouge, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,]

#image Sense Hat signalant une stabilisation de l'humidité
hstable = [blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, rouge, rouge, rouge,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, bleu, bleu, bleu, blanc, rouge, rouge, rouge,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,]

#image Sense Hat signalant une diminution de l'humidité
hmoins = [blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, rouge, rouge, rouge,
         bleu, bleu, bleu, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         bleu, blanc, blanc, bleu, blanc, blanc, blanc, blanc,
         blanc, blanc, blanc, blanc, blanc, blanc, blanc, blanc,]

#image Sense Hat tête d'astronaute
humain = [blanc, blanc, brun, brun, brun, brun, blanc, blanc,
          blanc, brun, brun, brun, brun, brun, brun, blanc,
          brun, brun, bleu, rose, rose, bleu, brun, brun,
          brun, rose, rose, rose, rose, rose, rose, brun,
          blanc, rose, rouge, rose, rose, rouge, rose, blanc,
          blanc, rose, rose, rouge, rouge, rose, rose, blanc,
          blanc, rose, rose, rose, rose, rose, rose, blanc,
          blanc, blanc, blanc, rose, rose, blanc, blanc, blanc]


#effacer leds Sense Hat
sense.clear()

#prise du taux d'humidité de départ (sans personne dans Columbus...)
humide = sense.get_humidity()

#arrondi à un chiffre après la virgule
initiale=round(humide, 1)

#affichage dans le shell du taux d'humidité de départ
print("Humidité initiale", initiale)

#ouverture d'un fichier nommé humide pour ajouter les données générales du taux d'humidité
fichier1 = open("humide.csv", "a")

#pour écrire dans le fichier le nom des colonnes
fichier1.write("Date, Humidité \n")

#ouverture d'un fichier monné presence pour ne garder que les données notant la présence d'un astronaute
fichier2 = open("presence.csv", "a")

#pour écrire dans le fichier le nom des colonnes
fichier2.write("Date, Humidité \n")
            
#affichage dans le shell
print ("Date            , Humidité")


#calcul du seuil à partir duquel on pense qu'une personne est présente soit 5% de plus que le taux initial
var_plus = initiale*1.05

# heure de départ du test
timedepart = time.time()

#durée du test en secondes
#timesortie = 60*2 pour nos tests sur deux minutes...
#timesortie de 85 min pour l'ISS
timesortie = 60*85

#répéter jusqu'à ce qu'on atteigne 1h25min de test
while time.time() < timedepart + timesortie:
    
    #relevé du capteur humidité
    humidity = sense.get_humidity()

    #arrondi à 1 chiffre après la virgule
    h=round(humidity, 1)

    #écrire les données dans le fichier humide
    fichier1.write(time.strftime('%d %m %y %T'))
    fichier1.write(",")
    fichier1.write(str(humidity))
    fichier1.write("\n")

    print(time.strftime('%d %m %y %T'),h)
    
    # test si le taux est inférieur à la valeur initiale + 5%
    if h<var_plus:
        #affichages Leds sur le Sense Hat du H- et H= + 1 seconde
        sense.set_pixels(hmoins)
        time.sleep(1)
        sense.set_pixels(hstable)
        time.sleep(1)
        #affichage Leds sur le Sense Hat du taux d'humidité
        sense.show_message("H:{0}".format(h), text_colour = vert, scroll_speed=0.05)
        
        

    else:
        #écrire les données dans le fichier presence
        fichier2.write(time.strftime('%d %m %y %T'))
        fichier2.write(",")
        fichier2.write(str(humidity))
        fichier2.write("\n")
        
        #affichage dans le shell signalant la présence
        print("Présence détectée")

        #affichage Leds sur le Sense Hat de H+ et de la tête d'astronaute + 1 seconde
        sense.set_pixels(hplus)
        time.sleep(1)
        sense.set_pixels(humain)
        time.sleep(1)
        #sense.show_message("il y a quelqu'un dans Columbus", back_colour = rouge)

# fermeture des 2 fichiers
fichier2.close()
fichier1.close()


