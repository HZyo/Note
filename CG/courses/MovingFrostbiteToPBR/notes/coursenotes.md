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

## 4.1 General

lighting pipeline 应支持 high dynamic range HDR，光照处理必须在线性空间完成。管线的输入和输出都应该是 gamma corrected 的，Frostbite 选择依赖于 sRGB。

一个可信的场景基于光照的一致性和正确性：所有物体从周围环境获取光照、反射光照且有阴影。主要准则是默认使所有物体正确，然后给 artist 调整。

支持的光源

- punctual light
- photometric light
- area light
- emissive surface
- IBL
  - distant light probe (sky)
  - localized light probe
  - screen space reflections (SSR)

一致性包括

- material lighting：所有 BSDF 与所有光源类型正确交互
- indirect-diffuse lighting：所有的光源类型都应考虑
- indrect-specular lighting：SSR、localized light probes 和 distant light probes 应正确结合
- light units：单位统一
- decals：正确影响所有光源类型

## 4.2 解析光源参数 Analytical light parameters

将光的 hue（color）从 intensity 分离。用 color temperature 或 correlated color temperature (CCT) 来定义颜色，单位是 Kelvin (K)。

从 color temperature 获取 hue 很困难，artist 也可以直接使用 RGB。

只有 point 和 spot 是 punctual light，其他都是 area light

![1560942163731](assets/1560942163731.png)

## 4.3 光单位 Light unit

> 细节很多，较难把握

photometry 本质上是根据人眼的灵敏度加权的 radiometry。

![1560942485636](assets/1560942485636.png)

人眼灵敏度用 CIE photometric curve $V(\lambda)$ 表示。

![1560942704697](assets/1560942704697.png)

photometric 量与 radiometric 量的关系如下（积分区间是可见光谱 380nm - 780nm）
$$
X_{v}=K_{m} \cdot \int_{380}^{780} X_{e}(\lambda) V(\lambda) d \lambda
$$
其中常数 $K_m$ 是 the maximum spectral luminous efficacy of radiation for photoscopic vision，$K_m=683$。

> 1 watt 的 555nm 灯是 683 lumens

在 spectral 渲染器中，光源用 radiometric 单位描述。将其装换为像素经常需要 photometric weighted 过程。

在 Frostbite 中，所有光源使用 photometric 单位。

...

## 4.4 Punctual lights

Frostbite 只支持 point 和 spot 这两种 punctual light。为了物理正确，他们应遵循“平方反比定律”。

![1560943664320](assets/1560943664320.png)

公式为
$$
E=\frac{I}{\text {distance}^{2}}
$$
其中 $I$ 是 luminous intensity，E 是 illuminance。

为了避免数值问题，通常给添加一个下限
$$
E=\frac{I}{\max \left(\text {distance}^{2}, 0.01^{2}\right)}
$$
在 Frostbite 中，artists 可以读 punctual light intensity 使用 luminous power 或 luminous intensity 作为单位。光照计算中，luminous power 总是会转换成 luminous intensity，转换关系如下

- 点光源 Point light
  $$
  \phi=\int_{S} I \mathrm{dl}=\int_{0}^{2 \pi} \int_{0}^{\pi} I \mathrm{d} \theta \mathrm{d} \phi=4 \pi I
  $$

- 聚光灯 Spot light
  $$
  \phi=\int_{\Omega} I \mathrm{dl}=\int_{0}^{2 \pi} \int_{0}^{\theta_{\text { outer }}} I \mathrm{d} \theta \mathrm{d} \phi=2 \pi\left(1-\cos \frac{\theta_{\text { outer }}}{2}\right) I
  $$

  > 常见的是用 inner 和 outer 角度来设定 spot light 的，因此可推出不同的公式

相同的 luminous power，张角越小则越亮

![1560945333299](assets/1560945333299.png)

这种耦合使得 artist 很难操作，因此在 Frostbite 中 spot light 单位转换设定为
$$
\phi = \pi I
$$
转换关系总结如下

- Point
  $$
  \frac{\phi}{4 \pi}
  $$

- Spot
  $$
  \frac{\phi}{2 \pi\left(1-\cos \frac{\theta_{\text { outer }}}{2}\right)} \text { or } \frac{\phi}{\pi}
  $$

- Frustum
  $$
  \frac{\phi}{4 \arcsin \left[\sin \left(\frac{\theta_{a}}{2}\right) \sin \left(\frac{\theta_{b}}{2}\right)\right]}
  $$

  > Frustum light 在 Frostbite 中视为面光源，因此他们不会使用这个公式
  >
  > 只是偶尔用一下，并不能像 punctual light 那样使用有效的 lighting path

