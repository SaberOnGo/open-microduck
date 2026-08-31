# 来源与许可证说明

> 本文是项目维护说明，不构成法律意见。复制、修改或再分发第三方内容前，应检查当时 upstream 的实际 LICENSE / NOTICE 和文件级许可。

## 项目身份

OpenMicroDuck 是独立、非官方的研究项目，与 Pollen Robotics、Hugging Face 不存在隶属、授权、赞助或官方合作关系。

Microduck 名称、商标和相关品牌资产归各自权利人所有。本仓库使用 Microduck 名称是为了标识研究、互操作与文档对象，并不表示官方身份。

## 官方软件

官方 `pollen-robotics/microduck` 仓库当前使用 **Apache License 2.0**：

https://github.com/pollen-robotics/microduck

软件 Apache-2.0 并不自动授予第三方商标权，也不等于未公开的机械/电子设计文件获得开放许可。

## 官方 RL 仓库与 3D 资产

官方 `pollen-robotics/microduck_rl` README 当前声明：

- 软件：**Apache License 2.0**；
- 3D model files：**Creative Commons BY-SA-NC**。

https://github.com/pollen-robotics/microduck_rl

不同资产可能存在文件级、版本级或上游来源差异，因此复制 mesh、转换模型、截图或衍生作品前应重新检查最新许可。

如果具体资产适用 **NC（NonCommercial）** 条款，商业使用限制尤其需要注意。

## Microduck 不是以开源硬件形式发布

官方 Press Kit 明确说明：“open source”针对**软件栈**，并要求不要把机械与电子设计文件描述成开源硬件。

https://pollen-robotics.com/microduck/press-kit/

因此 OpenMicroDuck 明确区分：

- 对公开事实的文档和分析；
- 根据公开信息独立推导的测量/重建；
- 按软件许可证公开的 upstream 软件；
- 受各自资产许可证约束的 3D 模型与衍生作品；
- 未公开的专有制造文件——不属于本仓库内容。

## 社区衍生 CAD / 图片

第三方对公开资产做转换时，衍生结果可能继续受源资产条款约束。

例如 `fanhao375/microduck-replica` 声明其 scripts 为 Apache-2.0，而由上游 Microduck 3D 模型产生的 assembly/CAD 衍生内容为 CC BY-SA-NC 4.0：

https://github.com/fanhao375/microduck-replica

OpenMicroDuck 当前选择**链接并总结**这些研究结果，而不是把其 CAD/图片直接复制进本仓库。

## Attribution

使用 upstream 代码或资产时：

1. 保留许可证要求的版权与 NOTICE；
2. 标注 upstream 项目和来源路径；
3. 不删除许可证要求的 attribution；
4. 不把社区转换文件包装成 Pollen Robotics 官方文件；
5. 能自行绘制说明图/表格时优先自行创作。

## 仓库统一许可证状态

OpenMicroDuck **目前尚未选择 repository-wide license**。项目正在先把原创文档/代码与不同许可的第三方引用清楚分离，因此暂不草率套用统一许可证。

仓库公开并不等于 OpenMicroDuck 原创内容可以不受限制地任意复用。

无论未来 OpenMicroDuck 使用什么许可证，第三方内容仍然适用其原始版权和许可条款。

## 商标与非官方说明

公开页面应保留清晰的非隶属声明，不使用官方 Microduck Logo/视觉体系把本仓库包装得像官方项目。

“Microduck reverse-engineering research”这类描述性使用，与声称自己是官方 Microduck 项目是不同的。

## 私有与保密资料

保密、泄露、非法获得或与本公开项目无关的私有工程资料不属于 OpenMicroDuck 范围，禁止提交。

另见 [研究规范](../research-guidelines.md) 和根目录 [DISCLAIMER.md](../../../DISCLAIMER.md)。
