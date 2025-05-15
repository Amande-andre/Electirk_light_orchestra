from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

# Ajout du middleware CORS pour permettre les requêtes cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # il faudra préciser les origines autorisées plus tard
    allow_credentials=True,     # pour l'instant, on autorise toutes les origines
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compile/")
async def compile_file(file: UploadFile = File(...)):
    filename = file.filename  # Nom du fichier
    filepath = f"/tmp/{filename}"
    
    # Sauvegarder le fichier temporairement
    with open(filepath, "wb") as f:
        f.write(await file.read())
    
    output_binary = filepath.replace(".c", "")
    
    try:
        # Compiler avec gcc
        compile_result = subprocess.run(
            ["gcc", filepath, "-o", output_binary],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if compile_result.returncode != 0:
            return {"success": False, "error": compile_result.stderr, "output": None}
        
        # Exécuter le binaire généré
        run_result = subprocess.run(
            [output_binary],
            capture_output=True,
            text=True,
            timeout=5  # Timeout de 5 secondes pour l'exécution
        )
        
        # Construire la réponse
        return {
            "success": True, 
            "message": f"{filename} compilé avec succès",
            "output": run_result.stdout,
            "error_output": run_result.stderr if run_result.stderr else None,
            "exit_code": run_result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False, 
            "error": "L'exécution du programme a dépassé le délai imparti", 
            "output": None
        }
    except Exception as e:
        return {"success": False, "error": str(e), "output": None}