光照计算

- Point light
  $$
  \begin{aligned}
  L_{o u t}
  &= f(\mathbf{v}, \mathbf{l}) E\\
  &= f(\mathbf{v}, \mathbf{l}) L_{i n}\langle\mathbf{n} \cdot \mathbf{l}\rangle\\
  &= f(\mathbf{v}, \mathbf{l}) \frac{I}{\text {distance}^{2}}\langle\mathbf{n} \cdot \mathbf{l}\rangle\\
  &= f(\mathbf{v}, \mathbf{l}) \frac{\phi}{4 \pi \text { distance }^{2}}\langle\mathbf{n} \cdot \mathbf{l}\rangle\\
  \end{aligned}
  $$

- Spot light
  $$
  \begin{aligned}
  L_{o u t}&=f(\mathbf{v}, \mathbf{l}) \frac{I}{\text{distance}^{2}}\langle\mathbf{n} \cdot \mathbf{l}\rangle\\
  &= f(\mathbf{v}, \mathbf{l}) \frac{\phi}{\pi \text { distance }^{2}}\langle\mathbf{n} \cdot \mathbf{l}\rangle \text {getAngleAttenuation}( )
  \end{aligned}
  $$

出于性能考虑，渲染器会实现一个有限灯光范围以支持灯光裁剪算法。Frostbite 所用的如下

$$
E_{\text {window} 1}=\left(\frac{I}{\text {distance}^{2}}\right) \operatorname{saturate}\left(1-\frac{\text {distance}^{n}}{\text {light} \text {Radius}^{n}}\right)^{2}
$$

其中 n = 4，同于 Karis[^Kar13]。这个函数用于所有 punctual light 和 area light，然而并不能很好符合非球形 non-spherical shape 如 tube 或 rectangle light。

本节相关代码如下

```c++
float smoothDistanceAtt ( float squaredDistance , float invSqrAttRadius )
{
    float factor = squaredDistance * invSqrAttRadius ;
    float smoothFactor = saturate (1.0 f - factor * factor );
    return smoothFactor * smoothFactor;
}

float getDistanceAtt ( float3 unormalizedLightVector , float invSqrAttRadius )
{
    float sqrDist = dot ( unormalizedLightVector , unormalizedLightVector );
    float attenuation = 1.0 / (max ( sqrDist , 0.01*0.01) );
    attenuation *= smoothDistanceAtt ( sqrDist , invSqrAttRadius );
    
    return attenuation ;
}

float getAngleAtt ( float3 normalizedLightVector , float3 lightDir ,
float lightAngleScale , float lightAngleOffset )
{
    // On the CPU
    // float lightAngleScale = 1.0 f / max (0.001f, ( cosInner - cosOuter ));
    // float lightAngleOffset = -cosOuter * angleScale ;
    
    float cd = dot ( lightDir , normalizedLightVector );
    float attenuation = saturate (cd * lightAngleScale + lightAngleOffset );
    // smooth the transition
    attenuation *= attenuation ;
    
    return attenuation ;
}

// Process punctual light
float3 unnormalizedLightVector = lightPos - worldPos ;
float3 L = normalize ( unnormalizedLightVector );
float att = 1;
att *= getDistanceAtt ( unormalizedLightVector , lightInvSqrAttRadius );
att *= getAngleAtt (L, lightForward , lightAngleScale , lightAngleOffset );

// lightColor is the outgoing luminance of the light time the user light color
// i.e with point light and luminous power unit : lightColor = color * phi / (4 * PI)
float3 luminance = BSDF (...) * saturate ( dot (N, L)) * lightColor * att ;
```

## 4.5 Photometric lights

photometric lights 使用 photometric profile 来描述强度分布。这些分布保存在文件中，常见的格式是 IES(.ies) 和 EULUMDAT (.ldt，简单的 ASCII 文件)。相关资源网站如 [Lithonia](www.lithonia.com)。

这些文件存储了多种角度的 luminous intensity。

![1560950205681](assets/1560950205681.png)

> ...

artists 可以使用 IES 作为 mask 来制造阴影

![1560950453717](assets/1560950453717.png)

## 4.6 Sun

太阳从地球上看的角度在 $[0.526^\circ, 545^\circ]$，即对应的立体角为 $[0.000066,0.000071]$。将太阳视为 punctual light 对 diffuse 部分是一个可接受的近似，然而对于 specular 会有问题。在 Frostbite 中，为了部分减轻这个问题，太阳处理成一个远处的面光源，垂直于 outer hemisphere。

> Outer Sphere 是什么？一个圆盘垂直于一个半球？

artists 要配置垂直于太阳方向的表面的 illuminance (lux)。 

