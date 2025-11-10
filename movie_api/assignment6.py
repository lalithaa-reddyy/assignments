from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

movies = [
    {"title": "Black Mirror", "director": "ABC", "year": 2011},
    {"title": "Jurassic World", "director": "DEF", "year": 2014},
    {"title": "27 Dresses", "director": "GHIJ", "year": 2004},
]
@app.get("/movies")
async def read_all_movies():
    return movies


@app.get("/movies/{movie_title}")
async def read_movie(movie_title: str):
    for movie in movies:
        if movie["title"].casefold() == movie_title.casefold():
            return movie
    raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")


@app.post("/movies/create_movie")
async def create_movie(new_movie: dict = Body(...)):
    for movie in movies:
        if movie["title"].casefold() == new_movie["title"].casefold():
            raise HTTPException(status_code=400, detail="Movie already exists")
    
    movies.append(new_movie)
    return {"message": "Movie added successfully", "movie": new_movie}


@app.delete("/movies/delete_movie/{movie_title}")
async def delete_movie(movie_title: str):
    for movie in movies:
        if movie["title"].casefold() == movie_title.casefold():
            movies.remove(movie)
            return {"message": "Movie deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")



@app.put("/movies/update_movie/{movie_title}")
async def update_movie(movie_title: str, updated_movie: dict = Body(...)):
    for movie in movies:
        if movie["title"].casefold() == movie_title.casefold():
            movie.update(updated_movie)
            return {"message": "Movie updated successfully" }
    raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")
