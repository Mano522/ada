"""
Smart Traffic Signal Optimization Using Kruskal's Greedy Algorithm
VTU ADA Mini Project - Python + Tkinter

Idea:
Roads connected to one intersection are represented as graph edges. The vehicle
count on each road is treated as the edge weight. Kruskal's greedy algorithm
builds a maximum spanning tree by selecting the highest-weight road that does
not form a cycle, then assigns signal priority and green time from that order.

Time Complexity:
Let n be the number of roads.
- Sorting roads by vehicle count takes O(n log n).
- Disjoint-set union/find operations are almost O(1) per road.
- Assigning signal time for selected roads takes O(n).
- Total time complexity is O(n log n).
- Space complexity is O(n), because we store graph nodes, selected roads, and results.
"""

from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox, ttk


@dataclass
class Road:
    """Represents one road connected to the traffic intersection graph."""

    name: str
    source: str
    destination: str
    vehicle_count: int


@dataclass
class SignalPlan:
    """Stores the optimized result for one road."""

    priority: int
    road_name: str
    vehicle_count: int
    green_time: int
    waiting_time_before: int
    waiting_time_after: int


class TrafficGraph:
    """
    Simple graph representation for one intersection.

    The central node is the intersection. Each road is an edge from the road
    entry point to the intersection. Vehicle count is the edge weight.
    """

    def __init__(self) -> None:
        self.roads: list[Road] = []

    def add_road(self, name: str, source: str, destination: str, vehicle_count: int) -> None:
        self.roads.append(Road(name, source, destination, vehicle_count))

    def clear(self) -> None:
        self.roads.clear()


class DisjointSet:
    """Union-find structure used by Kruskal's algorithm."""

    def __init__(self, nodes: set[str]) -> None:
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node: str) -> str:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first: str, second: str) -> bool:
        first_root = self.find(first)
        second_root = self.find(second)

        if first_root == second_root:
            return False

        if self.rank[first_root] < self.rank[second_root]:
            self.parent[first_root] = second_root
        elif self.rank[first_root] > self.rank[second_root]:
            self.parent[second_root] = first_root
        else:
            self.parent[second_root] = first_root
            self.rank[first_root] += 1

        return True


class KruskalSignalOptimizer:
    """Applies Kruskal's greedy strategy to assign signal priority and green time."""

    MIN_GREEN_TIME = 10
    MAX_GREEN_TIME = 60
    VEHICLES_PER_GREEN_SLOT = 2
    AVG_WAIT_PER_VEHICLE = 4

    def optimize(self, roads: list[Road]) -> tuple[list[SignalPlan], int]:
        """
        Kruskal algorithm steps:
        1. Treat each road as a weighted graph edge.
        2. Sort roads in descending order based on vehicle count.
        3. Select the highest-weight road if it does not create a cycle.
        4. Repeat until a maximum spanning tree is formed.
        5. Allocate signal priority and green time using the selected edge order.
        """

        if not roads:
            return [], 0

        selected_roads = self._build_maximum_spanning_tree(roads)
        signal_plans: list[SignalPlan] = []

        # Before optimization, assume every road receives a fixed average signal.
        fixed_green_time = 25
        total_wait_before = 0
        total_wait_after = 0

        for priority, road in enumerate(selected_roads, start=1):
            # More vehicles means more green time. The value is capped so that
            # no road blocks the intersection for too long.
            calculated_time = self.MIN_GREEN_TIME + (
                road.vehicle_count // self.VEHICLES_PER_GREEN_SLOT
            )
            green_time = min(self.MAX_GREEN_TIME, max(self.MIN_GREEN_TIME, calculated_time))

            # Waiting time model for demonstration:
            # More green time reduces waiting pressure on busy roads.
            waiting_before = road.vehicle_count * self.AVG_WAIT_PER_VEHICLE
            service_gain = max(1, green_time - fixed_green_time)
            waiting_after = max(0, waiting_before - service_gain * priority)

            total_wait_before += waiting_before
            total_wait_after += waiting_after

            signal_plans.append(
                SignalPlan(
                    priority=priority,
                    road_name=road.name,
                    vehicle_count=road.vehicle_count,
                    green_time=green_time,
                    waiting_time_before=waiting_before,
                    waiting_time_after=waiting_after,
                )
            )

        waiting_time_reduced = max(0, total_wait_before - total_wait_after)
        return signal_plans, waiting_time_reduced

    def _build_maximum_spanning_tree(self, roads: list[Road]) -> list[Road]:
        """Build a Kruskal maximum spanning tree from traffic-weighted roads."""

        nodes = {road.source for road in roads} | {road.destination for road in roads}
        disjoint_set = DisjointSet(nodes)
        sorted_roads = sorted(roads, key=lambda road: road.vehicle_count, reverse=True)
        selected_roads: list[Road] = []

        for road in sorted_roads:
            if disjoint_set.union(road.source, road.destination):
                selected_roads.append(road)

        return selected_roads