光照计算如下
$$
L_{o u t}=f(\mathbf{v}, \mathbf{l}) E=f(\mathbf{v}, \mathbf{l}) E_{\perp}\langle\mathbf{n} \cdot \mathbf{l}\rangle
$$
对应的代码为

```c++
float3 D = sunDirection ;
float r = sin( sunAngularRadius ); // Disk radius
float d = cos( sunAngularRadius ); // Distance to disk

// Closest point to a disk ( since the radius is small , this is
// a good approximation
float DdotR = dot (D, R);
float3 S = R - DdotR * D;
float3 L = DdotR < d ? normalize (d * D + normalize (S) * r) : R;
// Diffuse and specular evaluation
float illuminance = sunIlluminanceInLux * saturate ( dot (N, D));

// D: Diffuse direction use for diffuse lighting
// L: Specular direction use with specular lighting
luminance = BSDF (V, D, L, data ) * illuminance ;
```

## 4.7 Area lights

Frostbite 支持四种面光源：sphere、disk、tube 和 rectangle。

计算公式为

$$
L_\text{out}=\int_{\Omega^{+}} f(\mathbf{v}, \mathbf{l}) V(\mathbf{l}) L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l}=\int_{\Omega_{\mathrm{light}}} f(\mathbf{v}, \mathbf{l})  L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle
$$

如果面光源可以从阴影点到达，则函数 V 是 1，否则为 0。函数 V 使得我们可以同时考虑面光源的形状和阴影。本节中我们不考虑引用（在[第 4.10.4 节](#4.10.4)考虑）。$\Omega_\text{light}$ 是面光源所占的立体角。

积分可按面积积分

![1560999695226](assets/1560999695226.png)
$$
L_\text{out}=\int_{A} f(\mathbf{v}, \mathbf{l}) L_\text{in} \frac{\langle\mathbf{n} \cdot \mathbf{l}\rangle\left\langle \mathbf{n}_{a} \cdot-\mathbf{l}\right\rangle}{\text{distance}^{2}} \mathrm{d} A
$$
这个方程不总是有解析解，但可以用蒙特卡洛积分和重要性采样进行数值积分。这个计算很耗费时间，我们设计了近似解。引擎内置的参考模式可用来检验近似解的准确性。

diffuse 和 specular 的光照积分要分开讨论
$$
\begin{aligned}

L_\text{out}

&=\int_{\Omega_\text{light}} f_{d}(\mathbf{v}, \mathbf{l}) L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle d \mathbf{l}

=\int_{A} f_{d}(\mathbf{v}, \mathbf{l}) L_\text{in} \frac{\langle\mathbf{n} \cdot \mathbf{l}\rangle\left\langle\mathbf{n}_{a} \cdot-\mathbf{l}\right\rangle}{\text{distance}^{2}} \mathrm{d} A\\

L_\text{out}

&=\int_{\Omega_\text{light}} f_{r}(\mathbf{v}, \mathbf{l}) L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle d \mathbf{l}

=\int_{A} f_{r}(\mathbf{v}, \mathbf{l}) L_\text{in} \frac{\langle\mathbf{n} \cdot \mathbf{l}\rangle\left\langle\mathbf{n}_{a} \cdot-\mathbf{l}\right\rangle}{\text{distance}^{2}} \mathrm{d} A\\

\end{aligned}
$$

> area light 没有用于生产中，目标用于 30 fps 游戏和电影。

### 4.7.1 面光源单位 Area light unit

artists 可选择两种单位

- Luminous power：光出射的总量，不受光源大小的影响，但越大的光源产生的高光会越暗，因为 power 会在 area 上均分。

  ![1561001291033](assets/1561001291033.png)

- Luminance：描述了表面功率。总能量与光源大小相关。光源产生的高光不随光源大小变化。

  ![1561003297325](assets/1561003297325.png)

实践中，artist 很少使用 luminance。

为了光照计算便利，我们会将 luminance power 转换成 luminance，Lambertian emitter 光源的转换关系如下
$$
L=\frac{\phi}{A \int_{\Omega^{+}}\langle \mathbf{l} \cdot \mathbf{n}\rangle \mathrm{d} \mathbf{l}}=\frac{\phi}{A \pi}
$$
对于四种面光源，具体的转换关系如下

- Sphere
  $$
  \frac{\phi}{4 \text { radius }^{2} \pi^{2}}
  $$

- Disk
  $$
  \frac{\phi}{\text{radius}^{2} \pi^{2}}
  $$

- Tube
  $$
  \frac{\phi}{\left(2 \pi\ \text{radius}\ \text{width} + 4 \pi\ \text{radius} ^{2}\right) \pi}
  $$

- Rectangle
  $$
  \frac{\phi}{\text{width}\ \text{height}\ \pi}
  $$

punctual light 没有面积，因此只能使用 luminous intensity 作为单位，如果 artist 用 luminance 作为单位，那么就将这些 punctual light 视为 1 cm 的小面光源。

### 4.7.2 Diffuse area lights

#### 4.7.2.1 General

首先我们用 Lambertian diffuse BRDF $\frac{\rho}{\pi}$ 来解光照积分，先不用 Disney diffuse BRDF。假设面光源有恒定的 $L_\text{in}$。因此 diffuse 光照积分为
$$
L_\text{o u t}=\frac{\rho}{\pi} \int_{\Omega_{\text {light}}} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle=\frac{\rho}{\pi} E(n)
$$
其中 illuminance E 为
$$
E(n)=\int_{\Omega_{\text { light }}} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l}=\int_{A} L_\text{in} \frac{\langle\mathbf{n} \cdot \mathbf{l}\rangle\left\langle\mathbf{n}_{a} \cdot-\mathbf{l}\right\rangle}{\text{distance}^{2}} \mathrm{d} A
$$
平方反比不适用于面光源。只能用上式进行计算。

