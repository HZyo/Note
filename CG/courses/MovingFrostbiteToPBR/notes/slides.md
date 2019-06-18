# 目录

[TOC]

# 概览

将 Frostbite 引擎转变成 PBR

包含三个部分

- 总结将引擎转变成 PBR 的**所有步骤** 
- 在基础实现中使用当时**最先进的技术**（PBR）
- 质量上小**提升** 

# PBR 范畴

![1560830890000](assets/1560830890000.jpg)

- 材质
- 灯光
- 环境
- 摄像机

# 参考框架 Reference Framework

![1560830985103](assets/1560830985103.jpg)

从 Frosbite 输出到 Mitsuba（离线 PT），但太慢，因此构建了引擎内置的参考模式

# 材质 Material

## 标准模型 Standard Model

- 标准材质：Specular (GGX)  + Diffuse (Disney)

  > 示例
  >
  > 电介质 Dielectric
  >
  > ![1560831348995](assets/1560831348995.jpg)
  >
  > 导体 Conductor
  >
  > ![1560831365406](assets/1560831365406.jpg)

- 其他材质

  - 次表面材质
  - 单层涂敷 coated 材料

## 镜面项 Specular

$$
f_s(\mathbf{v},\mathbf{l})=
\frac{F_{\text{Schlick}}G_\text{HC-Smith}D_\text{GGX}}
{4(\mathbf{n}\cdot\mathbf{v})(\mathbf{n}\cdot\mathbf{l})}
$$

注意这里的几何函数 $G$ 并不是 regular/standard (uncorrelated) Smith 函数，而是 height-correlated Smith 函数（理论上更加正确）[^Heitz14]。

> standard (uncorrelated) Smith
> $$
> G(\mathbf{v},\mathbf{l})\approx G_1(\mathbf{v})G_1(\mathbf{l})
> $$
> 其中
> $$
> G_1(\omega)=\frac{2}{1+\sqrt{1+\alpha_{g}^{2} \tan ^{2} \theta}}
> $$

对比如下

- Standard(uncorrelated) Smith G Term

  ![1560835117049](assets/1560835117049.jpg)

- Height-correlated Smith G Term

  ![1560835123957](assets/1560835123957.jpg)

差别不是很大，但在高粗糙度时差距比较明显

![1560835348408](assets/1560835348408.jpg)

## 漫反射项 Diffuse

对于漫反射项，我们想把**镜面的粗糙度和漫反射项的粗糙度结合**起来，在**高粗糙度时想要有回射 retro-reflective 现象**。

![1560836293874](assets/1560836293874.jpg)

我们调研了 GGX 分布[^Gotanda14]，但还是用 Disney 漫反射模型[^Burley12]，因为简单而且足够好。

>对于 Lambertian Diffuse，根本就没有粗糙度的概念

对比如下

- Lambertian Diffuse

  ![1560836389100](assets/1560836389100.jpg)

- Disney Diffuse

  ![1560836417636](assets/1560836417636.jpg)

Lambertian Diffuse 对于所有粗糙度都是一样的，Disney Diffuse 在低粗糙度时比较暗，高粗糙度时比较亮。差距细微，但还是有差距。

![1560836538706](assets/1560836538706.jpg)

Disney 模型不满足能量守恒，通过简单的线性校正 linear correction 即可

![1560836768603](assets/1560836768603.jpg)

效果如下

![1560836800670](assets/1560836800670.jpg)

变得暗了些，特别是高粗糙度的情形，此时有更多的回射。

## 参数化 Parameterization

![1560837043612](assets/1560837043612.jpg)

> 这里 Reflectance 就是反射率，就是电介质的 $F_0$。

遵循 Burley 的方法。

暴露 `smoothness` 给 artists 而不是 `roughness`，因为白色即为光滑更加直观。

![1560837453377](assets/1560837453377.jpg)

为了得到“感官上线性”的粗糙度，我们使用了 Burly[^Burley12] 的方法。

![1560837582350](assets/1560837582350.jpg)

