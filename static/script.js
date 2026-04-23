const canvas = document.getElementById("gridCanvas")
const ctx    = canvas.getContext("2d")

const size = 50
const cell = 12

canvas.width  = size * cell
canvas.height = size * cell

let grid  = []
let start = null
let goal  = null

const SPEED_MAP = { 1: 80, 2: 40, 3: 15, 4: 5, 5: 1 }
let visitDelay = 15
let pathDelay  = 25


function updateSpeed(val) {
  document.getElementById("speedLabel").textContent = val + "x";
  visitDelay = SPEED_MAP[val];
  pathDelay  = Math.round(SPEED_MAP[val] * 1.6);
}

function setStatus(msg, color) {
  const el = document.getElementById("statusText")
  el.textContent = msg
  el.style.color = color || "var(--cyan)"
}

// Live counter updaters
function setNodesExplored(n) {
  document.getElementById("nodesExplored").textContent = n
}

function setPathLength(n) {
  document.getElementById("pathLength").textContent = n
}

function setPhase(text, color) {
  const el = document.getElementById("currentPhase")
  el.textContent = text
  el.style.color = color || "var(--cyan)"
}


function resetCounters() {
  setPathLength(0);
  setPhase("IDLE", "var(--text)");
}

// Draw a glowing orange circle with white border for GOAL
function drawGoalIcon(x, y) {
  const cx = y * cell + cell / 2;
  const cy = x * cell + cell / 2;
  const radius = cell * 0.38;
  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
  ctx.shadowColor = '#ff9f0a';
  ctx.shadowBlur = 16;
  ctx.fillStyle = '#ff9f0a';
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#fff';
  ctx.stroke();
  ctx.restore();
}

function getAlgoColor(algo) {
  const map = {
    bfs:    "#00cfff",
    dfs:    "#bf5fff",
    astar:  "#00cfff",
    greedy: "#ff9f0a",
    best:   "#e67e22"
  }
  return map[algo] || "#95a5a6"
}

// Generate Grid
async function generateGrid() {
  setStatus("GENERATING GRID...")
  resetCounters()
  const res = await fetch("/grid")
  grid  = await res.json()
  start = null
  goal  = null
  drawGrid()
  setStatus("GRID READY — CLICK TO SET START")
}

// Draw full grid
function drawGrid() {
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      if      (grid[i][j] === -1) ctx.fillStyle = "#ff2d55";
      else if (grid[i][j] === 5)  ctx.fillStyle = "#ff9f0a";
      else                        ctx.fillStyle = "#060d14";
      ctx.fillRect(j*cell, i*cell, cell, cell);
      ctx.strokeStyle = "rgba(0,207,255,0.12)";
      ctx.strokeRect(j*cell, i*cell, cell, cell);
    }
  }
  redrawMarkers();
}

// Draw single cell
function drawCell(x, y, color, glow, type = null) {
  // Custom rendering for START and GOAL
  if (type === 'start') {
    drawStarCell(x, y);
    return;
  }
  if (type === 'goal') {
    drawGoalCell(x, y);
    return;
  }
  ctx.fillStyle = color;
  ctx.fillRect(y*cell, x*cell, cell, cell);
  if (glow) {
    ctx.shadowColor = color;
    ctx.shadowBlur  = 8;
    ctx.fillRect(y*cell, x*cell, cell, cell);
    ctx.shadowBlur  = 0;
  }
  ctx.strokeStyle = "rgba(0,207,255,0.08)";
  ctx.strokeRect(y*cell, x*cell, cell, cell);
}

// Draw a glowing green star for START
function drawStarCell(x, y) {
  const cx = y * cell + cell / 2;
  const cy = x * cell + cell / 2;
  const outer = cell * 0.45;
  const inner = cell * 0.20;
  ctx.save();
  ctx.beginPath();
  for (let i = 0; i < 5; i++) {
    const angle = ((18 + i * 72) * Math.PI) / 180;
    ctx.lineTo(cx + Math.cos(angle) * outer, cy - Math.sin(angle) * outer);
    const angle2 = ((54 + i * 72) * Math.PI) / 180;
    ctx.lineTo(cx + Math.cos(angle2) * inner, cy - Math.sin(angle2) * inner);
  }
  ctx.closePath();
  ctx.shadowColor = '#39ff14';
  ctx.shadowBlur = 16;
  ctx.fillStyle = '#39ff14';
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#fff';
  ctx.stroke();
  ctx.restore();
}