面光源能覆盖很大范围的立体角，且可能部分位于着色点所在平面（由法向定义）之下。

![1561004226932](assets/1561004226932.png)

> 示例
>
> ![1561006970735](assets/1561006970735.png)
>
> 作图时参考，右图中没有 horizon handling

有一些方法可以用来求解上述积分方程。有的要求面光源只占一小部分立体角，并且不考虑 horizon handling。有的考虑了 horizon handling 但 intensity 不正确。如果既考虑了 horizon handling 又有正确的 intensity，那么将其称为 "correctly handling the horizon"。

积分很复杂，但一些情况下存在解析解。在 light transport 和 hear transfer 领域内有解决方案。

在 light transport 中，form factor 如下
$$
\text{FoormFactor}=\int_{x \in P_{i}} \int_{y \in P_{j}} \frac{\cos \theta \cos \theta^{\prime}}{\pi r^{2}} V(x, y) \mathrm{d} x \mathrm{d} y
$$
因此，illuminance 变为
$$
E(n)=\int_{\Omega_{\text { light }}} L_{i n}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l}= L_{i n} \pi\ \text{FormFactor}
$$
在 radiative transfer 中，有一个等价的公式，称为 view factor。为了简化，两者都称为 form factor。form factor 的公式可能是也可能不是 correctly handling the horizon。

对于 sphere 和 disk 面光源，我们使用了 form factor。

#### 4.7.2.2 Sphere area lights

有两种方法

- Quilez[^Qui06] 给出的方法没有考虑 horizon handling，并且要求小立体角。类似于 "Patch to a sphere frontal"，Quilez 的版本使用了 $\langle\mathbf{n} \cdot 1\rangle$ 来处理球心不在表面方向处的情形

  > 示例
  >
  > ![1561008742943](assets/1561008742943.png)
  >
  > 绿色部分是正确部分，可以看到对于大球光源，正确的部分变少了

- "Pathch to a sphere tilted"[^Mar14] correctly handling the horizon

两种方法的适用情况如下

![1561009706360](assets/1561009706360.png)

实现代码为

```c++
float3 Lunormalized = lightPos - worldPos ;
float3 L = normalize ( Lunormalized );
float sqrDist = dot ( Lunormalized , Lunormalized );

#if WITHOUT_CORRECT_HORIZON // Analytical solution above horizon

    // Patch to Sphere frontal equation ( Quilez version )
    float sqrLightRadius = light . radius * light . radius ;
    // Do not allow object to penetrate the light ( max )
    // Form factor equation include a (1 / FB_PI ) that need to be cancel
    // thus the " FB_PI *"
    float illuminance = FB_PI *
        ( sqrLightRadius / ( max( sqrLightRadius , sqrDist ))) * saturate ( dot (     worldNormal , L));

# else // Analytical solution with horizon

    // Tilted patch to sphere equation
    float Beta = acos ( dot ( worldNormal , L));
    float H = sqrt ( sqrDist );
    float h = H / radius ;
    float x = sqrt (h * h - 1);
    float y = -x * (1 / tan ( Beta ));

    float illuminance = 0;
    if (h * cos ( Beta ) > 1)
        illuminance = cos ( Beta ) / (h * h);
    else
    {
        illuminance = (1 / ( FB_PI * h * h)) *
            ( cos ( Beta ) * acos (y) - x * sin ( Beta ) * sqrt (1 - y * y)) +
            (1 / FB_PI ) * atan ( sin ( Beta ) * sqrt (1 - y * y) / x);
    }

    illuminance *= FB_PI ;

# endif
```