`Reflectance` 用于控制 Fresnel 值，对应 $F_0​$ 的子集，以获得更多的精度，最终是将 0 - 255 映射到 0 - 0.16。

![1560837894676](assets/1560837894676.jpg)

- 低范围（0 - 127）用于 specular micro occlusion
- 中值（128）代表最常见的 0.04
- 高范围（129 - 255）用于宝石 gem stone。最大为 0.16，虽然有些宝石为 0.17，但为了更好地编码 $F_0$ 选择了 0.16。

> 示例
>
> ![1560838151927](assets/1560838151927.jpg)

# 光照 Lightingnm

![1560838319206](assets/1560838319206.jpg)

光照包含解析光 analytical lights、太阳 sun、天空 sky、周围环境 entrie surroundings。

光照**一致性** lighting **coherence** 是实现真实画面的关键：

- 所有的 BRDF 应该对**所有光源类型**积分
- 所有的光需要管理**直接**和**间接**光照
- 所有的光照应正确**组合**（SSR/local IBL/...）
- 所有的灯之间都有**正确的比例** 

## 参考单位和框架 Units & Frame of Reference

![1560838784149](assets/1560838784149.jpg)

我们知道光源的范围很广：蜡烛发出的光很少，太阳非常明亮。

在过去，艺术家通常为场景中最强的光源定义一个任意值。然后他们定义了相对于这个关键光源的其他光源的强度。

这使得调整灯光或重复使用灯光设置变得困难。

一个更好的方法是使用一个共同的参考框架。

![1560838832527](assets/1560838832527.jpg)

通过使用一致的光强单位系统（例如光度测量 photometry），可以为任何给定光源确定精确的（物理）值。

通过一个单一的参考框架，我们现在可以确保我们所有的照明一致性，我们可以在不同的场景中重用一些照明设备。

Frostbite 整个光照管线使用了光度 photometric 单位。有四种类型

![1560838993590](assets/1560838993590.jpg)

> lum. power 强调**整体**的光照效果
>
> illum. 强调**被照射物**的光照效果
>
> lum. 强调**某点某方向**的光照效果
>
> lum. intensity 强调**某方向**的光照效果

光源与相应的光度单位如下

![1560839078440](assets/1560839078440.jpg)

> EV 是等价于 $\text{cd}/\text{m}^2$ 的单位

## 解析光源 Analytical Lights

### 参数化 Paramaterization

![1560839277894](assets/1560839277894.jpg)

颜色用 intensity 和 color 来控制，用色温 color temperature 来控制颜色。

