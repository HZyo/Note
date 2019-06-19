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

## 3.1 材质模型 Material models

### 3.1.1 外观 Appearance 

![1560924180465](assets/1560924180465.png)

不同的外观可根据物理属性（如 conductivity，mean-free-path，absorption）分类。

BSDF 模型可分为反射部分 BRDF 和透射部分 BTDF。本文只关注反射部分和一个特定的材质模型，其可表示“标准”外观。

### 3.1.2 材质模型 Material models

所使用的标准材质模型可分成两部分

- 低角频率信号 low angular frequency signal，称为 diffuse，记为 $f_d$ 
- 低到高角频率信号 low to hight angular frequency，称为 specular，记为 $f_r$ 

![1560924923148](assets/1560924923148.png)

一个平坦的表面可以用菲涅尔定律来表示，对于不平坦的表面，可以使用微平面模型。

![1560925155675](assets/1560925155675.png)

一个微平面模型如下[^Hei14]
$$
f_{d / r}(\mathbf{v})=\frac{1}{|\mathbf{n} \cdot \mathbf{v}||\mathbf{n} \cdot \mathbf{1}|} \int_{\Omega} f_{m}(\mathbf{v}, \mathbf{1}, \mathbf{m}) G(\mathbf{v}, \mathbf{l}, \mathbf{m}) D(\mathbf{m}, \alpha)\langle\mathbf{v} \cdot \mathbf{m}\rangle\langle\mathbf{l} \cdot \mathbf{m}\rangle \mathrm{d} \mathbf{m}
$$

适用于 diffuse 和 specular。

对于镜面项， $f_m$ 是一个完美的镜子，可以用菲涅尔定律建模，公式如下
$$
f_{r}(\mathbf{v})=\frac{F\left(\mathbf{v}, \mathbf{h}, f_{0}, f_{90}\right) G(\mathbf{v}, 1, \mathbf{h}) D(\mathbf{h}, \alpha)}{4\langle\mathbf{n} \cdot \mathbf{v}\rangle\langle\mathbf{n} \cdot \mathbf{l}\rangle}
$$
Heirz[^Hei14]指出应使用正确的 G 项，很多文献使用 Smith 近似，然而更精确的形式考虑了遮蔽和阴影的相干性，如下
$$
\begin{aligned}

G(\mathbf{v}, 1, \mathbf{h}, \alpha)&=\frac{\chi^{+}(\mathbf{v} . \mathbf{h}) \chi^{+}(\mathbf{l} . \mathbf{h})}{1+\Lambda(\mathbf{v})+\Lambda(\mathbf{l})}\\

\Lambda(\mathbf{m})&=\frac{-1+\sqrt{1+\alpha^{2} \tan ^{2}\left(\theta_{m}\right)}}{2}=\frac{-1+\sqrt{1+\frac{\alpha^{2}\left(1-\cos ^{2}\left(\theta_{m}\right)\right)}{\cos ^{2}\left(\theta_{m}\right) )}}}{2}\\

\end{aligned}
$$
比较如下

![1560926027093](assets/1560926027093.png)

高粗糙度下，height-correlated 版本更亮一些。

对于 diffuse，$f_m$ 遵循 Lambertian 模型，因此有
$$
f_{d}(\mathbf{v})=\frac{\rho}{\pi} \frac{1}{|\mathbf{n} \cdot \mathbf{v}||\mathbf{n} \cdot 1|} \int_{\Omega} G(\mathbf{v}, 1, \mathbf{m}) D(\mathbf{m}, \alpha)\langle\mathbf{v} \cdot \mathbf{m}\rangle\langle\mathbf{1} \cdot \mathbf{m}\rangle \mathrm{d} \mathbf{m}
$$
往常 $f_d​$ 被视为简单的 Lambertian 模型，然而 diffuse 部分应该与 specular 一致，并且考虑 `roughness`[^Bur12]。上式没有解析解，Burley[^Bur12] 给出了经验公式，考虑了 `roughness` 并且在 grazing angles 处有回射 retro-reflection
$$
\begin{aligned}

f_{d}&=\frac{\rho}{\pi}\left(1+F_{D 90}(1-\langle\mathbf{n} \cdot 1\rangle)^{5}\right)\left(1+F_{D 90}(1-\langle\mathbf{n} \cdot \mathbf{v}\rangle)^{5}\right)\\

F_{D 90}&=0.5+\cos \left(\theta_{d}\right)^{2} \alpha\\

\end{aligned}
$$

> $\theta_d​$ 不知道指什么

### 3.1.3 能量守恒 Energy conservation