#### 4.7.2.3 Disk area light

有两种方法

- Coombe[^CH05] 给出的方法没有考虑 horizon handling，而且朝向有限制
- radiative transfer 中的方法[^HSM10b] 考虑了 horizon handling，但是限制了 tilted plane 和无朝向的 disk。为了考虑朝向，我们在公式中额外乘了 $\left\langle\mathbf{n}_{\text { light }} \cdot-\mathbf{l}\right\rangle$。这个修改适用于 horizon 之上且占小立体角的情形，其他情况下有小的偏差。结果足够好了。

![1561011234921](assets/1561011234921.png)

> 示例
>
> ![1561011457738](assets/1561011457738.png)
>
> 左图是考虑了 horizon handling 的结果，右图是真值

代码如下

```c++
float cot ( float x) { return cos (x) / sin (x); }
float acot ( float x) { return atan (1 / x); }

#if WITHOUT_CORRECT_HORIZON // Analytical solution above horizon

    // Form factor equation include a (1 / FB_PI ) that need to be cancel
    // thus the " FB_PI *"
    float illuminance = FB_PI * saturate ( dot ( planeNormal , -L)) *
    saturate ( dot( worldNormal , L)) /
        ( sqrDist / ( radius * radius ) + 1);

# else // Analytical solution with horizon

    // Nearly exact solution with horizon
    float h = length ( lightPos - worldPos );
    float r = lightRadius ;
    float theta = acos ( dot ( worldNormal , L));
    float H = h / r;
    float H2 = H * H;
    float X = pow ((1 - H2 * cot ( theta ) * cot ( theta )), 0.5) ;

    float illuminance = 0;
    if ( theta < acot (1 / H))
    {
        illuminance = (1 / (1 + H2)) * cos ( theta );
    }
    else
    {
        illuminance = -H * X * sin ( theta ) / ( FB_PI * (1 + H2)) +
            (1 / FB_PI ) * atan (X * sin ( theta ) / H) +
            cos ( theta ) * ( FB_PI - acos (H * cot ( theta ))) / ( FB_PI * (1 + H2));
    }

    // Multiply by saturate ( dot ( planeNormal , -L)) to better match ground
    // truth . Matches well with the first part of the equation but there
    // is a discrepancy with the second part . Still an improvement and it is
    // good enough .
    illuminance *= FB_PI * saturate (dot( planeNormal , -L));

# endif
```

在 Frostbite 中，disk area light 和 spot light 类似，也可以支持 angular attenuation。

```c++
// On the CPU
float3 virtualPos = lightPos + lightForward * ( discRadius / tan ( halfOuterAngle ))

// On the GPU
// Attenuate with a virtual position which is the light position shifted
// in opposite light direction by an amount based on the outer angle .
illuminance *= getAngleAtt ( normalize ( virtualPos - worldPos ), lightForward , lightAngleScale , lightAngleOffset );
```

#### 4.7.2.4 Sphere and disk area lights merging

sphere 和 disk 的计算类似，因此两者可合并

```c++
// A right disk is a disk oriented to always face the lit surface .
// Solid angle of a sphere or a right disk is 2 PI (1 - cos ( subtended angle )).
// Subtended angle sigma = arcsin (r / d) for a sphere
// and sigma = atan (r / d) for a right disk
// sinSigmaSqr = sin( subtended angle )^2, it is (r^2 / d ^2) for a sphere
// and (r^2 / ( r^2 + d ^2) ) for a disk
// cosTheta is not clamped
float illuminanceSphereOrDisk ( float cosTheta , float sinSigmaSqr )
{
    float sinTheta = sqrt (1.0 f - cosTheta * cosTheta );

    float illuminance = 0.0 f;
    // Note : Following test is equivalent to the original formula .
    // There is 3 phase in the curve : cosTheta > sqrt ( sinSigmaSqr ),
    // cosTheta > -sqrt ( sinSigmaSqr ) and else it is 0
    // The two outer case can be merge into a cosTheta * cosTheta > sinSigmaSqr
    // and using saturate ( cosTheta ) instead .
    if ( cosTheta * cosTheta > sinSigmaSqr )
    {
        illuminance = FB_PI * sinSigmaSqr * saturate ( cosTheta );
    }
    else
    {
        float x = sqrt (1.0 f / sinSigmaSqr - 1.0 f); // For a disk this simplify to x = d / r
        float y = -x * ( cosTheta / sinTheta );
        float sinThetaSqrtY = sinTheta * sqrt (1.0 f - y * y);
        illuminance = ( cosTheta * acos (y) - x * sinThetaSqrtY ) * sinSigmaSqr + atan (
            sinThetaSqrtY / x);
}

    return max ( illuminance , 0.0 f);
}

// Sphere evaluation
float cosTheta = clamp ( dot ( worldNormal , L), -0.999 , 0.999) ; // Clamp to avoid edge case
// We need to prevent the object penetrating into the surface
// and we must avoid divide by 0, thus the 0.9999 f
float sqrLightRadius = lightRadius * lightRadius ;
float sinSigmaSqr = min( sqrLightRadius / sqrDist , 0.9999 f);
float illuminance = illuminanceSphereOrDisk ( cosTheta , sinSigmaSqr );

// Disk evaluation
float cosTheta = dot ( worldNormal , L);
float sqrLightRadius = lightRadius * lightRadius ;
// Do not let the surface penetrate the light
float sinSigmaSqr = sqrLightRadius / ( sqrLightRadius + max ( sqrLightRadius , sqrDist ));
// Multiply by saturate ( dot ( planeNormal , -L)) to better match ground truth .
float illuminance = illuminanceSphereOrDisk ( cosTheta , sinSigmaSqr )
* saturate ( dot( planeNormal , -L));
```