// Draw a glowing orange circle with white border for GOAL
function drawGoalCell(x, y) {
  const cx = y * cell + cell / 2;
  const cy = x * cell + cell / 2;
  const radius = cell * 0.38;
  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
  ctx.shadowColor = '#ff9f0a';
  ctx.shadowBlur = 16;
  ctx.fillStyle = '#ff9f0a';
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#fff';
  ctx.stroke();
  ctx.restore();
}

function redrawMarkers() {
  if (start) drawCell(start[0], start[1], null, false, 'start');
  if (goal)  drawCell(goal[0],  goal[1],  null, false, 'goal');
}

// Canvas click
canvas.addEventListener("click", function(e) {
  const x = Math.floor(e.offsetY / cell)
  const y = Math.floor(e.offsetX / cell)

  if (grid[x][y] === -1) {
    setStatus("⚠ OBSTACLE — CHOOSE ANOTHER CELL", "var(--pink)")
    return
  }

  if (!start) {
    start = [x, y];
    drawCell(x, y, null, false, 'start');
    setStatus("START SET — CLICK TO SET GOAL", "var(--purple)");
  } else if (!goal) {
    goal = [x, y];
    drawCell(x, y, null, false, 'goal');
    setStatus("GOAL SET — PRESS FIND ROUTE", "var(--yellow)");
  }
})

// Animate with live counter
async function animateSearch(visited, path, color) {

  // Phase 1: Exploration with live node counter
  setStatus("SCANNING — EXPLORING NODES...", "var(--cyan)")
  setPhase("EXPLORING", "var(--cyan)")

  for (let i = 0; i < visited.length; i++) {
    const node = visited[i]
    drawCell(node[0], node[1], color, false)

    // Update counter every single node
    setNodesExplored(i + 1)

    await delay(visitDelay)
  }

  // Phase 2: Path tracing with live path counter
  setStatus("PATH FOUND — TRACING ROUTE...", "var(--green)")
  setPhase("TRACING", "var(--green)")

  for (let i = 0; i < path.length; i++) {
    const p = path[i]
    drawCell(p[0], p[1], "#39ff14", true)

    // Update path length live
    setPathLength(i + 1)

    await delay(pathDelay)
  }

  redrawMarkers()
  setStatus("ROUTE COMPLETE ✓", "var(--green)")
  setPhase("DONE ✓", "var(--green)")
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

// Find Route
async function findRoute() {
  if (!start || !goal) {
    setStatus("⚠ SET START AND GOAL FIRST", "var(--pink)")
    return
  }

  resetCounters()
  const algo = document.getElementById("algo").value
  setStatus("COMPUTING ROUTE...", "var(--cyan)")
  setPhase("COMPUTING", "var(--cyan)")

  const res = await fetch("/route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, goal, algorithm: algo })
  })

  const data = await res.json()

  if (!data.path || data.path.length === 0) {
    setStatus("⚠ NO PATH FOUND", "var(--pink)")
    setPhase("FAILED", "var(--pink)")
    return
  }

  await animateSearch(data.visited, data.path, getAlgoColor(algo))
  updateTable(data.comparison)
}

// Update table
function updateTable(results) {
  const tbody = document.querySelector("#resultTable tbody")
  tbody.innerHTML = ""

  const lengths = results.map(r => r.length).filter(l => l > 0)
  const minLen  = Math.min(...lengths)

  results.forEach(r => {
    let ratingClass = "rating-avg";
    let ratingText  = "";

    if (r.length === 0) {
      ratingText  = "NO PATH";
      ratingClass = "rating-slow";
    } else if (r.length === minLen) {
      ratingText  = "OPTIMAL ★";
      ratingClass = "rating-best";
    } else if (r.length <= minLen * 1.1) {
      ratingText  = "GOOD";
      ratingClass = "rating-good";
    } else {
      ratingText  = "NOT OPTIMAL";
      ratingClass = "rating-slow";
    }

    tbody.innerHTML += `
      <tr>
        <td>${r.algorithm}</td>
        <td>${r.length || "—"}</td>
        <td>${r.time}s</td>
        <td class="${ratingClass}">${ratingText}</td>

      </tr>`;
  });
}


// Reset
function resetSelection() {
  start = null
  goal  = null
  resetCounters()
  drawGrid()
  setStatus("RESET — CLICK TO SET START")
}

// Ensure grid is generated and drawn on page load
window.onload = generateGrid;
