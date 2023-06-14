##################################
#    DEPENDENCIES & CONSTANTS    #
##################################

import os
import shutil
import json
import logging
from SpeechRecognition.src.speaker_diarization import SpeakerDiarization
import nltk
nltk.download('punkt')
from SentimentalAnalysis.src.endpoint import predict_script

SUPPORTED_EXTENSIONS = [".mp3", ".mp4", ".wav", ".json"]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "static")
TEMPLATES_PATH = os.path.join(ROOT_PATH, "templates")
MOVIES_PATH = os.path.join(ROOT_PATH, "movies")

if not os.path.isdir(MOVIES_PATH):
    os.mkdir(MOVIES_PATH)

# Logging module is initialized.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(ROOT_PATH, "samsa.log")),
    ]
)

from threading import Thread
from typing import Optional, List, Union
from fastapi import FastAPI, Request, File, UploadFile, Response, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, or_

from . import models, schemas, crud, database, functions, exceptions

# Set the path to the ffmpeg executable
ffmpeg_path = '/ffmpeg.exe'

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# Files added to
app.mount("/files", StaticFiles(directory=MOVIES_PATH), name="files")

# HTML templates inserted.
templates = Jinja2Templates(directory=TEMPLATES_PATH)

# Creates db tables.
database.Base.metadata.create_all(bind=database.engine)

# next function is necessary to get Session object.
next(database.get_db()).execute(text('CREATE VIRTUAL TABLE IF NOT EXISTS movies_fts USING fts5(movies)'))

# The model that segments, diarize speech is loaded.
speaker_diarization_model = SpeakerDiarization()

##################################
#     HTML RESPONSES (VIEWS)     #
##################################
@app.get('/', response_class=HTMLResponse)
async def index_view(request: Request):
    # This route is used to route itself to the previously uploaded audio files, previously processed audio files to look its graphs.
    return templates.TemplateResponse("index.html", {"request": request, "message": "message"})


@app.get("/database", response_class=HTMLResponse)
async def database_view(request: Request, db: models.Session = Depends(database.get_db)):
    movies = db.query(models.MovieDB).all()
    temp_movies = []
    for movie in movies:
        temp_movie = dict()
        movie_path = os.path.join(MOVIES_PATH, str(movie.id))

        temp_movie['movie'] = movie
        temp_movie['speakers'] = functions.get_speakers(movie_path, os.path.splitext(movie.name)[0] + '.json')
        temp_movie['files'] = functions.get_files(movie_path)
        temp_movies.append(temp_movie)

    return templates.TemplateResponse("database.html", {"request": request, "movies": temp_movies})


@app.get("/authors", response_class=HTMLResponse)
async def authors_view(request: Request):
    return templates.TemplateResponse("authors.html", {"request": request})


@app.get("/movies/{movie_id}", response_class=HTMLResponse)
async def movie_view(request: Request, movie_id: int, db: models.Session = Depends(database.get_db)):
    movie = db.query(models.MovieDB).filter(models.MovieDB.id == movie_id).first()
    if movie == None:
        return templates.TemplateResponse("not_found.html", {"request": request})
    movie_id = movie.id
    name, extension = os.path.splitext(movie.name)
    description = movie.description
    movie_path = os.path.join(MOVIES_PATH, str(movie_id))
    speakers = functions.get_speakers(movie_path, name + '.json')
    files = functions.get_files(movie_path)

    # TODO: show graphs.
    m = {
        'movie_id': movie_id,
        'name': name,
        'extension': extension,
        'description': description,
        'speakers': speakers,
        'files': files,
        'graphs': 1
    }
    return templates.TemplateResponse("movie.html", {"request": request, "m": m})


##################################
#         API OPERATIONS         #
##################################

@app.get('/m', response_model=List[schemas.Movie])
async def list_movies(offset: int = 0, limit: int = 100, db: models.Session = Depends(database.get_db)):
    ret_list = db.query(models.MovieDB).offset(offset).limit(limit).all()
    return JSONResponse(content=[jsonable_encoder(schemas.Movie.from_orm(item)) for item in ret_list])


@app.get('/m/{id}')
async def get_movie(id: int, db: models.Session = Depends(database.get_db)):
    movie = db.query(models.MovieDB).filter(models.MovieDB.id == id).first()
    if movie is None:
        return Response(content=json.dumps({"error": "There is no such entry with id=`{}`".format(id)}), status_code=404)
    return JSONResponse(content=jsonable_encoder(schemas.Movie.from_orm(movie)))