#### 4.7.2.5 Rectangular area lights

几种情况如下

![1561012808956](assets/1561012808956.png)

没有找到考虑了 horizon handling 的简单 form factor 解决方案。因此得使用替代方案。

Drobot 给出了近似解，利用了一个最具代表性的 diffuse point lihgt 加以立体角权重
$$
E(\mathbf{n})=\int_{\Omega_{\text { light }}} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l} \approx \Omega_{\text { light }} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle
$$

这个近似对小的立体角有效，上式通过仔细选择 $\mathbf{l}$ 可以使其扩展到大立体角情形，该点成为 Most Representative Point (MRP)。

retangle 立体角的计算有解析解[^UFK13]，但没有考虑 horizon handling。出于性能考虑，对 $\Omega_\text{light}​$ 的估计不考虑 horizon handling，直接计算直角椎体的立体角 rihgt pyramid solid angle[^Pla]。

```c++
1 float rightPyramidSolidAngle ( float dist , float halfWidth , float halfHeight )
{
    float a = halfWidth ;
    float b = halfHeight ;
    float h = dist ;
    
    return 4 * asin (a * b / sqrt ((a * a + h * h) * (b * b + h * h)));
}


float rectangleSolidAngle ( float3 worldPos ,
    float3 p0 , float3 p1 ,
    float3 p2 , float3 p3)
{
    float3 v0 = p0 - worldPos ;
    float3 v1 = p1 - worldPos ;
    float3 v2 = p2 - worldPos ;
    float3 v3 = p3 - worldPos ;

    float3 n0 = normalize ( cross (v0 , v1));
    float3 n1 = normalize ( cross (v1 , v2));
    float3 n2 = normalize ( cross (v2 , v3));
    float3 n3 = normalize ( cross (v3 , v0));

    float g0 = acos ( dot (-n0 , n1));
    float g1 = acos ( dot (-n1 , n2));
    float g2 = acos ( dot (-n2 , n3));
    float g3 = acos ( dot (-n3 , n0));

    return g0 + g1 + g2 + g3 - 2 * FB_PI ;
}
```

MRP 方法的质量依赖于立体角的准确估计。然而这估计较为困难，不适合于实时计算。

我们使用了替代方法 Stryctyre sampling of light shape

易知
$$
\int_{\Omega} f(x) \mathrm{dl}=\Omega \text { Average }[f(x)]
$$
因此，对于 illuminance 有
$$
E(n)=\int_{\Omega_{\text { light }}} L_{i n}\langle\mathbf{n} \cdot 1\rangle \mathrm{d} \mathbf{l}=\Omega_{\text { light }} L_{i n} \text { Average }[\langle\mathbf{n} \cdot \mathbf{1}\rangle]
$$
这个均值的难以求得，可以采样估计。对于 retangular llight，我们使用 4 个角点和中心点
$$
E(n)=\int_{\Omega_{\text{light}}} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l} \approx \Omega_{\text{light}} L_\text{in} \frac{1}{N} \sum_{i=1}^{N} \max \left(\left\langle\mathbf{n} \cdot \mathbf{l}_{i}\right\rangle, 0\right)
$$
这种方法通过 clamp 余弦值，隐式地考虑了 horizon handling。

这个方法有几乎不明显的 artifact，此由过少的样本产生。

![1561016204975](assets/1561016204975.png)

实现代码为