能量守恒要求
$$
\rho_{h d}(\mathbf{v})=\int_{\Omega} f(\mathbf{v}, 1)\langle\mathbf{n} \cdot \mathbf{1}\rangle \mathrm{dl}=\int_{\Omega}\left(f_{r}(\mathbf{v}, \mathbf{l})+f_{d}(\mathbf{v}, \mathbf{l})\right)\langle\mathbf{n} \cdot 1\rangle \mathrm{d} \mathbf{l} \leq 1
$$
Disney diffuse 不是能量守恒的。

我们修改了它，保证了能量守恒，并且保留了回射的特性，如下

```c++
float Fr_DisneyDiffuse ( float NdotV , float NdotL , float LdotH , float linearRoughness )
{
    float energyBias = lerp (0, 0.5 , linearRoughness );
    float energyFactor = lerp (1.0 , 1.0 / 1.51 , linearRoughness );
    float fd90 = energyBias + 2.0 * LdotH * LdotH * linearRoughness ;
    float3 f0 = float3 (1.0f, 1.0f, 1.0 f);
    float lightScatter = F_Schlick (f0 , fd90 , NdotL ).r;
    float viewScatter = F_Schlick (f0 , fd90 , NdotV ).r;

    return lightScatter * viewScatter * energyFactor ;
}
```

![1560927690240](assets/1560927690240.png)

![1560927800844](assets/1560927800844.png)

### 3.1.4 形态特征 Shape characteristics

specular 有两个容易被忽视但有重要影响的现象

