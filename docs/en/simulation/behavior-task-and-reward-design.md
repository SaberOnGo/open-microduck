# Behavior, Task, and Reward Design

[English] | [简体中文](../../zh-CN/simulation/behavior-task-and-reward-design.md)

This page explains the work that happens **before or around reinforcement-learning training** when adding a new robot action.

## What is this work called?

The broadest useful name is **Behavior / Task Design**.

It usually contains three parts:

- **Behavior / Task Design** — define what the robot should do and what counts as success.
- **Reward Design** — turn that goal into numerical scores and penalties that the RL algorithm can optimize.
- **Curriculum Design** — for difficult actions, split the problem into easier stages or starting conditions.

PPO is the learning algorithm. These design steps define **what PPO is asked to learn**.

## Simple example: stand on one leg

Human goal:

> Raise the right foot, balance on the left foot, stay upright, and do not flail.

The training task may score it like this:

```text
right foot off the floor      reward
body stays upright            reward
left foot stays planted       reward
stance foot stays flat        reward
body thrashes or drifts       penalty
joints move violently         penalty
robot falls                   end episode / failure
```

The exact weights are experiments, not universal constants. A reward can also be wrong even when the code is correct: if the scoring rule misses something important, the policy may discover an ugly shortcut that still earns points.

The public `microduck-lab` project documents this directly. Its one-leg behavior combines positive terms for one-foot balance, foot height, stance-foot contact and posture with penalties for body motion, drift, jerky actions, high joint speed and motor effort.

## Adding a completely new action

A practical workflow is:

1. **Describe the action in plain language.**
   Example: “crouch, jump forward, land on both feet, then recover to standing.”

2. **Define success that can be measured in simulation.**
   Examples: body height, foot contacts, forward displacement, orientation, joint state, landing stability.

3. **Check that the policy can observe enough information to learn it.**
   A reward should not depend on hidden information that the policy cannot infer from its observations. `microduck-lab` explicitly warns against rewarding unobservable state.

4. **Create the first reward recipe.**
   Reward the important outcomes and penalize obvious failure modes. Prefer several understandable terms over one vague “good action” score.

5. **Run a short training experiment.**
   Do not start with the longest or most expensive run. The first goal is to see whether the desired motion appears at all.

6. **Watch the actual rollout, not only the reward chart.**
   Check whether the robot learned the intended action or found a scoring loophole.

7. **Fix the task definition, then train again.**
   If the robot succeeds in the wrong way, adjust reward terms or measurable targets. If it never discovers the required motion, reward tuning alone may not help.

8. **Add a curriculum for hard actions.**
   Start closer to the goal, simplify initial conditions, or train easier stages first, then progressively return to the real task. `microduck-lab` uses staged curricula for difficult behaviors.

9. **Verify the deterministic exported policy.**
   Export the policy, evaluate it without training noise, and inspect the resulting motion.

10. **Only then move to final sim-to-real training.**
    `microduck-lab` describes itself as a fast prototyping environment. Final robot-ready policies should be retrained with the full upstream `microduck_rl` sim-to-real setup and domain randomization.

## Where Codex or another coding agent can help

A coding agent can handle much of this loop:

```text
plain-language action request
        ↓
inspect existing behaviors and observations
        ↓
draft reward / curriculum code
        ↓
run tests
        ↓
launch short training
        ↓
render rollout
        ↓
inspect failure mode
        ↓
revise task and repeat
```

Human review is still important because “high reward” is not the same as “the motion looks correct.”

## Rule of thumb

When a new action fails, ask these questions in order:

1. **Can the policy observe what it needs?**
2. **Does any rollout ever perform part of the desired action?**
3. **Does the reward actually pay for the behavior humans want?**
4. **Is the policy exploiting a shortcut?**
5. **Does the task need a curriculum instead of more training steps?**

This ordering prevents many wasted training runs.

## Public sources

- Jonathan Hawkins, `microduck-lab`: <https://github.com/jonathanhawkins/microduck-lab>
- `microduck-lab` training playbook: <https://github.com/jonathanhawkins/microduck-lab/blob/main/microduck_local/AGENTS.md>
- Pollen Robotics, `microduck_rl`: <https://github.com/pollen-robotics/microduck_rl>

Source level: **public upstream repositories and public third-party implementation notes**. This page summarizes their openly documented training workflow; it does not claim that third-party `microduck-lab` behavior recipes are official Pollen Robotics recipes.