```c++
if ( dot ( worldPos - lightPos , lightPlaneNormal ) > 0)
{
    float halfWidth = lightWidth * 0.5;
    float halfHeight = lightHeight * 0.5;
    float3 p0 = lightPos + lightLeft * -halfWidth + lightUp * halfHeight ;
    float3 p1 = lightPos + lightLeft * -halfWidth + lightUp * - halfHeight ;
    float3 p2 = lightPos + lightLeft * halfWidth + lightUp * - halfHeight ;
    float3 p3 = lightPos + lightLeft * halfWidth + lightUp * halfHeight ;
    float solidAngle = rectangleSolidAngle ( worldPos , p0 , p1 , p2 , p3);

    float illuminance = solidAngle * 0.2 * (
    saturate ( dot( normalize (p0 - worldPos ), worldNormal ) +
    saturate ( dot( normalize (p1 - worldPos ), worldNormal ))+
    saturate ( dot( normalize (p2 - worldPos ), worldNormal ))+
    saturate ( dot( normalize (p3 - worldPos ), worldNormal ))+
    saturate ( dot( normalize ( lightPos - worldPos ), worldNormal )));
}
```

#### 4.7.2.6 Tube area light

在 Frostbite 中，tube area light 是一个 capsule（一个圆柱 + 2 个半球）。

![1561017008748](assets/1561017008748.png)

form factor 和 solid angle 都难以计算，难以实时计算。

我们将 capsule 分割为 1 个圆柱和 2 个半球，并利用之前的结果

- 圆柱体视为一个正对的等大 rectangular lihgt
- 两个半球视为一个位于圆柱轴上离着色点最近的位置的球
- 两者叠加

效果如下，很接近真值

![1561017730667](assets/1561017730667.png)

实现代码为

```c++
// Return the closest point on the line ( without limit )
float3 closestPointOnLine ( float3 a, float3 b, float3 c)
{
    float3 ab = b - a;
    float t = dot(c - a, ab) / dot (ab , ab);
    return a + t * ab;
}

// Return the closest point on the segment ( with limit )
float3 closestPointOnSegment ( float3 a, float3 b, float3 c)
{
    float3 ab = b - a;
    float t = dot(c - a, ab) / dot(ab , ab);
    return a + saturate (t) * ab;
}

// The sphere is placed at the nearest point on the segment .
// The rectangular plane is define by the following orthonormal frame :
float3 forward = normalize ( closestPointOnLine (P0 , P1 , worldPos ) - worldPos );
float3 left = lightLeft ;
float3 up = cross ( lightLeft , forward );

float3 p0 = lightPos - left * (0.5 * lightWidth ) + lightRadius * up;
float3 p1 = lightPos - left * (0.5 * lightWidth ) - lightRadius * up;
float3 p2 = lightPos + left * (0.5 * lightWidth ) - lightRadius * up;
float3 p3 = lightPos + left * (0.5 * lightWidth ) + lightRadius * up;

float solidAngle = rectangleSolidAngle ( worldPos , p0 , p1 , p2 , p3);

float illuminance = solidAngle * 0.2 * (
saturate ( dot ( normalize (p0 - worldPos ), worldNormal )) +
saturate ( dot ( normalize (p1 - worldPos ), worldNormal )) +
saturate ( dot ( normalize (p2 - worldPos ), worldNormal )) +
saturate ( dot ( normalize (p3 - worldPos ), worldNormal )) +
saturate ( dot ( normalize ( lightPos - worldPos ), worldNormal )));

// We then add the contribution of the sphere
float3 spherePosition = closestPointOnSegment (P0 , P1 , worldPos );
float3 sphereUnormL = spherePosition - worldPos ;
float3 sphereL = normalize ( sphereUnormL );
float sqrSphereDistance = dot ( sphereUnormL , sphereUnormL );

float illuminanceSphere = FB_PI * saturate ( dot ( sphereL , data . worldNormal )) *
    (( lightRadius * lightRadius ) / sqrSphereDistance );

illuminance += illuminanceSphere ;
```

### 4.7.3 Five times rule

当面光源与着色点距离比较大时，平方反比定律是可能可行的近似。一个经验规律是 the five times rule[^Rye]：*与光源的距离应该大于其直径的 5 倍*。

> *"the distance to a light source should be greater than five times the largest dimension of the sources"*  

在实践中并没有去做这个优化。

### 4.7.4 Diffuse area light with Disney diffuse

之前的推导中没有使用 Disney diffuse，我们只对一个光源方向进行计算，公式为
$$
L_{o u t}=f_{d}(\mathbf{v}, \mathbf{l}) E(n)
$$
这个光源方向可以用光源位置进行计算，也可以利用 Drobot 方法中的 MRP。

