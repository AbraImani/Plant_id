import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from PIL import Image
import time

load_dotenv(find_dotenv(), override=True)

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

image_path =input("Entrez le chemin de l'image : ")

if not os.path.isfile(image_path):
    raise SystemExit("Le chemin de l'image invalide ! Exiting ... ")

image = Image.open(image_path)
print(image)

model = genai.GenerativeModel('gemini-1.5-flash')

while True :
    instructions = """
                Charge toi de repondre justement aux questions qui se lié à une plante, si sur l'image on 
                ne trouve pas 50pourcent des choses botaniques, réponds je suis pas capable de traiter cette photo.
                je suis base de donner des informations des choses botaniques seulement.
                
                Que tes reponses soit toujours en Français S'il vous plait, je ne connais aucun autre langue que
                le français.
            """
            
    prompt ="""
            J'aime que les reponses soit en français
            Identifier cette plante sur cette photo et donner les éléments suivantes de cette plante en format JSON : 
            - son nom
            - son nom scientifique
            - Etat de la plante (S'il est malade ou pas, une reponse de soit il est malade ou pas juste)
            - un bref description
            - Un detail plante (Famille, Native region, Growth Habit, Flower color and Leaf Type)

            """
            #            - Etat de la plante (S'il est malade ou pas, une reponse de soit il est malade ou pas juste)
    prompts = instructions + prompt
    if prompt.lower not in ['exit', 'quitter', 'bye']:
        reponse = model.generate_content([prompts, image])
        print('')
        print(reponse.text)
        print('')
        break
        
    else :
        print('Je vous laisse')
        time.sleep(2)
        print('bye-bye')
        break