# Interview Repo

Welcome! This is a starter Python repository for your interview exercise.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repo-url>
   cd interview_repo
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Linux/macOS
   # venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```



## Project Structure

```
interview_repo/
├── maniskill/           # Maniskill Exercise
├── grocery_robot/       # Grocery Robot Exercise
│   └── main.py          # Entry point – start here!
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

## Exercises

### Grocery Robot Exercise

1. **Run the starter script**:
   ```bash
   python grocery_robot/main.py
   ```

#### Software–Hardware Hackathon (120 minutes)

**You should assume:**
- An xArm6 with a gripper
- A fixed RGB or RGB-D camera observing the workspace
- Some existing code (Python/C++), which may be rough or brittle

**You are encouraged to:**
- Read and understand the existing code
- Ask questions or request help with implementation
- Critique assumptions and design decisions

**Your task:** Extend the starter code by implementing a simple perception → grasp → place pipeline for one of the fruits on the table. Once you have a basic pipeline working, choose one or two areas to improve.

**Possible improvement areas:**

- **Perception:**
  - Hand–eye calibration between the robot/gripper and camera
  - Confidence estimation or failure detection
  - Fruit detection (color, depth, geometry, heuristics)
  - Pose estimation of the fruit

- **Control & Execution:**
  - Grasp pose selection
  - Improved motion smoothness
  - Preventing fruit damage (grip force control)
  - Obstacle avoidance

### Maniskill Exercise



Don't hesitate to ask questions if anything is unclear. Good luck!








