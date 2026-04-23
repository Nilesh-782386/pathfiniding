from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from grid_generator import generate_grid
from bfs_algorithm import bfs
from dfs_algorithm import dfs
from astar_algorithm import astar
from greedy_best_first import greedy_best_first
from best_first import best_first
from comparison import compare_algorithms

app = Flask(__name__)
CORS(app)

grid = generate_grid()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/grid")
def get_grid():
    global grid
    grid = generate_grid()
    return jsonify(grid)


@app.route("/route", methods=["POST"])
def route():

    data = request.json

    start = tuple(data["start"])
    goal = tuple(data["goal"])
    algo = data.get("algorithm", "astar")

    if algo == "bfs":
        path, visited = bfs(grid, start, goal)

    elif algo == "dfs":
        path, visited = dfs(grid, start, goal)

    elif algo == "astar":
        path, visited = astar(grid, start, goal)

    elif algo == "greedy":
        path, visited = greedy_best_first(grid, start, goal)

    elif algo == "best":
        path, visited = best_first(grid, start, goal)

    else:
        path, visited = [], []

    comparison = compare_algorithms(grid, start, goal)

    return jsonify({
        "path": path,
        "visited": visited,
        "comparison": comparison
    })
   

if __name__ == "__main__":
    app.run(debug=True)