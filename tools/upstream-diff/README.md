# Upstream Parameter Diff Tool

This small tool turns selected **public upstream source parameters** into JSON so two revisions can be compared without manually rereading every file.

It does **not** download anything and does **not** infer a production BOM.

## English

### What it extracts

From a local `pollen-robotics/microduck` checkout:

- Dynamixel joint IDs;
- home pose values;
- IMU bridge ID;
- baud rate;
- battery operating-map values;
- startup register expectations;
- parsed `deploy/robotd.toml` configuration;
- source-file hashes.

From a local `pollen-robotics/microduck_rl` checkout:

- `robot_allcollisions.xml` joint names, axes and ranges;
- inertial body masses / CoM / inertia values;
- total model inertial mass;
- mesh instance counts;
- source-file hash.

### Create a snapshot

```bash
python tools/upstream-diff/extract_microduck.py snapshot \
  --microduck ../microduck \
  --microduck-rl ../microduck_rl \
  --out snapshot-old.json
```

Check out another upstream revision, then create another snapshot:

```bash
python tools/upstream-diff/extract_microduck.py snapshot \
  --microduck ../microduck \
  --microduck-rl ../microduck_rl \
  --out snapshot-new.json
```

### Compare snapshots

```bash
python tools/upstream-diff/extract_microduck.py diff snapshot-old.json snapshot-new.json
```

The command prints changed JSON paths with `before` and `after` values.

A non-empty diff exits with status `1`, so it can later be used in CI.

### Evidence rule

A changed source parameter means only:

> the public upstream source changed between these two revisions.

It does **not** automatically mean the final production hardware changed.

---

## 简体中文

这个工具用于把官方公开源码里的部分关键参数自动提取成 JSON，然后比较两个版本。

它的目的不是自动“猜 BOM”，而是解决一个很实际的问题：

> 官方仓库更新以后，Joint Range、Home Pose、Mass、Runtime Config 到底哪里变了？

### 当前会自动提取

从本地 `microduck`：

- Servo ID；
- Home Pose；
- IMU Bridge ID；
- Baud Rate；
- Battery Runtime Mapping；
- Startup Register；
- `deploy/robotd.toml`；
- 源文件 SHA256。

从本地 `microduck_rl`：

- `robot_allcollisions.xml` Joint / Axis / Range；
- Body Mass / CoM / Inertia；
- Simulation Model 总惯性质量；
- Mesh Instance Count；
- 源文件 SHA256。

### 生成参数快照

```bash
python tools/upstream-diff/extract_microduck.py snapshot \
  --microduck ../microduck \
  --microduck-rl ../microduck_rl \
  --out snapshot-old.json
```

切换到另一个官方 commit 后，再生成一次：

```bash
python tools/upstream-diff/extract_microduck.py snapshot \
  --microduck ../microduck \
  --microduck-rl ../microduck_rl \
  --out snapshot-new.json
```

### 比较

```bash
python tools/upstream-diff/extract_microduck.py diff snapshot-old.json snapshot-new.json
```

如果有变化，会输出：

```text
哪个参数路径变了
before 是什么
new 是什么
```

有差异时程序返回 exit code `1`，以后可以接 CI 自动提醒。

### 证据边界

工具发现“源码参数变化”，只代表：

> **两个官方公开源码 revision 不一样。**

不能自动写成：

> “量产 Microduck 硬件一定改版了。”

仍然要结合产品资料、官方说明和证据等级判断。