> [色温 from 百度百科](https://baike.baidu.com/item/%E8%89%B2%E6%B8%A9/103689?fr=aladdin)
>
> 色温是表示光线中包含颜色成分的一个[计量单位](https://baike.baidu.com/item/%E8%AE%A1%E9%87%8F%E5%8D%95%E4%BD%8D/9595478)。从理论上讲，色温是指绝对[黑体](https://baike.baidu.com/item/%E9%BB%91%E4%BD%93/5398327)从绝对零度(一273℃)开始加温后所呈现的颜色。黑体在受热后．逐渐由黑变红，转黄，发白，最后发出蓝色光。当加热到一定的温度．黑体发出的光所含的光谱成分．就称为这一温度下的色温，计量单位为“K”(开尔文)、如果某一光源发出的光，与某一温度下黑体发出的光所含的[光谱](https://baike.baidu.com/item/%E5%85%89%E8%B0%B1/757474)成分相同．即称为某K色温。如100 W灯泡发出光的颜色，与绝对黑体在2527℃时的颜色相同，那么这只灯泡发出的光的色温就是：（2527+273）K=2800K。

artists 要选取合适的单位，详见[参考单位和框架 Units & Frame of Reference](#参考单位和框架 Units & Frame of Reference)。

> 这些值很容易设置，从产品外包装上或网上就能看到
>
> ![1560839565317](assets/1560839565317.jpg)

### 形状

真实世界的光源是各种形状的面光源

![1560839721920](assets/1560839721920.jpg)

我们支持四种不同的形状：球 sphere、圆盘 disk、长方形 rectangle 和管 tube。

他们都对应了一个简化版本，分别为点 point，聚 spot，锥 frustum 和线 line。只有 point 和 spot 使用了 punctual light path。

### Punctual light

- 单位：lum. power (lm) 或者 lum. intensity (cd)

- 遵循了平方反比定律 inverse square law，为了性能原因，在给定衰减半径 attenuation radius 处衰减至 0，采用了 Karis 的方案[^Karis13]。

![1560840214007](assets/1560840214007.jpg)

> 通过实际测量，物理公式是正确的
>
> ![1560840354404](assets/1560840354404.jpg)

### Photometric lights

- 单位：lum. intensity (cd)

- 用于点光源和聚光灯

  ![1560840641540](assets/1560840641540.jpg)

参数的获取可以来自于 IES profiles 或者 artists 自行设置

> 示例
>
> ![1560840946178](assets/1560840946178.jpg)
>
> ![1560840955840](assets/1560840955840.jpg)

### Area lights

- 单位：lum. power (lm) 或 lum. ($\text{cd}/\text{m}^2$ 或 EV)

面光源是 PBR 引擎的“一等公民”，然而难以实现，现还没有准备投入生产。

![1560841117542](assets/1560841117542.jpg)

将面光源的计算分成 diffuse 和 specular。

#### Diffuse

正确处理 diffuse 是获取大面光源软光照的关键，需要考虑 horizon。当光开始于着色点相应平面交叉时，光照强度应该衰减。

![1560841471015](assets/1560841471015.jpg)

![1560841484987](assets/1560841484987.jpg)

有三种积分方法

- 解析 Analytic：form factor (radiosity) / view factor (heat transfer)
- MRP：**M**ost **R**epresentative **P**oint lighting[^Drobot14]
- Strutured sampling of light shape：内部研发

![1560841926946](assets/1560841926946.jpg)

#### Specular

没有满意的方法。

选择使用了 Karis 的 Shortest distance to reflection ray 方法[^Karis13]，因为快且结果不错，没有圆盘和长方形的面光源的能量守恒形式。

![1560843599080](assets/1560843599080.jpg)

> 示例
>
> ![1560843563534](assets/1560843563534.jpg)

> 有什么游戏推动了计算机图形学的发展？ - 叛逆者的回答 - 知乎
> https://www.zhihu.com/question/27055011/answer/117061007
>
> 这里给出了实时多边形面光源的解决方案，2016 年的文章，在本教程之后

### Sun light

- 单位：Illuminance (lux)

对于 diffuse，用单一方向简单近似。

对于 specular，使用了定向圆盘近似，有两点好处

- 为光滑的材料生成实际的太阳圆盘形状
- 减少镜面混叠（相对于定向光）。

![1560844061888](assets/1560844061888.jpg)

![1560844069486](assets/1560844069486.jpg)

### Emissive surfaces

- 单位：Luminance ($\text{cd}/\text{m}^2$ 或 EV)
- 面光源的互补，只代表面光源的可见部分，不发射光，但使用物理光照单位使得他们与光源发出的光相匹配

![1560844572929](assets/1560844572929.jpg)

> 这个配图没看懂，喵喵喵~

## Image-Based Lights

### 分类

- Distant light probe: parallax-free far lighting
- Local light probes: local lighting with parallax
- Screen-space reflections: close-range lighting (supporting glossy reflection)
- Planar reflections: an alternative to SSR

> woc，我之前写的文章应该是只包括了 disntant light probe
>
> 见笑了

### Distant light probe

- 单位：Luminance ($\text{cd}/\text{m}^2$ 或 EV)

- 来源

  - HDRI

    ![1560845127022](assets/1560845127022.jpg)

    > 网上的大部分 HDR 图像的值范围很可能不大好

  - Procedural sky

反射方程（环境光 x BRDF）预积分 [^Karis13]

![1560846159827](assets/1560846159827.jpg)

> 详细参考 [深入理解 PBR/基于图像照明 (IBL)](https://zhuanlan.zhihu.com/p/66518450) 

各项同性假设引入误差

![1560846709460](assets/1560846709460.jpg)

每当光照变化，LD 需要重新计算（需要快速计算以支持实时捕获和更新）

#### LD 积分方法

- 重要性采样
- 多重重要性采样
- 过滤重要性采样 Filtered importance sampling，收敛快速

对比如下

![1560846998836](assets/1560846998836.jpg)

![1560847117943](assets/1560847117943.jpg)

#### Runtime evaluation

![1560847399418](assets/1560847399418.jpg)

通常我们用反射方向（红色虚线箭头）来采样 cubemap，但是 BRDF 的主方向（绿色实线箭头）与其不同，使用主方向采样可以提高准确度。从反射方向到主方向的公式在课程笔记中提供。

对比如下

- 反射方向 Mirror Direction

  ![1560847611278](assets/1560847611278.jpg)

- 主方向 Dominant Direction

  ![1560847618690](assets/1560847618690.jpg)

对粗糙材质的提升效果显著

![1560847712988](assets/1560847712988.jpg)

### Local light probes

Local light probes 捕捉周围环境，并通过盒和球 proxy 使用视差校正 parallax correction[^Lagarde12]。

![1560856870674](assets/1560856870674.jpg)

一个场景，得到对应的包围盒（proxy geometry），然后在中心计算光照，得到一个 cubemap

![1560856938624](assets/1560856938624.jpg)

这个 incident capture 值包含了 diffuse，忽略了其他 view-dependent 效果，如 specular。

对于 conductors，他们没有 diffuse 项，我们使用 $F_0​$ 作为 diffuse 颜色。

同时我们还会存储可见性，放在 alpha 通道。当没有物体遮挡时，我们就可以直接使用 distant light probe。

![1560857704577](assets/1560857704577.jpg)

这个 local light probe 用法上类似于 distant light probe，但要进行视差校正 parallax correction，通过 distance-based roughness 来完成

我们可以看到，不同位置下反射所覆盖到的墙的面积不同，考虑这种现象，我们用距离去调整粗糙度

![1560858339296](assets/1560858339296.jpg)

![1560858352188](assets/1560858352188.jpg)

效果如下

![1560858454542](assets/1560858454542.jpg)

# 相机

Frostbite 内的光照计算使用了真实世界的 luminance 值，我们需要将这个 luminance 转换成像素值。

由于其极高的动态范围，不可能捕捉到整个入射亮度范围，因此相机只能通过“曝光”场景捕捉一小部分。

![1560859119314](assets/1560859119314.jpg)

相机设置

![1560859581952](assets/1560859581952.jpg)

![1560859597754](assets/1560859597754.jpg)

到达 sensor 的 luminance 由 exposure 决定，将转变成像素值。

![1560859711038](assets/1560859711038.jpg)

从 exposed value 到像素值的转变使用常见的 color pipeline（tonemapping、color grading、gamma correction 等）。

曝光计算依赖于基于物理的方法，我们使用的标准名为 Saturation-Based Sensitivity。

![1560859921131](assets/1560859921131.jpg)

测试结果

Sunny 16, sky 20000 lux, sun 100000 lux, f/16, 1/125s, ISO 100

![1560859984616](assets/1560859984616.jpg)

# 转移到 PBR

- 标准材质，viewer with distant light probe，教育关键的 artists
- 同时使用 PBR / non-PBR，实现自动转换
- 安利 PBR 给游戏团队，提供一组验证工具

# 参考

[^Burley12]: Brent Burley, “**Physically Based Shading at Disney**”, SIGGRAPH’12, PBR Course

[^Karis13]: Brian Karis, “**Real Shading in Unreal Engine 4**”, SIGRRAPH’13, PBR Course

[^Drobot14]: Michal Drobot, ”**Physically Based Area Lights**”, GPU Pro 5

[^Gotanda14]: unknown

[^Heitz14]: Eric Heitz, ”**Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs**”, JCGT, 2014

[^Lagarde12]: Sébastien Lagarde, “**Local Image-based Lighting With Parallax-Corrected Cubemaps**”, SIGGRAPH’12

