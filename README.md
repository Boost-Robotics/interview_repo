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


#### Software–Hardware Hackathon (110 minutes)

**You should assume:**
- An xArm6 with a gripper
- A fixed RGB or RGB-D camera observing the workspace
- Some existing code (Python/C++), which may be rough or brittle

**You are encouraged to:**
- Read and understand the existing code
- Ask questions or request help with implementation
- Critique assumptions and design decisions

**Your task:** Extend the starter code by implementing a simple perception → grasp → place pipeline for one of the fruits on the table. Once you have a basic pipeline working, choose one or two areas to improve.

1. **Run the starter script**:
   ```bash
   python grocery_robot/main.py
   ```
   
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

Behavior Cloning Challenge (90 mins + 120 mins)
Objective
Using pre-recorded demonstrations and existing training scripts, run a controlled ablation study on ManiSkill peg insertion:
ACT vs Diffusion Policy
Action space variants
Observation space variants
Try to get through as much as you can. The goal of this is to test some hypotheses that you may have about behavior cloning. If this seems too difficult in the time given, please let us know sooner rather than later.
Some questions to answer:
What is the difference between ACT vs Diffusion Policy vs Vanilla BC? Should we expect performance differences on this peg in hole task? 
Maniskill Docs: https://maniskill.readthedocs.io/en/latest/index.html
Maniskill: https://github.com/haosulab/ManiSkill
Access to GCP: gcloud compute ssh --zone "us-central1-a" "instance-20260226-035150" --project "vocal-affinity-454218-p3"










(my_env) hans@instance-20260226-035150:~/bc_ws$ python -m mani_skill.utils.download_demo PegInsertionSide-v1
Downloading demonstrations to /home/hans/.maniskill/demos - 1/1, PegInsertionSide-v1
29.5Mit [00:01, 19.3Mit/s]                                                                                                                                                       
(my_env) hans@instance-20260226-035150:~/bc_ws$ 


Don't hesitate to ask questions if anything is unclear. Good luck!








