# Smart Traffic Signal Optimization Using Greedy Algorithm

VTU 5th semester ADA mini-project available as both a website and a Python Tkinter app.

## How to Run

### Website Version

Open `index.html` in any browser.

### Python Tkinter Version

```bash
python3 smart_traffic_signal_optimizer.py
```

Use the **Load Sample Traffic Data** button for a quick demo, or enter custom
vehicle counts and click **Start Optimization**.

## Features

- Traffic intersection simulation
- Vehicle count input system
- Greedy-based signal optimization
- Priority assignment for crowded roads
- Signal timing visualization
- Real-time result display
- Error handling for invalid inputs
- Sample traffic data
- Signal allocation table
- Waiting time reduction display

## Core ADA Concept

The project uses a Greedy Algorithm to prioritize the road with the maximum vehicle count first. Roads are represented as graph edges, and vehicle counts are used as weights.

Greedy Algorithms are widely used in resource allocation, scheduling, and optimization problems in real-world systems.

## Files

- `index.html`: Website interface
- `styles.css`: Website styling and traffic visualization
- `script.js`: Greedy algorithm and browser interactivity
- `smart_traffic_signal_optimizer.py`: Main Python Tkinter project
- `PROJECT_REPORT.md`: Markdown report for presentation and viva
- `README.md`: Quick project overview and run instructions
