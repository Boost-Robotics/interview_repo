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

---


### Maniskill Exercise

**Duration:** 90 minutes + 120 minutes  
**Task:** ManiSkill Peg Insertion Behavior Cloning Ablation Study

#### Objective

Using pre-recorded demonstrations and existing training scripts, run a controlled ablation study on the ManiSkill **PegInsertionSide-v1** task.

You should compare:

- ACT vs Diffusion Policy vs Vanilla BC vs RLPD (if time permits) 
- Action space variants
- Observation space variants

Try to get through as much as you can. The goal is to test hypotheses you may have about behavior cloning and understand how different modeling and environment choices affect performance.

If the task seems too difficult to complete in the time given, please let us know sooner rather than later.

---

#### Questions to Answer

Please be prepared to discuss:

1. What is the difference between **ACT**, **Diffusion Policy**, **Vanilla BC**, and **RLPD**?
2. Should we expect performance differences between these approaches on the peg-in-hole task?
3. How do action space choices affect learning and evaluation?
4. How do observation space choices affect performance?
5. What ablations did you run, and what conclusions can you draw from them?
6. What would you try next if you had more time?

---

#### Useful Links

- ManiSkill documentation: https://maniskill.readthedocs.io/en/latest/index.html
- ManiSkill GitHub repository: https://github.com/haosulab/ManiSkill
- Learning from demonstrations setup: https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html

---

#### Download Demonstrations

Follow the ManiSkill instructions for downloading demonstration data:

https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html

You should end up with demonstration trajectories under a path similar to:

```bash
~/.maniskill/demos/PegInsertionSide-v1/motionplanning/
```

Set the demonstration path if needed:

```bash
export DEMO_PATH=~/.maniskill/demos
```

---

#### Replay Demonstrations into an Easier Action / State Space

Before training, replay the demonstrations into a more convenient control and observation format.

```bash
python -m mani_skill.trajectory.replay_trajectory \
  --traj-path ${DEMO_PATH}/PegInsertionSide-v1/motionplanning/trajectory.h5 \
  --use-first-env-state \
  -c pd_ee_delta_pose \
  -o state \
  --save-traj \
  --num-envs 10 \
  -b physx_cpu
```

This should produce a replayed trajectory file using:

- **Control mode:** `pd_ee_delta_pose`
- **Observation mode:** `state`
- **Backend:** `physx_cpu`

---

#### Train a Policy

Navigate to the ACT baseline directory:

```bash
cd ~/projects/maniskill_ws/ManikSkill/examples/baselines/act
```

Train a policy:

```bash
python train.py \
  --env-id PegInsertionSide-v1 \
  --demo-path ~/.maniskill/demos/PegInsertionSide-v1/motionplanning/trajectory.state.pd_ee_delta_pose.physx_cpu.h5 \
  --control-mode "pd_ee_delta_pose" \
  --sim-backend "physx_cpu" \
  --num_demos $demos \
  --max_episode_steps 200 \
  --total_iters 10000 \
  --log_freq 100 \
  --eval_freq 5000 \
  --exp-name act-PegInsertionSide-v1-state-${demos}_motionplanning_demos-$seed \
  --track
```
  
#### General Questions to consider:

- Which policy performs best with limited demonstrations?
- Which one is easiest to train?
- Which one is most stable across seeds?
- Which one handles multimodal demonstrations better?
 
#### 2. Action Space Variants

Try different control modes, such as:

```bash
pd_ee_delta_pose
pd_ee_pose
pd_joint_delta_pos
pd_joint_pos
```

Questions to consider:

- Does end-effector control make the task easier than joint-space control?
- Does delta control help compared to absolute control?
- Which action space produces smoother rollouts?
- Which action space is most sensitive to compounding errors?

---

#### 3. Observation Space Variants

Try different observation modes, such as:

```bash
state
rgb
rgbd
pointcloud
```

Questions to consider:

- Is low-dimensional state enough for this task?
- Does vision make the task harder or more realistic?
- How much does observation space affect sample efficiency?
- Are failures due to perception or control?

---

## Notes

This challenge is intentionally open-ended. We care more about your reasoning, experimental judgment, and debugging process than completing every ablation.

Use your time to run the most informative experiments first.

Don't hesitate to ask questions if anything is unclear. Good luck!