class TrafficSignalApp:
    """Tkinter GUI for entering traffic data and viewing optimized results."""

    KRUSKAL_C_CODE = r"""#include <stdio.h>
#include <stdlib.h>

struct Edge
{
    int src, dest, weight;
};

int findParent(int parent[], int node)
{
    if (parent[node] == node)
        return node;

    return findParent(parent, parent[node]);
}

void unionSet(int parent[], int u, int v)
{
    int uParent = findParent(parent, u);
    int vParent = findParent(parent, v);

    parent[uParent] = vParent;
}

void sortEdges(struct Edge edge[], int edges)
{
    int i, j;
    struct Edge temp;

    for (i = 0; i < edges - 1; i++)
    {
        for (j = 0; j < edges - i - 1; j++)
        {
            if (edge[j].weight > edge[j + 1].weight)
            {
                temp = edge[j];
                edge[j] = edge[j + 1];
                edge[j + 1] = temp;
            }
        }
    }
}

int main()
{
    int vertices, edges;

    printf("Enter number of vertices: ");
    scanf("%d", &vertices);

    printf("Enter number of edges: ");
    scanf("%d", &edges);

    struct Edge edge[edges];

    int i;

    printf("Enter source destination weight:\n");

    for (i = 0; i < edges; i++)
    {
        scanf("%d %d %d", &edge[i].src, &edge[i].dest, &edge[i].weight);
    }

    sortEdges(edge, edges);

    int parent[vertices];

    for (i = 0; i < vertices; i++)
    {
        parent[i] = i;
    }

    int minCost = 0;
    int count = 0;

    printf("\nEdges in Minimum Spanning Tree:\n");

    for (i = 0; i < edges && count < vertices - 1; i++)
    {
        int u = edge[i].src;
        int v = edge[i].dest;
        int w = edge[i].weight;

        if (findParent(parent, u) != findParent(parent, v))
        {
            printf("%d - %d = %d\n", u, v, w);

            minCost += w;

            unionSet(parent, u, v);

            count++;
        }
    }

    printf("\nMinimum Cost = %d\n", minCost);

    return 0;
}"""

    SAMPLE_DATA = {
        "North Road": 45,
        "East Road": 28,
        "South Road": 60,
        "West Road": 18,
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart Traffic Signal Optimization - Kruskal Algorithm")
        self.root.geometry("1080x720")
        self.root.minsize(980, 650)

        self.graph = TrafficGraph()
        self.optimizer = KruskalSignalOptimizer()
        self.road_entries: dict[str, tk.Entry] = {}
        self.current_signal_plans: list[SignalPlan] = []

        self.colors = {
            "background": "#f7f8fb",
            "panel": "#ffffff",
            "text": "#222831",
            "muted": "#667085",
            "accent": "#1f7a8c",
            "green": "#2eaf5d",
            "yellow": "#f0b429",
            "red": "#d64545",
            "road": "#3d4852",
        }

        self._configure_style()
        self._build_layout()
        self.load_sample_data()

    def _configure_style(self) -> None:
        """Create a clean, readable theme for the presentation GUI."""

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["background"])
        style.configure("Panel.TFrame", background=self.colors["panel"])
        style.configure(
            "Title.TLabel",
            background=self.colors["background"],
            foreground=self.colors["text"],
            font=("Arial", 20, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.colors["background"],
            foreground=self.colors["muted"],
            font=("Arial", 11),
        )
        style.configure(
            "PanelTitle.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Arial", 13, "bold"),
        )
        style.configure(
            "Info.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["muted"],
            font=("Arial", 10),
        )
        style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _build_layout(self) -> None:
        """Build input controls, visual simulation area, and result table."""

        main = ttk.Frame(self.root, padding=18)
        main.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            main,
            text="Smart Traffic Signal Optimization Using Kruskal Algorithm",
            style="Title.TLabel",
        )
        title.pack(anchor=tk.W)

        subtitle = ttk.Label(
            main,
            text="VTU 5th Semester ADA Mini Project | Maximum spanning tree using Kruskal's greedy algorithm",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor=tk.W, pady=(3, 14))

        content = ttk.Frame(main)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self._build_input_panel(content)
        self._build_result_panel(content)

    def _build_input_panel(self, parent: ttk.Frame) -> None:
        """Create road input fields and action buttons."""

        input_panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(input_panel, text="Vehicle Count Input", style="PanelTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            input_panel,
            text="Enter vehicles waiting on each road connected to the intersection.",
            style="Info.TLabel",
        ).pack(anchor=tk.W, pady=(4, 16))

        for road_name in self.SAMPLE_DATA:
            row = ttk.Frame(input_panel, style="Panel.TFrame")
            row.pack(fill=tk.X, pady=6)

            label = ttk.Label(row, text=road_name, style="Info.TLabel", width=14)
            label.pack(side=tk.LEFT)

            entry = ttk.Entry(row, font=("Arial", 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
            self.road_entries[road_name] = entry

        button_frame = ttk.Frame(input_panel, style="Panel.TFrame")
        button_frame.pack(fill=tk.X, pady=(18, 12))

        optimize_button = ttk.Button(
            button_frame,
            text="Start Optimization",
            command=self.start_optimization,
        )
        optimize_button.pack(fill=tk.X, pady=4)

        sample_button = ttk.Button(
            button_frame,
            text="Load Sample Traffic Data",
            command=self.load_sample_data,
        )
        sample_button.pack(fill=tk.X, pady=4)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_inputs)
        clear_button.pack(fill=tk.X, pady=4)

        ttk.Label(input_panel, text="Real-time Result", style="PanelTitle.TLabel").pack(
            anchor=tk.W, pady=(16, 6)
        )
        self.summary_label = ttk.Label(
            input_panel,
            text="Enter vehicle counts and start optimization.",
            style="Info.TLabel",
            wraplength=280,
            justify=tk.LEFT,
        )
        self.summary_label.pack(anchor=tk.W)

        self.priority_label = ttk.Label(
            input_panel,
            text="Priority road: -",
            style="Info.TLabel",
            wraplength=280,
            justify=tk.LEFT,
        )
        self.priority_label.pack(anchor=tk.W, pady=(8, 0))

    def _build_result_panel(self, parent: ttk.Frame) -> None:
        """Create the simulation canvas and signal allocation table."""

        result_panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        result_panel.grid(row=0, column=1, sticky="nsew")
        result_panel.rowconfigure(1, weight=1)
        result_panel.columnconfigure(0, weight=1)

        result_header = ttk.Frame(result_panel, style="Panel.TFrame")
        result_header.grid(row=0, column=0, sticky="ew")
        result_header.columnconfigure(0, weight=1)

        ttk.Label(
            result_header,
            text="Traffic Intersection Simulation",
            style="PanelTitle.TLabel",
        ).grid(row=0, column=0, sticky=tk.W)

        self.code_toggle_button = ttk.Button(
            result_header,
            text="Show Kruskal C Code",
            command=self.toggle_source_code,
        )
        self.code_toggle_button.grid(row=0, column=1, sticky=tk.E)

        self.canvas = tk.Canvas(
            result_panel,
            height=320,
            background="#eef3f6",
            highlightthickness=1,
            highlightbackground="#d0d7de",
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=(10, 14))

        ttk.Label(result_panel, text="Signal Allocation Table", style="PanelTitle.TLabel").grid(
            row=2, column=0, sticky=tk.W
        )

        columns = ("priority", "road", "vehicles", "green_time", "wait_before", "wait_after")
        self.result_table = ttk.Treeview(
            result_panel,
            columns=columns,
            show="headings",
            height=8,
        )

        headings = {
            "priority": "Priority",
            "road": "Road",
            "vehicles": "Vehicles",
            "green_time": "Green Time (sec)",
            "wait_before": "Wait Before",
            "wait_after": "Wait After",
        }
        widths = {
            "priority": 75,
            "road": 130,
            "vehicles": 90,
            "green_time": 130,
            "wait_before": 110,
            "wait_after": 100,
        }

        for column in columns:
            self.result_table.heading(column, text=headings[column])
            self.result_table.column(column, width=widths[column], anchor=tk.CENTER)

        self.result_table.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        self._build_source_code_panel(result_panel)
        self._draw_intersection()

    def _build_source_code_panel(self, parent: ttk.Frame) -> None:
        """Create a hidden source-code viewer for the C implementation."""

        self.source_code_frame = ttk.Frame(parent, style="Panel.TFrame")

        header = ttk.Label(
            self.source_code_frame,
            text="Kruskal MST C Program",
            style="PanelTitle.TLabel",
        )
        header.pack(anchor=tk.W, pady=(14, 8))

        code_container = ttk.Frame(self.source_code_frame, style="Panel.TFrame")
        code_container.pack(fill=tk.BOTH, expand=True)

        code_scrollbar = ttk.Scrollbar(code_container, orient=tk.VERTICAL)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.source_code_text = tk.Text(
            code_container,
            height=14,
            wrap=tk.NONE,
            font=("Courier New", 10),
            background="#111827",
            foreground="#e5e7eb",
            insertbackground="#e5e7eb",
            relief=tk.FLAT,
            padx=12,
            pady=10,
            yscrollcommand=code_scrollbar.set,
        )
        self.source_code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        code_scrollbar.config(command=self.source_code_text.yview)

        self.source_code_text.insert("1.0", self.KRUSKAL_C_CODE)
        self.source_code_text.config(state=tk.DISABLED)

    def toggle_source_code(self) -> None:
        """Show or hide the full C source-code panel."""

        if self.source_code_frame.winfo_ismapped():
            self.source_code_frame.grid_remove()
            self.code_toggle_button.config(text="Show Kruskal C Code")
        else:
            self.source_code_frame.grid(row=4, column=0, sticky="nsew")
            self.code_toggle_button.config(text="Hide Kruskal C Code")

    def load_sample_data(self) -> None:
        """Fill input boxes with sample traffic values for quick testing."""

        for road_name, count in self.SAMPLE_DATA.items():
            self.road_entries[road_name].delete(0, tk.END)
            self.road_entries[road_name].insert(0, str(count))

    def clear_inputs(self) -> None:
        """Clear all inputs and reset the displayed simulation."""

        for entry in self.road_entries.values():
            entry.delete(0, tk.END)

        self.current_signal_plans = []
        self.summary_label.config(text="Enter vehicle counts and start optimization.")
        self.priority_label.config(text="Priority road: -")
        self._clear_table()
        self._draw_intersection()

    def start_optimization(self) -> None:
        """Read inputs, validate them, run Kruskal optimization, and show results."""

        try:
            roads = self._read_roads_from_inputs()
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
            return

        self.graph.clear()
        for road in roads:
            self.graph.add_road(
                road.name,
                road.source,
                road.destination,
                road.vehicle_count,
            )

        self.current_signal_plans, waiting_time_reduced = self.optimizer.optimize(
            self.graph.roads
        )

        self._update_result_table()
        self._draw_intersection()
        self._update_summary(waiting_time_reduced)

    def _read_roads_from_inputs(self) -> list[Road]:
        """Validate vehicle counts and convert them into weighted graph edges."""

        roads: list[Road] = []
        for road_name, entry in self.road_entries.items():
            raw_value = entry.get().strip()

            if raw_value == "":
                raise ValueError(f"Vehicle count for {road_name} cannot be empty.")

            if not raw_value.isdigit():
                raise ValueError(f"Vehicle count for {road_name} must be a non-negative integer.")

            vehicle_count = int(raw_value)
            if vehicle_count > 500:
                raise ValueError(f"Vehicle count for {road_name} is too high for this demo.")

            roads.append(
                Road(
                    name=road_name,
                    source=road_name.replace(" Road", " Entry"),
                    destination="Main Intersection",
                    vehicle_count=vehicle_count,
                )
            )

        if all(road.vehicle_count == 0 for road in roads):
            raise ValueError("At least one road must have vehicles waiting.")

        return roads

    def _clear_table(self) -> None:
        """Remove previous rows from the result table."""

        for item in self.result_table.get_children():
            self.result_table.delete(item)

    def _update_result_table(self) -> None:
        """Display priority order and green signal timing in tabular form."""

        self._clear_table()
        for plan in self.current_signal_plans:
            self.result_table.insert(
                "",
                tk.END,
                values=(
                    plan.priority,
                    plan.road_name,
                    plan.vehicle_count,
                    plan.green_time,
                    plan.waiting_time_before,
                    plan.waiting_time_after,
                ),
            )

    def _update_summary(self, waiting_time_reduced: int) -> None:
        """Show Kruskal's selected road order and total waiting time reduction."""

        if not self.current_signal_plans:
            return

        priority_order = " -> ".join(plan.road_name for plan in self.current_signal_plans)
        top_plan = self.current_signal_plans[0]

        self.summary_label.config(
            text=(
                f"Kruskal MST order: {priority_order}\n"
                f"Total waiting time reduced: {waiting_time_reduced} seconds"
            )
        )
        self.priority_label.config(
            text=(
                f"Priority road: {top_plan.road_name} "
                f"({top_plan.vehicle_count} vehicles, {top_plan.green_time} sec green)"
            )
        )

    def _draw_intersection(self) -> None:
        """Draw a visual traffic-flow indicator for the four-road intersection."""

        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 760)
        height = max(self.canvas.winfo_height(), 320)
        center_x = width // 2
        center_y = height // 2

        # Draw horizontal and vertical roads.
        self.canvas.create_rectangle(0, center_y - 42, width, center_y + 42, fill=self.colors["road"], outline="")
        self.canvas.create_rectangle(center_x - 42, 0, center_x + 42, height, fill=self.colors["road"], outline="")
        self.canvas.create_oval(
            center_x - 48,
            center_y - 48,
            center_x + 48,
            center_y + 48,
            fill="#222831",
            outline="#ffffff",
            width=2,
        )
        self.canvas.create_text(
            center_x,
            center_y,
            text="INTERSECTION",
            fill="#ffffff",
            font=("Arial", 9, "bold"),
        )

        road_positions = {
            "North Road": (center_x, 42, center_x, center_y - 70, "vertical"),
            "East Road": (width - 90, center_y, center_x + 70, center_y, "horizontal"),
            "South Road": (center_x, height - 42, center_x, center_y + 70, "vertical"),
            "West Road": (90, center_y, center_x - 70, center_y, "horizontal"),
        }

        plan_by_road = {plan.road_name: plan for plan in self.current_signal_plans}

        for road_name, (label_x, label_y, signal_x, signal_y, direction) in road_positions.items():
            plan = plan_by_road.get(road_name)
            vehicle_count = plan.vehicle_count if plan else self._safe_entry_value(road_name)
            is_priority = plan is not None and plan.priority == 1
            signal_color = self.colors["green"] if is_priority else self.colors["red"]

            self._draw_signal_light(signal_x, signal_y, signal_color)
            self._draw_vehicle_bar(label_x, label_y, vehicle_count, direction, is_priority)

            label_text = road_name
            if plan:
                label_text = f"{road_name}\nP{plan.priority} | {plan.green_time}s"

            self.canvas.create_text(
                label_x,
                label_y,
                text=label_text,
                fill=self.colors["text"],
                font=("Arial", 10, "bold"),
                justify=tk.CENTER,
            )

    def _draw_signal_light(self, x: int, y: int, color: str) -> None:
        """Draw one signal indicator near the intersection."""

        self.canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill=color, outline="#ffffff", width=2)

    def _draw_vehicle_bar(
        self,
        label_x: int,
        label_y: int,
        vehicle_count: int,
        direction: str,
        is_priority: bool,
    ) -> None:
        """Draw simple vehicle-density bars beside each road."""

        bar_length = min(120, 20 + vehicle_count * 2)
        bar_color = self.colors["green"] if is_priority else self.colors["yellow"]

        if direction == "vertical":
            x1 = label_x + 58
            y1 = label_y - bar_length // 2
            x2 = label_x + 72
            y2 = label_y + bar_length // 2
        else:
            x1 = label_x - bar_length // 2
            y1 = label_y + 34
            x2 = label_x + bar_length // 2
            y2 = label_y + 48

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bar_color, outline="")
        self.canvas.create_text(
            (x1 + x2) // 2,
            y2 + 13 if direction == "horizontal" else (y1 + y2) // 2,
            text=f"{vehicle_count}",
            fill=self.colors["text"],
            font=("Arial", 9, "bold"),
        )

    def _safe_entry_value(self, road_name: str) -> int:
        """Return a valid integer from an entry box, or zero while editing."""

        value = self.road_entries[road_name].get().strip()
        return int(value) if value.isdigit() else 0


def main() -> None:
    """Start the Tkinter application."""

    root = tk.Tk()
    app = TrafficSignalApp(root)

    # Redraw after Tkinter calculates the final canvas size.
    root.after(100, app._draw_intersection)
    root.mainloop()


if __name__ == "__main__":
    main()
