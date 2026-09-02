# 我有官方 Microduck：普通用户从哪里开始

[English](../../en/getting-started/official-robot-owner.md) | **简体中文**

> 这页面向购买官方 Microduck 的用户。它不是研究样机的装配或首次通电教程。

## 先分清两条路线

| 你的情况 | 应该看什么 |
|---|---|
| 购买了官方 Microduck，想开机、配手柄、检查状态或更新 | 本页和官方 `docs/robot/` 用户文档 |
| 自己制作控制板、线束、机械件或完整研究样机 | [硬件 Bring-up 与标定](hardware-bringup-and-calibration.md) |

不要把研究样机的串口、舵机 EEPROM、初始化或开发板 Provisioning 步骤直接套到客户机器人上。

## 推荐的第一次操作顺序

1. 阅读官方 [Robot Cheat Sheet](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/cheatsheet.md)。
2. 按官方 [手柄配对说明](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/pair-a-gamepad.md) 完成一次配对。
3. 在机器人上先运行只读检查：

```bash
robotctl version
robotctl health
robotctl monitor
```

4. 需要从电脑通过蓝牙连接时，阅读官方 [`duckctl` 文档](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/duckctl.md)。
5. 更新、回滚和固定版本只按官方 [Cheat Sheet 的 Updates 章节](https://github.com/pollen-robotics/microduck/blob/main/docs/robot/cheatsheet.md#updates-updaterd) 操作。

OpenMicroDuck 在这里提供中文导航；真实命令和当前行为以官方仓库对应版本为准。

## 两个安全边界

- 官方 Cheat Sheet 明确说明 `relax` 会切断舵机保持力，机器人可能直接倒下。操作前先用手托住或放在安全软垫上。
- 官方 `duckctl` 文档说明浏览器控制台的 `stop` 只是把运动意图归零，**不是切断舵机电源的急停**。

第一次测试应清空周围空间，远离桌边、脸、手指、宠物和易碎物。轮滑和翻滚动作需要更大的安全区域。

## 出问题时先保存什么

提交问题前保存：

- `robotctl version`；
- `robotctl health --json`（公开前检查是否含设备或个人信息）；
- 问题发生前执行的命令；
- 是否刚更新、是否自动回滚；
- 电池、手柄和当前运行模式。

不要公开设备 Secret、私钥、Token、Wi-Fi 密码或包含这些信息的日志。

## 官方来源

- https://github.com/pollen-robotics/microduck
- https://github.com/pollen-robotics/microduck/tree/main/docs/robot
- https://pollen-robotics.com/microduck/
