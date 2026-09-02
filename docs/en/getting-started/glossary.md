# Beginner Glossary: Training in Plain Language

**English** | [简体中文](../../zh-CN/getting-started/glossary.md)

> Do not memorize the vocabulary. First understand each term's job in the workflow.

## The whole loop

```text
During training
numbers the robot sees (Observation)
        ↓
the Policy produces an Action
        ↓
the simulator computes what happens
        ↓
Reward tells the training algorithm whether that direction helped
        ↓
repeat, save a Checkpoint, and export ONNX

At runtime
real/virtual robot state → ONNX Policy → 14 joint actions
```

## Core terms

| Term | Plain-language meaning | In Microduck | Common misunderstanding |
|---|---|---|---|
| **Simulation** | Software computes the robot's motion and contacts | MuJoCo runs a virtual Microduck | A good animation is not real-hardware proof |
| **Policy** | A function that chooses the next action from the current state | 61 inputs become 14 actions | It is not the whole robot AI stack |
| **Observation** | Numbers available to the policy each cycle | IMU, joints, last action, commands, and more | The standard walking policy does not read camera images directly |
| **Action** | The policy's next control target | Targets for 14 policy joints | The runtime also has a fifteenth mouth/beak motor |
| **Reward** | A training-time score | Rewards direction tracking and staying upright | Exported ONNX does not keep reading rewards |
| **PPO** | An algorithm that updates a policy from practice | The RL algorithm used upstream | PPO controls how to learn; task design controls what to learn |
| **Checkpoint** | A saved training state | Network and training progress at one moment | It is not automatically a deployable ONNX file |
| **ONNX** | A portable model-file format | The runtime loads movement policies | Correct export must preserve input normalization |
| **Inference** | Running a trained model | The policy runs every 20 ms | Inference is not retraining and usually needs much less compute |
| **Domain randomization** | Deliberately vary simulation parameters during training | Varies friction, voltage, delay, and more | It is controlled and versioned, not arbitrary noise |
| **Sim-to-real** | Transfer a simulation-trained behavior to hardware | ONNX moves from MuJoCo into the runtime | Simulation success is only the first half |
| **Daemon** | A small Linux program that stays running in the background | `robotd` owns motion; `updaterd` owns updates | A daemon is a software role, not another AI model |
| **BAM** | A higher-fidelity actuator model for non-ideal servo behavior | Represents XL330 voltage, back-EMF, friction, and more | Code parameters are not automatically manufacturer ratings |
| **Backlash** | Free play when a gear train changes direction | Upstream provides backlash task variants | It is more than random angle noise |

## Three statements that are not interchangeable

1. **“I ran it.”** You loaded an ONNX policy trained by someone else.
2. **“I trained it.”** Your training result passed simulation and export checks.
3. **“I completed sim-to-real.”** You also recorded real-hardware test conditions and results.

## What to read next

- [Choose Your Path](choose-your-path.md)
- [Simulation First](simulation-first.md)
- [Behavior, Task, and Reward Design](../simulation/behavior-task-and-reward-design.md)
- [Reproducible Training and ONNX Export](../simulation/reproducible-training-and-export.md)