@app.post('/')
async def upload_audio_File(uploaded_file: UploadFile = File(...), db: models.Session = Depends(database.get_db)):
    if uploaded_file == None:
        return JSONResponse(content=json.dumps({"error": "File cannot be empty. Please select a file."}), status_code=422)
    
    file_name, file_extension = os.path.splitext(uploaded_file.filename)
    if file_extension not in SUPPORTED_EXTENSIONS:
        e = exceptions.UnsupportedFileError(file_extension)
        logging.error(e.message)
        return JSONResponse(content=json.dumps({"error": e.message}), status_code=422)
    
    try:
        db_movie = crud.MovieCRUD.create_movie(db, uploaded_file.filename)
    except exceptions.DuplicateMovieError as e:
        logging.error(e.message)
        return JSONResponse(content=json.dumps({'error': e.message}), status_code=400)   

    # Creates the directory for uploaded file and stores it.
    db_movie_dir_path = os.path.join(MOVIES_PATH, str(db_movie.id))
    if os.path.isdir(db_movie_dir_path): shutil.rmtree(db_movie_dir_path)
    os.mkdir(db_movie_dir_path)

    # Creates related files
    if file_extension == ".mp3":
        wav_file_path = functions.mp3_to_wav(uploaded_file, db_movie_dir_path)

    elif file_extension == ".mp4":
        wav_file_path = functions.mp4_to_wav(uploaded_file, db_movie_dir_path)

    elif file_extension == ".wav":
        wav_file_path = os.path.join(db_movie_dir_path, uploaded_file.filename)
        with open(wav_file_path, "wb") as wav_file:
            wav_file.writelines(uploaded_file.file.readlines())
    
    if file_extension != ".json":
        output_file_path = os.path.join(db_movie_dir_path, file_name + ".json")
        thread_speech = Thread(target=functions.run_speech_2_text, args=(wav_file_path, output_file_path, speaker_diarization_model))
        thread_speech.start()
        
    else:
        json_file_path = os.path.join(db_movie_dir_path, uploaded_file.filename)
        with open(json_file_path, 'wb') as json_file:
            json_file.writelines(uploaded_file.file.readlines())
        json_data = json.loads(json_file_path)

        # Apply sentiment analysis
        sentiment_results = predict_script(json_file_path)
        for idx in range(len(json_data)):
            json_data[idx]['results'] = {
                "sentiment": sentiment_results.iloc[idx]['sentiment'],
                "probability": sentiment_results.iloc[idx]['probability'],
                "valence": sentiment_results.iloc[idx]['valence']
            }

        functions.save_JSON(json_file_path, json_data)

    logging.info('The file: "' + file_name + '" is successfully uploaded')
    return JSONResponse(content=jsonable_encoder(db_movie))


# These two methods are not going to be rendered.
@app.put("/m/{id}")
async def update_movie_info(id: int, movie: schemas.MovieUpdate, db: models.Session = Depends(database.get_db)):
    db_movie = db.query(models.MovieDB).filter(models.MovieDB.id == id).first()
    if db_movie is None:
        logging.info('There is no such movie `{}` to be updated'.format(id))
        return JSONResponse(content=json.dumps({"error": "There is no such movie."}), status_code=404)
    else:
        movie_path = os.path.join(MOVIES_PATH, str(db_movie.id))

        # To change speaker names.        
        for speaker in movie.speakers:
            msg = functions.change_speaker_name(
                movie_path,
                os.path.splitext(db_movie.name)[0] + '.json',
                speaker["old_name"],
                speaker["new_name"]
                )
            if msg != 'ok':
                logging.warning(msg)

        # To change and save movie objects.
        db_movie.description = movie.description
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        logging.info('Movie `{}` has been successfully updated.'.format(db_movie.id))
        return JSONResponse(content=jsonable_encoder(schemas.Movie.from_orm(db_movie)))


@app.delete("/m/{id}", status_code=204)
async def delete_movie(id: int, db:models.Session = Depends(database.get_db)):
    db_movie = db.query(models.MovieDB).filter(models.MovieDB.id == id).first()
    if db_movie is None:
        logging.info('There is no such movie `{}` to be deleted.'.format(id))
        return JSONResponse(content=json.dumps({"error": "There is no such movie."}), status_code=404)
    else:
        db.delete(db_movie)    # delete from db.
        db.commit()
        movie_path = os.path.join(MOVIES_PATH, str(id))
        if os.path.isdir(movie_path):    # delete dir.
            shutil.rmtree(movie_path)
        logging.info('Movie object `{}` has been deleted successfully.'.format(id))
    return JSONResponse(content=json.dumps({"message": "success"}))


# Full text search to find movies.
@app.post("/search", response_model = List[schemas.Movie])
def search(q: str, db: models.Session = Depends(database.get_db)):
    results = db.query(models.MovieDB).filter(or_(
        models.MovieDB.description.like('%' + q + '%'),
        models.MovieDB.name.like('%' + q + '%'),
        models.MovieDB.id.like('%' + q + '%'),
        models.MovieDB.date.like('%' + q + '%')
    )).all()
    logging.info('Search has been run with parameter `{}`'.format(q))
    if len(results) == 0:
        return JSONResponse(content=json.dumps({"message": "There is no such movie in database."}), status_code=404)
    else:
        return JSONResponse(content=[jsonable_encoder(schemas.Movie.from_orm(result)) for result in results], status_code=200)
    

@app.get("/not-found")
def not_found_page(request: Request, q: str = ""):
    return templates.TemplateResponse('not_found.html', {"request": request, "q": q}, status_code=404)
