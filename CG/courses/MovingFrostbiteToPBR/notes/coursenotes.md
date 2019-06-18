# 目录

[TOC]

# 1. 导论 Introduction

基于 Killzone Shadow Fall [^Dro13]，Unreal Engine 4 [^Kar13]，Remember Me [^LH13] 和 Metal Gear Solid V: Ground Zeroes [^Koj+13]，Frostbite 转移到 PBR。在此基础上，试图进一步**完善现有的技术**，并逐步**解决该领域的公开问题**。

在适当的近似下，我们更喜欢提升图像质量的**可信度** believability 而不是绝对正确性 absolute correctness。

PBR的核心原则之一就是**材料和灯光信息的解耦** decoupling，这对于确保场景中所有对象之间的视觉**一致性**至关重要，有助于跨环境**重用**资源 assets 和照明设备 lighting rigs，减少了向 artists 公开的参数数量，使创作更加**直观**。

转移到 PBR 需要更新整个图形管线（渲染器和工具）。

记号

![1560865143498](assets/1560865143498.png)

# 2. 参考 Reference

### 2.1 验证模型和假设 Validating models and hypothesis 

**观察并与现实世界进行比较**是做出正确选择并判断一项技术或方法的相关性的最佳方法。

![1560865484659](assets/1560865484659.png)

然而准确测量真实数据很复杂或者需要花费大量时间。特定的数据库如 MERL 可以获取这些数据以帮助快速检验模型。

### 2.2 Validating in-engine approximations

现代的 PBR 路径追踪器如 Mitsuba 实现了先进的渲染技术，可以创建十分真实的画面。Frostbite 中有一个简单的输出器 exporter 用于 Mitsuba，这使我们能够快速评估估算值的有效性。

可以输出几何体 geometry、常量材质信息 constant material information（i.e. 没有纹理 textures）和所有光源 light source。我们可以检验材质模型，光积分和光强。

![1560866112378](assets/1560866112378.png)

### 2.3 Validating in-engine reference mode

为了加速，我们增加了一个引擎内置的参考模式，用 GPU 实现的。渲染时间并不快，但是迭代时间比我们的简单导出器快一个数量级。

> 渲染速度不快。。。。。太尴尬了。。。。。
>
> 好吧迭代速度快点就快点吧，原本也就几秒搞定，快能快到哪去。。。。。

![1560866942375](assets/1560866942375.png)

# 3. 材质 Material



# 4. 光照 Lighting



# 5. 图像 Image



# 6. 转移到 PBR Transition to PBR



# 参考文献

[^Dro13]: M. Drobot. "[**Lighting of Killzone: Shadow Fall**](http://www.guerrilla-games.com/publications/)". In: Digital Dragons. 2013.

[^Kar13]: B. Karis. "[**Real Shading in Unreal Engine 4**](http://selfshadow.com/publications/s2013-shading-course/)". In: Physically Based Shading in Theory and Practice, ACM SIGGRAPH 2013 Courses. SIGGRAPH ’13. Anaheim, California: ACM, 2013, 22:1{22:8. isbn: 978-1-4503-2339-0. doi: 10.1145/2504435.2504457.

[^Koj+13]: H. Kojima, H. Sasaki, M. Suzuki, and J. Tago. "[**Photorealism Through the Eyes of a FOX: The Core of Metal Gear Solid Ground Zeroes**](http://www.gdcvault.com/play/1018086/Photorealism-Through-the-Eyes-of)". In: Game Developers Conference. 2013.

[^LH13]: S. Lagarde and L. Harduin. "[**The Art and Rendering of Remember Me**](http://seblagarde.wordpress.com/2013/08/22/gdceurope-2013-talk-the-art-and-rendering-of-remember-me/)". In: Game Developers Conference Europe. 2013.

