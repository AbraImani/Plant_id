import os
from fastapi import FastAPI, UploadFile, HTTPException
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import io

# Charger les variables d'environnement
# load_dotenv(find_dotenv(), override=True)
GOOGLE_API_KEY = "AIzaSyBetznO_T7Loxri-xr1_Qzi-PTzyFvokpk"
# Configurer l'API Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "Bonjour"}

@app.post("/upload/")
async def upload_image(file: UploadFile):
    # Vérifier si le fichier est une image
    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image.")
    image_data = file.read()
    # Charger l'image
    image = Image.open(io.BytesIO(await image_data))
    
    # Traiter l'image (similaire à ton code dans talk_with_image.py)
    instructions = """
                    Charge toi de répondre justement aux questions qui se lient à une plante.
                    Si sur l'image on ne trouve pas 50% des choses botaniques, réponds "je suis pas capable de traiter cette photo".
                    Je suis basé pour donner des informations des choses botaniques seulement.
                    
                    Que tes réponses soient toujours en français. Je ne connais aucun autre langue que le français.
                """
    
    prompt = """
            Identifier cette plante sur cette photo et donner les éléments suivants de cette plante en format liste : 
            - son nom
            - son nom scientifique
            - Etat de la plante (S'il est malade ou pas)
            - un bref description
            - Détails sur la plante (Famille, Native region, Growth Habit, Flower color and Leaf Type)
            """
    
    # Combiner instructions et prompt
    prompts = instructions + prompt

    # Utiliser le modèle pour générer la réponse
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompts, image])
        
        # Retourner la réponse en JSON
        return {"réponse": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur dans le traitement de l'image : {str(e)}")


# Pour lancer l'API avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
