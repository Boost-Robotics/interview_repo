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

**Duration:** 90 minutes + 120 minutes  
**Task:** ManiSkill Peg Insertion Behavior Cloning Ablation Study

---

#### Objective

Using pre-recorded demonstrations and existing training scripts, run a controlled ablation study on the ManiSkill **PegInsertionSide-v1** task.

You should compare:

- ACT vs Diffusion Policy vs Vanilla BC
- Action space variants
- Observation space variants

Try to get through as much as you can. The goal is to test hypotheses you may have about behavior cloning and understand how different modeling and environment choices affect performance.

If the task seems too difficult to complete in the time given, please let us know sooner rather than later.

---

#### Questions to Answer

Please be prepared to discuss:

1. What is the difference between **ACT**, **Diffusion Policy**, and **Vanilla BC**?
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

#### GCP Access

SSH into the provided GCP instance:

```bash
gcloud compute ssh \
  --zone "us-central1-a" \
  "instance-20260226-035150" \
  --project "vocal-affinity-454218-p3"
```

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

The resulting file should look similar to:

```bash
trajectory.state.pd_ee_delta_pose.physx_cpu.h5
```

Single-line replay command:

```bash
python -m mani_skill.trajectory.replay_trajectory --traj-path ${DEMO_PATH}/PegInsertionSide-v1/motionplanning/trajectory.h5 --use-first-env-state -c pd_ee_delta_pose -o state --save-traj --num-envs 10 -b physx_cpu
```

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

Single-line training command:

```bash
python train.py --env-id PegInsertionSide-v1 --demo-path ~/.maniskill/demos/PegInsertionSide-v1/motionplanning/trajectory.state.pd_ee_delta_pose.physx_cpu.h5 --control-mode "pd_ee_delta_pose" --sim-backend "physx_cpu" --num_demos $demos --max_episode_steps 200 --total_iters 10000 --log_freq 100 --eval_freq 5000 --exp-name=act-PegInsertionSide-v1-state-${demos}_motionplanning_demos-$seed --track
```

---

#### Suggested Ablations

You do not need to complete all of these. Prioritize the ones you think are most informative.

### 1. Policy Architecture

Compare:

| Policy | Notes |
|---|---|
| ACT | Chunked action prediction / sequence modeling |
| Diffusion Policy | Iterative denoising over action trajectories |
| Vanilla BC | Direct supervised action prediction |

Questions to consider:

- Which policy performs best with limited demonstrations?
- Which one is easiest to train?
- Which one is most stable across seeds?
- Which one handles multimodal demonstrations better?

---

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

#### 4. Number of Demonstrations

Try varying the number of demonstrations:

```bash
demos=10
demos=25
demos=50
demos=100
```

Questions to consider:

- How much data is needed before policies begin to succeed?
- Which policy is most data-efficient?
- Does performance saturate?
- Do some policies overfit more than others?

---

#### 5. Random Seeds

If time permits, run multiple seeds:

```bash
seed=0
seed=1
seed=2
```

Questions to consider:

- Are results consistent?
- Are there large differences between seeds?
- How confident are you in the conclusions?

---

#### Suggested Experiment Table

Fill in as much as you can during the challenge.

| Policy | Obs Mode | Control Mode | # Demos | Seed | Success Rate | Notes |
|---|---|---|---:|---:|---:|---|
| ACT | state | pd_ee_delta_pose |  |  |  |  |
| Diffusion Policy | state | pd_ee_delta_pose |  |  |  |  |
| Vanilla BC | state | pd_ee_delta_pose |  |  |  |  |
| ACT | rgb | pd_ee_delta_pose |  |  |  |  |
| ACT | state | pd_joint_delta_pos |  |  |  |  |

---

## Expected Discussion Points

### ACT vs Diffusion Policy vs Vanilla BC

**Vanilla Behavior Cloning** directly predicts the next action from the current observation using supervised learning. It is simple and fast, but can struggle with multimodal action distributions and compounding errors.

**ACT** predicts chunks of future actions rather than a single action at a time. This can improve temporal consistency and reduce action jitter, especially for precise manipulation tasks.

**Diffusion Policy** models an action trajectory through an iterative denoising process. It can represent complex and multimodal action distributions, but is usually more computationally expensive to train and evaluate.

For peg insertion, we may expect performance differences because the task requires precision, contact-rich behavior, and robustness to small errors. Policies that model action sequences may outperform one-step BC, especially if demonstrations contain subtle corrective behaviors.

---

## Deliverables

At the end of the challenge, please share:

1. The commands you ran
2. Any code or config changes you made
3. A table of completed experiments
4. Evaluation results, if available
5. A brief summary of what you learned
6. What you would do next with more time

---

## Notes

This challenge is intentionally open-ended. We care more about your reasoning, experimental judgment, and debugging process than completing every ablation.

Use your time to run the most informative experiments first.


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








