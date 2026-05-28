const roads = [
  { name: "North Road", inputId: "northRoad", countId: "northCount", node: "north", signalId: "northSignal" },
  { name: "East Road", inputId: "eastRoad", countId: "eastCount", node: "east", signalId: "eastSignal" },
  { name: "South Road", inputId: "southRoad", countId: "southCount", node: "south", signalId: "southSignal" },
  { name: "West Road", inputId: "westRoad", countId: "westCount", node: "west", signalId: "westSignal" },
];

const sampleData = {
  "North Road": 45,
  "East Road": 28,
  "South Road": 60,
  "West Road": 18,
};

const MIN_GREEN_TIME = 10;
const MAX_GREEN_TIME = 60;
const VEHICLES_PER_GREEN_SLOT = 2;
const AVG_WAIT_PER_VEHICLE = 4;
const FIXED_GREEN_TIME = 25;

const form = document.getElementById("trafficForm");
const sampleBtn = document.getElementById("sampleBtn");
const clearBtn = document.getElementById("clearBtn");
const resultTable = document.getElementById("resultTable");
const priorityStrip = document.getElementById("priorityStrip");
const optimizedOrder = document.getElementById("optimizedOrder");
const waitingReduction = document.getElementById("waitingReduction");
const errorMessage = document.getElementById("errorMessage");
const topPriority = document.getElementById("topPriority");

function readVehicleCounts() {
  const graphEdges = [];

  for (const road of roads) {
    const input = document.getElementById(road.inputId);
    const rawValue = input.value.trim();

    if (rawValue === "") {
      throw new Error(`Vehicle count for ${road.name} cannot be empty.`);
    }

    const vehicleCount = Number(rawValue);
    if (!Number.isInteger(vehicleCount) || vehicleCount < 0) {
      throw new Error(`Vehicle count for ${road.name} must be a non-negative integer.`);
    }

    if (vehicleCount > 500) {
      throw new Error(`Vehicle count for ${road.name} is too high for this demo.`);
    }

    graphEdges.push({
      name: road.name,
      source: road.name.replace(" Road", " Entry"),
      destination: "Main Intersection",
      vehicleCount,
    });
  }

  if (graphEdges.every((road) => road.vehicleCount === 0)) {
    throw new Error("At least one road must have vehicles waiting.");
  }

  return graphEdges;
}

function optimizeSignals(graphEdges) {
  /*
    Greedy algorithm steps:
    1. Sort roads in descending order by vehicle count.
    2. Pick the maximum traffic road first.
    3. Allocate larger green time to roads with more vehicles.
    4. Repeat for all remaining roads.

    Time Complexity:
    Sorting n roads takes O(n log n), and assignment takes O(n).
    Overall complexity is O(n log n).
  */
  const sortedRoads = [...graphEdges].sort((a, b) => b.vehicleCount - a.vehicleCount);
  let totalWaitBefore = 0;
  let totalWaitAfter = 0;

  const plans = sortedRoads.map((road, index) => {
    const priority = index + 1;
    const calculatedTime = MIN_GREEN_TIME + Math.floor(road.vehicleCount / VEHICLES_PER_GREEN_SLOT);
    const greenTime = Math.min(MAX_GREEN_TIME, Math.max(MIN_GREEN_TIME, calculatedTime));
    const waitingBefore = road.vehicleCount * AVG_WAIT_PER_VEHICLE;
    const serviceGain = Math.max(1, greenTime - FIXED_GREEN_TIME);
    const waitingAfter = Math.max(0, waitingBefore - serviceGain * priority);

    totalWaitBefore += waitingBefore;
    totalWaitAfter += waitingAfter;

    return {
      priority,
      roadName: road.name,
      vehicleCount: road.vehicleCount,
      greenTime,
      waitingBefore,
      waitingAfter,
    };
  });

  return {
    plans,
    waitingTimeReduced: Math.max(0, totalWaitBefore - totalWaitAfter),
  };
}

function renderResults(plans, waitingTimeReduced) {
  resultTable.innerHTML = plans
    .map(
      (plan) => `
        <tr>
          <td>${plan.priority}</td>
          <td>${plan.roadName}</td>
          <td>${plan.vehicleCount}</td>
          <td>${plan.greenTime} sec</td>
          <td>${plan.waitingBefore} sec</td>
          <td>${plan.waitingAfter} sec</td>
        </tr>
      `
    )
    .join("");

  priorityStrip.innerHTML = plans
    .map(
      (plan) => `
        <div class="priority-card">
          <strong>P${plan.priority}: ${plan.roadName}</strong>
          <span>${plan.vehicleCount} vehicles</span>
          <span>${plan.greenTime} sec green signal</span>
        </div>
      `
    )
    .join("");

  optimizedOrder.textContent = `Optimized order: ${plans.map((plan) => plan.roadName).join(" -> ")}`;
  waitingReduction.textContent = `Waiting time reduced: ${waitingTimeReduced} seconds`;
  topPriority.textContent = `Priority: ${plans[0].roadName} (${plans[0].greenTime}s green)`;
}

function updateVisuals(plans = []) {
  const planByRoad = new Map(plans.map((plan) => [plan.roadName, plan]));

  for (const road of roads) {
    const input = document.getElementById(road.inputId);
    const countLabel = document.getElementById(road.countId);
    const node = document.querySelector(`.${road.node}`);
    const vehicleCount = Number(input.value) || 0;
    const plan = planByRoad.get(road.name);

    countLabel.textContent = plan
      ? `P${plan.priority} | ${vehicleCount} vehicles | ${plan.greenTime}s`
      : `${vehicleCount} vehicles`;

    node.classList.toggle("active", Boolean(plan && plan.priority === 1));
  }
}

function showEmptyResults() {
  resultTable.innerHTML = '<tr><td colspan="6">No optimized signal allocation yet.</td></tr>';
  priorityStrip.innerHTML = '<div class="priority-card empty">Run optimization to view priority order.</div>';
  optimizedOrder.textContent = "Optimized order: Not calculated";
  waitingReduction.textContent = "Waiting time reduced: 0 seconds";
  topPriority.textContent = "Priority: Not calculated";
}

function loadSampleData() {
  for (const road of roads) {
    document.getElementById(road.inputId).value = sampleData[road.name];
  }

  errorMessage.textContent = "";
  showEmptyResults();
  updateVisuals();
}

function clearInputs() {
  for (const road of roads) {
    document.getElementById(road.inputId).value = "";
  }

  errorMessage.textContent = "";
  showEmptyResults();
  updateVisuals();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  errorMessage.textContent = "";

  try {
    const graphEdges = readVehicleCounts();
    const { plans, waitingTimeReduced } = optimizeSignals(graphEdges);
    renderResults(plans, waitingTimeReduced);
    updateVisuals(plans);
  } catch (error) {
    errorMessage.textContent = error.message;
  }
});

sampleBtn.addEventListener("click", loadSampleData);
clearBtn.addEventListener("click", clearInputs);

for (const road of roads) {
  document.getElementById(road.inputId).addEventListener("input", () => updateVisuals());
}

updateVisuals();