- Half-angle parametrization：BRDF形状发生非线性变换，即从正常入射角的各向同性向掠射角的各向异性转变，详见[4.9 节](#4.9)。

- Off-specular：经常假设 BRDF 的 lobe 中心在反射方向附近，然而由于 $\langle\mathbf{n} \cdot 1\rangle$ 和 G，当 `roughness` 增大时，BRDF 的 lobe 会朝向法向偏移，称为 Off-specular peak。lobe 的中心方向称为 dominant direction

  ![1560928607758](assets/1560928607758.png)

### 3.1.5 Frostbite standard model

总结一下，Frostbite 的标准材质模型

- specular $f_r$：镜面微平面模型，G 为 Smith correlated visibility function，D 为 GGX
- diffuse $f_d$：renormalization Disney diffuse

使用了 dominant direction 校正。

BRDF 代码如下

```c++
float3 F_Schlick (in float3 f0 , in float f90 , in float u)
{
    return f0 + ( f90 - f0) * pow (1. f - u, 5.f);
}

float V_SmithGGXCorrelated ( float NdotL , float NdotV , float alphaG )
{
    // Original formulation of G_SmithGGX Correlated
    // lambda_v = (-1 + sqrt ( alphaG2 * (1 - NdotL2 ) / NdotL2 + 1)) * 0.5 f;
    // lambda_l = (-1 + sqrt ( alphaG2 * (1 - NdotV2 ) / NdotV2 + 1)) * 0.5 f;
    // G_SmithGGXCorrelated = 1 / (1 + lambda_v + lambda_l );
    // V_SmithGGXCorrelated = G_SmithGGXCorrelated / (4.0 f * NdotL * NdotV );

    // This is the optimize version
    float alphaG2 = alphaG * alphaG ;
    // Caution : the " NdotL *" and " NdotV *" are explicitely inversed , this is not a mistake .
    float Lambda_GGXV = NdotL * sqrt ((- NdotV * alphaG2 + NdotV ) * NdotV + alphaG2 );
    float Lambda_GGXL = NdotV * sqrt ((- NdotL * alphaG2 + NdotL ) * NdotL + alphaG2 );

    return 0.5 f / ( Lambda_GGXV + Lambda_GGXL );
}

float D_GGX ( float NdotH , float m)
{
    // Divide by PI is apply later
    float m2 = m * m;
    float f = ( NdotH * m2 - NdotH ) * NdotH + 1;
    return m2 / (f * f);
}

// This code is an example of call of previous functions
float NdotV = abs( dot (N, V)) + 1e -5f; // avoid artifact
float3 H = normalize (V + L);
float LdotH = saturate ( dot (L, H));
float NdotH = saturate ( dot (N, H));
float NdotL = saturate ( dot (N, L));

// Specular BRDF
float3 F = F_Schlick (f0 , f90 , LdotH );
float Vis = V_SmithGGXCorrelated (NdotV , NdotL , roughness );
float D = D_GGX (NdotH , roughness );
float Fr = D * F * Vis / PI;

// Diffuse BRDF
float Fd = Fr_DisneyDiffuse (NdotV , NdotL , LdotH , linearRoughness ) / PI;
```

## 3.2 材质系统 Material system

### 3.2.1 材质 Material

在 Frostbite 中，材质定义为

- lighting path: deferred, forward or both
- input parameters: diffuse, smoothness, thickness, etc
- material model: rough surface, translucency, skin, hair, etc and non-PBR rough surface
- GBuffer layout

每种材质用 `MaterialID` 标识

Disney base material 使用下列参数

- Normal

- BaseColor

  - non-metallic: diffuse albedo
  - metallic: $F_0​$ 

- Smoothness: $\text{smoothness}=1-\alpha_\text{lin}​$ 

- MetalMask: metalness, mask 用于暗示 artist 这个值是 binary

- Reflectance: $F_0=0.16\ \text{reflectance}^2​$ 

  ![1560930607656](assets/1560930607656.png)

`roughness` 使用了平方映射

![1560930438896](assets/1560930438896.png)

相应的 GBuffer layout 如下

![1560930663756](assets/1560930663756.png)

> 有一些没看懂的点
>
> Normal 那的 10:10 是什么？
>
> `MaterialID` 后的括号是什么？
>
> GB1 的 alpha 通道什么意思？

有一些限制

- 所有的基础属性（`Normal`，`BaseColor`，`Smoothness`，`MetalMask`，`Reflectance`）要可混合 bendable 以支持延迟贴花 deferred decals。不可混合 unblendable 的属性（如 `MaterialID` 存储在 alpha 通道）。避免了压缩和编码机制，因为这会影响 blending。
- `MaterialID`应放在相同的位置，用于解释 `MatData`
- 常用的参数放在同一 buffer 中
- 只使用 4 个 buffer（不包括 depth）

### 3.2.2 渲染循环 Render loop

对于前向渲染的物体，设置好 shader，传输好参数就可以渲染了。对于延迟着色的物体，要考虑更多

- 材质模型尽量共享更多的光照代码，依赖于动态分支 dynamic branching 以支持小的调整。有大量不同光照代码的需要利用 stencil buffer 进行不同的 lighting pass。
- 材质尽量与基础代码布局相同，依赖于动态分支利用存储的参数以支持小的调整。有大量不同的材质需要不同的 GBuffer passes，然后在 lighting pass 中用 stencil buffer 标识
- 尝试用 fix-up pass 为不同 GBuffer layout 的材质共享 lighting pass

## 3.3 PBR 和贴花 PBR and decals

贴花 decals 可以被看作是一个动态系统的分层材料属性，让我们创造丰富的外观和变化。

在 Frostbite 中使用了延迟着色以渲染贴花（deferred decals）。

有一些要点

- 正确性 Correctness：混合操作的正确性很重要
- 交互 Interaction：贴花和目标表面应使用相同的材质
- ...

# 4. 光照 Lighting



# 5. 图像 Image



# 6. 转移到 PBR Transition to PBR



# 参考文献

[^Bur12]: B. Burley. "[**Physically Based Shading at Disney**](http://selfshadow.com/publications/s2012-shading-course/)". In: Physically Based Shading in Film and Game Production, ACM SIGGRAPH 2012 Courses. SIGGRAPH ’12. Los Angeles, California: ACM, 2012, 10:1{7. isbn: 978-1-4503-1678-1. doi: 10.1145/2343483.2343493.

[^Dro13]: M. Drobot. "[**Lighting of Killzone: Shadow Fall**](http://www.guerrilla-games.com/publications/)". In: Digital Dragons. 2013.

[^Hei14]: E. Heitz. "[**Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs**](http://jcgt.org/published/0003/02/03/)". In: Journal of Computer Graphics Techniques (JCGT) 3.2 (June 2014), pp. 32{91. issn: 2331-7418.

[^Kar13]: B. Karis. "[**Real Shading in Unreal Engine 4**](http://selfshadow.com/publications/s2013-shading-course/)". In: Physically Based Shading in Theory and Practice, ACM SIGGRAPH 2013 Courses. SIGGRAPH ’13. Anaheim, California: ACM, 2013, 22:1{22:8. isbn: 978-1-4503-2339-0. doi: 10.1145/2504435.2504457.

[^Koj+13]: H. Kojima, H. Sasaki, M. Suzuki, and J. Tago. "[**Photorealism Through the Eyes of a FOX: The Core of Metal Gear Solid Ground Zeroes**](http://www.gdcvault.com/play/1018086/Photorealism-Through-the-Eyes-of)". In: Game Developers Conference. 2013.

[^LH13]: S. Lagarde and L. Harduin. "[**The Art and Rendering of Remember Me**](http://seblagarde.wordpress.com/2013/08/22/gdceurope-2013-talk-the-art-and-rendering-of-remember-me/)". In: Game Developers Conference Europe. 2013.