对比如下

![1561019316021](assets/1561019316021.png)

MRP 更接近于真值。

### 4.7.5 Specular area lights

specular area light 在实时的限制下非常复杂。BRDF 的参数多，光源配置参数多使得其难以预计算。

最终我们使用了 Karis 的 shortest distance form reflection ray 方法[^Kar13]，能量守恒存在问题，并且在 grazing angle 处表现不好。

效果如下（左图为 Karis 方法，右图为参考）

![1561020266975](assets/1561020266975.png)

用 BRDF 的 dominant direction 去替代反射方向有微小的提升

![1561020406621](assets/1561020406621.png)

```c++
float3 getSpecularDominantDirArea ( float3 N, float3 R, float NdotV , float roughness )
{
    // Simple linear approximation
    lerpFactor = (1 - roughness );
    
    return normalize ( lerp (N, R, lerpFactor ));
}
```

## 4.8 Emissive surfaces

## 4.9 Image besed lights

## 4.10 Shadow and occlusion

## 4.11 Deferred / Forward rendering

# 5. 图像 Image



# 6. 转移到 PBR Transition to PBR



# 参考文献

[^Bur12]: B. Burley. "[**Physically Based Shading at Disney**](http://selfshadow.com/publications/s2012-shading-course/)". In: Physically Based Shading in Film and Game Production, ACM SIGGRAPH 2012 Courses. SIGGRAPH ’12. Los Angeles, California: ACM, 2012, 10:1{7. isbn: 978-1-4503-1678-1. doi: 10.1145/2343483.2343493.

[^CH05]: G. Coombe and M. Harris. "**Global Illumination Using Progressive Refinement Radiosity**". In: GPU Gems 2. Ed. by M. Pharr. Addison-Wesley, 2005, pp. 635-647.

[^Dro13]: M. Drobot. "[**Lighting of Killzone: Shadow Fall**](http://www.guerrilla-games.com/publications/)". In: Digital Dragons. 2013.

[^Dro14b]: M. Drobot. "**Physically Based Area Lights**". In: GPU Pro 5. Ed. by W. Engel. CRC Press, 2014, pp. 67-100.

[^Hei14]: E. Heitz. "[**Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs**](http://jcgt.org/published/0003/02/03/)". In: Journal of Computer Graphics Techniques (JCGT) 3.2 (June 2014), pp. 32-91. issn: 2331-7418.

[^HSM10b]: J. R. Howell, R. Siegel, and M. P. Meng¨u¸c. 2010. http://www.thermalradiation.net/sectionb/B-13.html

[^Kar13]: B. Karis. "[**Real Shading in Unreal Engine 4**](http://selfshadow.com/publications/s2013-shading-course/)". In: Physically Based Shading in Theory and Practice, ACM SIGGRAPH 2013 Courses. SIGGRAPH ’13. Anaheim, California: ACM, 2013, 22:1-22:8. isbn: 978-1-4503-2339-0. doi: 10.1145/2504435.2504457.

[^Koj+13]: H. Kojima, H. Sasaki, M. Suzuki, and J. Tago. "[**Photorealism Through the Eyes of a FOX: The Core of Metal Gear Solid Ground Zeroes**](http://www.gdcvault.com/play/1018086/Photorealism-Through-the-Eyes-of)". In: Game Developers Conference. 2013.

[^LH13]: S. Lagarde and L. Harduin. "[**The Art and Rendering of Remember Me**](http://seblagarde.wordpress.com/2013/08/22/gdceurope-2013-talk-the-art-and-rendering-of-remember-me/)". In: Game Developers Conference Europe. 2013.

[^Mar14]: I. Mart´ınez. [**Radiative view factors**](http://webserver.dmt.upm.es/~isidoro/tc3/Radiation%5C%20View%5C%20factors.pdf). 1995-2014.

[^Pla]: PlanetMath. [**Solid angle of rectangular pyramid**](http://planetmath.org/solidangleofrectangularpyramid).

[^Qui06]: I. Qu´ılez. [**Sphere ambient occlusion**](http://www.iquilezles.org/www/artiles/sphereao/sphereao.htm). 2006.

[^Rye]: A. Ryer. [**Light Measurement Handbook**](http://www.intl-lighttech.com/services/ilt-light-measurement-handbook). International Light Technologies Inc.

[^UFK13]: C. Ure~na, M. Fajardo, and A. King. “[**An Area-Preserving Parametrization for Spherical Rectangles**](https://www.solidangle.com/arnold/research/ )". In: Computer Graphics Forum 32.4 (2013), pp. 59-66. doi: 10.1111/cgf. 12151。

