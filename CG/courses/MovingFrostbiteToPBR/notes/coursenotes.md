# 目录

[TOC]

# 1. 导论 Introduction

基于 Killzone Shadow Fall [^Dro13]，Unreal Engine 4 [^Kar13]，Remember Me [^LH13] 和 Metal Gear Solid V: Ground Zeroes [^Koj+13]，Frostbite 转移到 PBR。在此基础上，试图进一步**完善现有的技术**，并逐步**解决该领域的公开问题**。

在适当的近似下，我们更喜欢提升图像质量的**可信度** believability 而不是绝对正确性 absolute correctness。

PBR的核心原则之一就是**材料和灯光信息的解耦** decoupling，这对于确保场景中所有对象之间的视觉**一致性**至关重要，有助于跨环境**重用**资源 assets 和照明设备 lighting rigs，减少了向 artists 公开的参数数量，使创作更加**直观**。

转移到 PBR 需要更新整个图形管线（渲染器和工具）。

记号

![1560865143498](assets/1560865143498.jpg)

# 2. 参考 Reference

### 2.1 验证模型和假设 Validating models and hypothesis 

**观察并与现实世界进行比较**是做出正确选择并判断一项技术或方法的相关性的最佳方法。

![1560865484659](assets/1560865484659.jpg)

然而准确测量真实数据很复杂或者需要花费大量时间。特定的数据库如 MERL 可以获取这些数据以帮助快速检验模型。

### 2.2 Validating in-engine approximations

现代的 PBR 路径追踪器如 Mitsuba 实现了先进的渲染技术，可以创建十分真实的画面。Frostbite 中有一个简单的输出器 exporter 用于 Mitsuba，这使我们能够快速评估估算值的有效性。

可以输出几何体 geometry、常量材质信息 constant material information（i.e. 没有纹理 textures）和所有光源 light source。我们可以检验材质模型，光积分和光强。

![1560866112378](assets/1560866112378.jpg)

### 2.3 Validating in-engine reference mode

为了加速，我们增加了一个引擎内置的参考模式，用 GPU 实现的。渲染时间并不快，但是迭代时间比我们的简单导出器快一个数量级。

> 渲染速度不快。。。。。太尴尬了。。。。。
>
> 好吧迭代速度快点就快点吧，原本也就几秒搞定，快能快到哪去。。。。。

![1560866942375](assets/1560866942375.jpg)

# 3. 材质 Material

## 3.1 材质模型 Material models

### 3.1.1 外观 Appearance 

![1560924180465](assets/1560924180465.jpg)

不同的外观可根据物理属性（如 conductivity，mean-free-path，absorption）分类。

BSDF 模型可分为反射部分 BRDF 和透射部分 BTDF。本文只关注反射部分和一个特定的材质模型，其可表示“标准”外观。

### 3.1.2 材质模型 Material models

所使用的标准材质模型可分成两部分

- 低角频率信号 low angular frequency signal，称为 diffuse，记为 $f_d$ 
- 低到高角频率信号 low to hight angular frequency，称为 specular，记为 $f_r$ 

![1560924923148](assets/1560924923148.jpg)

一个平坦的表面可以用菲涅尔定律来表示，对于不平坦的表面，可以使用微平面模型。

![1560925155675](assets/1560925155675.jpg)

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

![1560926027093](assets/1560926027093.jpg)

高粗糙度下，height-correlated 版本更亮一些。

对于 diffuse，$f_m$ 遵循 Lambertian 模型，因此有
$$
f_{d}(\mathbf{v})=\frac{\rho}{\pi} \frac{1}{|\mathbf{n} \cdot \mathbf{v}||\mathbf{n} \cdot 1|} \int_{\Omega} G(\mathbf{v}, 1, \mathbf{m}) D(\mathbf{m}, \alpha)\langle\mathbf{v} \cdot \mathbf{m}\rangle\langle\mathbf{1} \cdot \mathbf{m}\rangle \mathrm{d} \mathbf{m}
$$
往常 $f_d$ 被视为简单的 Lambertian 模型，然而 diffuse 部分应该与 specular 一致，并且考虑 `roughness`[^Bur12]。上式没有解析解，Burley[^Bur12] 给出了经验公式，考虑了 `roughness` 并且在 grazing angles 处有回射 retro-reflection
$$
\begin{aligned}

f_{d}&=\frac{\rho}{\pi}\left(1+F_{D 90}(1-\langle\mathbf{n} \cdot 1\rangle)^{5}\right)\left(1+F_{D 90}(1-\langle\mathbf{n} \cdot \mathbf{v}\rangle)^{5}\right)\\

F_{D 90}&=0.5+\cos \left(\theta_{d}\right)^{2} \alpha\\

\end{aligned}
$$

> $\theta_d$ 不知道指什么

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

![1560927690240](assets/1560927690240.jpg)

![1560927800844](assets/1560927800844.jpg)

### 3.1.4 形态特征 Shape characteristics

specular 有两个容易被忽视但有重要影响的现象

- Half-angle parametrization：BRDF形状发生非线性变换，即从正常入射角的各向同性向掠射角的各向异性转变，详见[4.9 节](#4.9)。

- Off-specular：经常假设 BRDF 的 lobe 中心在反射方向附近，然而由于 $\langle\mathbf{n} \cdot 1\rangle$ 和 G，当 `roughness` 增大时，BRDF 的 lobe 会朝向法向偏移，称为 Off-specular peak。lobe 的中心方向称为 dominant direction

  ![1560928607758](assets/1560928607758.jpg)

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
  - metallic: $F_0$ 

- Smoothness: $\text{smoothness}=1-\alpha_\text{lin}$ 

- MetalMask: metalness, mask 用于暗示 artist 这个值是 binary

- Reflectance: $F_0=0.16\ \text{reflectance}^2$ 

  ![1560930607656](assets/1560930607656.jpg)

`roughness` 使用了平方映射

![1560930438896](assets/1560930438896.jpg)

相应的 GBuffer layout 如下

![1560930663756](assets/1560930663756.jpg)

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

![1560942163731](assets/1560942163731.jpg)

## 4.3 光单位 Light unit

> 细节很多，较难把握

photometry 本质上是根据人眼的灵敏度加权的 radiometry。

![1560942485636](assets/1560942485636.jpg)

人眼灵敏度用 CIE photometric curve $V(\lambda)$ 表示。

![1560942704697](assets/1560942704697.jpg)

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

![1560943664320](assets/1560943664320.jpg)

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

![1560945333299](assets/1560945333299.jpg)

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

![1560950205681](assets/1560950205681.jpg)

> ...

artists 可以使用 IES 作为 mask 来制造阴影

![1560950453717](assets/1560950453717.jpg)

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

![1560999695226](assets/1560999695226.jpg)
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

  ![1561001291033](assets/1561001291033.jpg)

- Luminance：描述了表面功率。总能量与光源大小相关。光源产生的高光不随光源大小变化。

  ![1561003297325](assets/1561003297325.jpg)

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

![1561004226932](assets/1561004226932.jpg)

> 示例
>
> ![1561006970735](assets/1561006970735.jpg)
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
  > ![1561008742943](assets/1561008742943.jpg)
  >
  > 绿色部分是正确部分，可以看到对于大球光源，正确的部分变少了

- "Pathch to a sphere tilted"[^Mar14] correctly handling the horizon

两种方法的适用情况如下

![1561009706360](assets/1561009706360.jpg)

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

![1561011234921](assets/1561011234921.jpg)

> 示例
>
> ![1561011457738](assets/1561011457738.jpg)
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

![1561012808956](assets/1561012808956.jpg)

没有找到考虑了 horizon handling 的简单 form factor 解决方案。因此得使用替代方案。

Drobot 给出了近似解，利用了一个最具代表性的 diffuse point lihgt 加以立体角权重
$$
E(\mathbf{n})=\int_{\Omega_{\text { light }}} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l} \approx \Omega_{\text { light }} L_\text{in}\langle\mathbf{n} \cdot \mathbf{l}\rangle
$$

这个近似对小的立体角有效，上式通过仔细选择 $\mathbf{l}$ 可以使其扩展到大立体角情形，该点成为 Most Representative Point (MRP)。

retangle 立体角的计算有解析解[^UFK13]，但没有考虑 horizon handling。出于性能考虑，对 $\Omega_\text{light}$ 的估计不考虑 horizon handling，直接计算直角椎体的立体角 rihgt pyramid solid angle[^Pla]。

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

![1561016204975](assets/1561016204975.jpg)

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

![1561017008748](assets/1561017008748.jpg)

form factor 和 solid angle 都难以计算，难以实时计算。

我们将 capsule 分割为 1 个圆柱和 2 个半球，并利用之前的结果

- 圆柱体视为一个正对的等大 rectangular lihgt
- 两个半球视为一个位于圆柱轴上离着色点最近的位置的球
- 两者叠加

效果如下，很接近真值

![1561017730667](assets/1561017730667.jpg)

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

![1561019316021](assets/1561019316021.jpg)

MRP 更接近于真值。

### 4.7.5 Specular area lights

specular area light 在实时的限制下非常复杂。BRDF 的参数多，光源配置参数多使得其难以预计算。

最终我们使用了 Karis 的 shortest distance form reflection ray 方法[^Kar13]，能量守恒存在问题，并且在 grazing angle 处表现不好。

效果如下（左图为 Karis 方法，右图为参考）

![1561020266975](assets/1561020266975.jpg)

用 BRDF 的 dominant direction 去替代反射方向有微小的提升

![1561020406621](assets/1561020406621.jpg)

```c++
float3 getSpecularDominantDirArea ( float3 N, float3 R, float NdotV , float roughness )
{
    // Simple linear approximation
    lerpFactor = (1 - roughness );
    
    return normalize ( lerp (N, R, lerpFactor ));
}
```

## 4.8 Emissive surfaces

在 Frostbite 中，emissive lights 用来显示光源表面，面光源用来发光。

emissive light 在着色器中以像素精度生成，需要提供发光颜色和发光强度值，不发光，只是用于显示颜色。可以产生 blooming。

有三种 emissive surface

![1561021638831](assets/1561021638831.jpg)

在 Frostbite 中支持 case B，并隐式支持 case C。

渲染方法有四种

- Transparent objects: Emissive applied during the rendering of the surface. 
- Forward opaque objects: Emissive applied during the rendering of the surface.
- Deferred lit opaque objects with full emissive: Emissive applied in an extra rendering pass of the surface: the surface is rendered twice.
- Deferred lit opaque objects with cheap emissive: Emissive stored in the radiosity buffer, and applied at the same time as the indirect lighting.

引擎自动给光源生产了 emissive shape

![1561023115315](assets/1561023115315.jpg)

## 4.9 Image besed lights

IBL 使得我们可以表示一个点的入射光。这个光源会影响 BRDF 的 diffuse 和 specular。

需要计算光照积分
$$
L(\mathbf{v})=\int_{\Omega} f(\mathbf{l}, \mathbf{v}, \Theta) L(\math bf{l}) \mathrm{d} \mathbf{l}
$$
其中 $\Theta$ 指 Fresnel、`roughness`、`albedo` 等等。

我们使用了四种类型的 IBL[^Dro13] 

- Distant light probe: parallax-free far lighting, least accurate
- Local light probes: local lighting with parallax, cubemap
- Screen-space reflections: close-range lighting (supporting glossy reflection), ray  marching
- Planar reflections: an alternative to SSR, rendering the scene mirrored by a plane

static vs. dynamic：Distant 和 local light probes 是 static 的。他们的内容可以根据需求进行更新。SSR 和 planar reflection 包含了动态光照信息，他们每一帧都更新，因为他们与视角相关，计算可以分摊在多帧中。

### 4.9.1 Light probes acquisition and unit

IBL 与 image 关联

#### 4.9.1.1 Distant light probe

distant light probes 捕获了周围环境，表示成 cubemap。artists 有两种方式获取 distant light probe：

- 用基于物理的天空
- 用真实世界的相机捕获 High Dynamic Range Image HDRI

Frostbite 使用了基于物理的天空，可按需求更新（时间、天气变化）。

HDRI 中应移除强光源，以减少预积分的噪声和处理他们的可见性，如太阳。

#### 4.9.1.2 Local light probes

local light probe 在有限区域内捕获周围物体，可根据需求进行更新。

有几个渲染问题

- order-dependency：local light probe 应在渲染场景前完成处理
- metallic surface：金属表面是病态的因为他们没有 difuse 且在捕获期没有 specular。我们可以多次捕获 local light probe 来模拟 light bounces。或者依赖于 distant light probe，然而不适用于室内环境。
- view-dependent effects：local light probe 在某点进行捕获，glossy 和 mirror-like 表面的入射光对于视点来说不适用。

为了解决这些问题，为了解决这个问题，捕获时不考虑 specular。对于金属表面，他们近似成漫反射表面，用 $F_0$ 来作为 albedo。捕获时同时保存了可见性，存储在 alpha 通道中。

> 示例
>
> ![1561111432388](assets/1561111432388.jpg)

### 4.9.2 Light probe filtering

此部分的内容大多同于我之前写的文章 [深入理解 PBR/基于图像的照片 IBL](https://zhuanlan.zhihu.com/p/66518450)，不再赘述。

有一些不同之处或细节之处

- LD 项用 cos weighted hemisphere 采样

- LUT 的大小 128 * 128 足够了

- pre-filter environment map 256 * 256 或 512 * 512

- Disney diffuse 分成了 DFG 和 LD 项

- mipmap 不是 roughness 的线性形式，而是

  $$
  \text{mipLevel}=\sqrt{\alpha_{\text { lin }}}\text{mipCount}
  $$

### 4.9.3 Light probe evaluation

diffuse 和 specular 的 pre-integrations 都是 view-independent，而 diffuse 和 specular 是 view dependent。这意味着他们的 lobe direction 依赖于视线方向。对于 specular，我们计算 BRDF 时使用 principal direction 而不是 mirror reflection 来获取 pre-integrated 值。

highest value direction 依赖于视角和粗糙度。我们提出的模型不能正确捕获电介质在低视角的表现。这是因为实际的 lobe 只浮出了一点点，但因为 Fresnel 随视角增加较慢，因此影响不大。

```c++
// This is an accurate fitting of the specular peak ,
// but due to other approximation in our decomposition it doesn ’t perform well
float3 getSpecularDominantDir ( float3 N, float3 R, float NdotV , float roughness )
{
#if GSMITH_CORRELATED
    float lerpFactor = pow (1 - NdotV , 10.8649) * (1 - 0.298475 * log (39.4115 - 39.0029 *
        roughness )) + 0.298475 * log (39.4115 - 39.0029 * roughness );
# else
    float lerpFactor = 0.298475 f * NdotV * log (39.4115 f - 39.0029 f * roughness ) + (0.385503 f -
        .385503 f * NdotV ) * log (13.1567 f - 12.2848 f * roughness );
# endif

    // The result is not normalized as we fetch in a cubemap
    return lerp (N, R, lerpFactor );
}
```

用一个简单的近似效果更好

```c++
// We have a better approximation of the off specular peak
// but due to the other approximations we found this one performs better .
// N is the normal direction
// R is the mirror vector
// This approximation works fine for G smith correlated and uncorrelated
float3 getSpecularDominantDir ( float3 N, float3 R, float roughness )
{
    float smoothness = saturate (1 - roughness );
    float lerpFactor = smoothness * ( sqrt ( smoothness ) + roughness );
    // The result is not normalized as we fetch in a cubemap
    return lerp (N, R, lerpFactor );
}
```

比较结果如下

![1561172589487](assets/1561172589487.jpg)

可见高粗糙度下，mirror direction 误差较大。

对于 Disney diffuse，dominant direction 依赖于视线方向。一个简单的线性模型就能相对准确地捕获这种行为。

```c++
// N is the normal direction
// V is the view vector
// NdotV is the cosine angle between the view vector and the normal
float3 getDiffuseDominantDir ( float3 N, float3 V, float NdotV , float roughness )
{
    float a = 1.02341 f * roughness - 1.51174 f;
    float b = -0.511705 f * roughness + 0.755868 f;
    lerpFactor = saturate (( NdotV * a + b) * roughness );
    // The result is not normalized as we fetch in a cubemap
    return lerp (N, V, lerpFactor );
}
```

对于 distant Light，diffuse 和 specular 的计算如下

```c++
float3 evaluateIBLDiffuse (...)
{
    float3 dominantN = getDiffuseDominantDir (N, V, NdotV , roughness );
    float3 diffuseLighting = diffuseLD . Sample ( sampler , dominantN );

    float diffF = DFG . SampleLevel ( sampler , float2 (NdotV , roughness ), 0).z;

    return diffuseLighting * diffF ;
}

float3 evaluateIBLSpecular (...)
{
    float3 dominantR = getSpecularDominantDir (N, R, NdotV , roughness );
    
    // Rebuild the function
    // L . D. ( f0.Gv .(1 - Fc) + Gv.Fc ) . cosTheta / (4 . NdotL . NdotV )
    NdotV = max (NdotV , 0.5 f/ DFG_TEXTURE_SIZE );
    float mipLevel = linearRoughnessToMipLevel ( linearRoughness , mipCount );
    float3 preLD = specularLD . SampleLevel ( sampler , dominantR , mipLevel ). rgb ;
    
    // Sample pre - integrate DFG
    // Fc = (1-H.L)^5
    // PreIntegratedDFG .r = Gv .(1 - Fc)
    // PreIntegratedDFG .g = Gv.Fc
    float2 preDFG = DFG . SampleLevel ( sampler , float2 (NdotV , roughness ), 0).xy;

    // LD . ( f0.Gv .(1 - Fc) + Gv.Fc. f90 )
    return preLD * (f0 * preDFG .x + f90 * preDFG .y);
}
```

修改后的 Disney diffuse BRDF 保证了能量守恒。

未来考虑周围环境的视差，local light probe需要使用代理几何体来重投影光照信息。Frostbite 支持 sphere 和 oriented box，由 artist 手动放置。运行时，在 locla light probe 内的物体会计算采样方向与 proxy geometry 的交点，然后用校正的方向来进行 local light probe 的相关计算[^LZ12]。对于高粗糙度情形，这种校正会产生 artifact，我们用 roughness 在校正方向与原方向之间插值。此外还可以移动 cubemap 的中心。

local light probe 只用于 specular 部分，详见 [Appendix F. Local light probe evaluation](#F. Local light probe evaluation)。对于漫反射项，光照信息来自于 light map 或 probe voulumes，用 retro-reflective lobe 的 dominant direction。

BRDF lobe 描述了入射光的积分情况，会使得 BRDF 的 footprint  与距离相关。如果物体离着色点近时，反射的该物体会较为清晰，否则会模糊。

![1561178724148](assets/1561178724148.jpg)

> 示例
>
> ![1561178735756](assets/1561178735756.jpg)

local light probe proxy geometry 允许我们计算入射光与着色点的距离，以此大概估计 BRDF 的 footprint，并在估计中考虑了 roughness，称为 "distance based roughness"
$$
\alpha'=\frac{\text{distanceInteresectionToShadedPoint}}{\text{distanceInteresectionToProbeCenter}}\alpha
$$
这是一个很粗糙的估计，并且只对地粗糙度情形合理，对高粗糙度不合理，因此最后还对两者用粗糙度做线性插值。

```c++
float computeDistanceBaseRoughness (
    float distInteresectionToShadedPoint ,
    float distInteresectionToProbeCenter ,
    float linearRoughness )
{
    // To avoid artifacts we clamp to the original linearRoughness
    // which introduces an acceptable bias and allows conservation
    // of mirror reflection behavior for a smooth surface .
    float newLinearRoughness = clamp ( distInteresectionToShadedPoint /
    distInteresectionToProbeCenter * linearRoughness , 0, linearRoughness );
    return lerp ( newLinearRoughness , linearRoughness , linearRoughness );
}
```

当 SSR 失败时才会使用 local light probe。

### 4.9.4 Screen space reflections

SSR 能捕获接近中距（短距）的反射并且对小物体/小细节很重要。我们的技术依赖于建立在场景深度缓冲区之上的分层 z （Hierarchical-Z，Hi-Z）结构，可以快速追踪长光线，尽可能使用屏幕信息，称为 "Hi-Z Screen-Space Cone-Traced Reflections"[^Ulu14]。

emissive 只是视觉的，而 SSR 会将其考虑进去，因此相当于计算了两次光照，没法简单解决这个问题。

### 4.9.5 Image based lights composition

每种 IBL 类型代表不同的入射光，并且有各自的限制。为了能够让一个对象不断地适应它的环境，我们以分层的方式组合了所有这些 IBL。

SSR 是很好的获取正确反射的方式，但由于屏幕空间的限制，其经常失败。当 SSR 失败后，就用 local light probe。local light probes 根据层级来计算，从小至大，直到得到反射信息，否则用 distant light probe。

``` pascal
// Short range reflections
Evaluate SSR
RGB = SSR.rgb
Alpha = SSR.a
// Medium range reflections
while local light probes and Alpha < 1 do
    Evaluate local light probe
    a = saturate(localLightProbe.a - Alpha)
    RGB += localLightProbe.rgb * a
    Alpha = saturate(a + Alpha)
// Large range reflections
if Alpha < 1 then
    Evaluate distant light probe
    RGB += distantLightProbe.rgb * (1-Alpha)
```

如果 local light probe 对应像素有物体的话，则 alpha 为 1。

> 示例
>
> ![1561185593601](assets/1561185593601.jpg)
>
> 光线 1 可从绿 local light probe 中得 alpha 为 1，停止
>
> 光线 2 可从绿 local light probe 中得 alpha 为 0，因此继续在红 local light probe 中得 为 1，停止
>
> 光线 2 可从绿 local light probe 中得 alpha 为 0，因此继续在红 local light probe 中得 为 0，因此使用 distant light probe

此外还有 planar reflection，作为 SSR 的替代。（原文没有详细叙述）

## 4.10 Shadow and occlusion

### 4.10.1 Diffuse occlusion

环境光的渲染方程为
$$
L(\mathbf{v})=\int_{\Omega} f(\mathbf{l}, \mathbf{v}) L_{a}( \mathbf{l}) V(\mathbf{l})\langle\mathbf{n} \cdot \mathbf{1}\rangle
$$
$L_a$ 是环境光。一个粗糙的假设是将 V 分离出积分。
$$
L(\mathbf{v})\approx\left[\pi \int_{\Omega} f(\mathbf{l}, \mathbf{v}) L_{a}(\mathbf{l}) \mathrm{d} \mathbf{l}\right]\left[\frac{1}{\pi} \int_{\Omega} V(\mathbf{l})\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d} \mathbf{l}\right]
$$
这个分离只在 $f_r(\mathbf{l},\mathbf{v})$ 和 $L_a(\mathbf{l})$ 是常数时成立（用 constant distant light 照射 Lambertian 表面）。右边的是一个 $[0,1]$ 的标量，指示一个点可达性。

ambient occlusion 定义为
$$
A O=1-\frac{1}{\pi} \int_{\Omega} V(\mathbf{l})\langle\mathbf{n} \cdot \mathbf{l}\rangle \mathrm{d}\mathbf{l}
$$
游戏中，一般将预计算结果放在 light map，cubemap 或球谐函数 spherical harmonics 中。烘焙时缺乏场景动态物体的信息。运行时可与其他信息混合。

### 4.10.2 Specular occlusion

ao 只是用于 Lambertian 表面，对应的是 diffuse lighting。而 specular 的遮挡很难搞定，这会导致 light leaking。

> 示例
>
> ![1561188855724](assets/1561188855724.jpg)

使用 ao 来直接处理 specular 是不合理的。

Kozlowski[^KK07]强调，绝大多数光滑的场景都可以在一定程度上近似，而使用球谐函数的方向环境遮挡近似是最有效的方法。

Gotanda[^Got13]提出了一种由 ao 导出的 specula人occlusion。Frostbite 使用了相近的方法

```c++
float computeSpecOcclusion ( float NdotV , float AO , float roughness )
{
    return saturate (pow( NdoV + AO , exp2 ( -16.0 f * roughness - 1.0 f)) - 1.0 f + AO);
}
```

> 示例
>
> 对于 ao = 0.5 时，函数图像为
>
> ![1561191803953](assets/1561191803953.jpg)

对比

![1561191993995](assets/1561191993995.jpg)

### 4.10.3 Multi resolution ambient occlusion

有两类技术来生成漫反射遮蔽因子

- Offline pre-computation：捕获中短程遮挡信息
- Screen space techniques：捕获中程遮挡信息，有多种方法（HBAO，SSAO，VolumetricAO，ambient obscurance）

这些方法没法解决短距遮挡。我们将遮挡分成 small，medium 和 large 三挡。

Frostbite 用贴图来表达小遮挡。分成 diffuse 和 specular 两部分。

- diffuse micro-occlusion：视角无关，直接将预计算结果乘进 albedo 贴图中

  > 示例
  >
  > ![1561192569761](assets/1561192569761.jpg)
  >
  > 左 ao，中 diffuse micro-occlusion，右 albedo + diffuse micro-occlusion

  

- specular micro-occlusion：视角相关，使用了 Schuler 的方法[^Sch09]。

  ```c++
  f90 = saturate (50.0 * dot ( fresnel0 , 0.33) );
  
  float3 F_Schlick (in float3 f0 , in float f90 , in float u)
  {
      return f0 + ( f90 - f0) * pow (1. f - u, 5.f);
  }
  ```

  直接将 specular micro-occlusion 可以 pre-backed 入 reflectance texture 中。

  > 没看懂这种操作

medium 和 large 遮挡只作用于 indirect lighting，使用了 HBAO，可以提供来自动态物体的阴影，同时提供 ao，两者取最小值。

总结如下

- Direct diffuse: Diffuse micro-occlusion 
- Indirect diffuse: Diffuse micro-occlusion, min(bakedAO, HBAO)
- Direct specular: Fresnel reflectance modification through specular micro-occlusion
- Indirect specular: Fresnel reflectance modification through specular micro-occlusion then computeSpecularOcclusion(NdotV, min(bakedAo, HBAO), roughness)

### 4.10.4 Shadows

理想上，所有 lights 都应该有 shadow，但开销过大。通常依赖于 artist 来隐藏阴影的缺失。

软阴影对面光源很重要

![1561194092304](assets/1561194092304.jpg)

Frostbite 只支持点和 spot light 的光照贴图，这些 shadow map 用来支持所有光照类型。为了实现 area shadows，可以将投影中心往光照方向后移，并通过 heavy blurring 和低解析度来完成。

![1561194402256](assets/1561194402256.jpg)

## 4.11 Deferred / Forward rendering

Frostbite 支持 deferred 和 forward 混合渲染。支持 tiled path 和 light culling。用一个大循环来计算所有光源来减少读取 GBuffer 的带宽消耗和增加计算精度。

# 5. 图像 Image

## 5.1 A Physically Based Camera

前面所有的部分都集中在光线如何在场景中以一种基于物理的方式进行交互。要获得可信的结果，另一个重要的考虑因素是考虑从场景亮度到最终像素值的整个转换链。

### 5.1.1 Camera settings

由于在渲染管线中我们一直处理的是 photometric units，最后到达 camera 的能量也用 luminance 表示。入射光通常覆盖了很大范围的值。因此这些值需要映射到一个标准化的像素值来生成最后的图像。

![1561203907171](assets/1561203907171.jpg)

在数字相机中，这个过程通过曝光 exposing 一段时间后在进行一些后处理 post-process。

> *The purpose of this exposition is to maximize the sensor latitude by centring the current light range to halfway between white and dark (middle grey) and setting up the object of interest in the middle of the image range* 

变换的完整管线如下

![1561204215226](assets/1561204215226.jpg)

- 相对孔径 relative aperture（N，单位光圈 f-stops）：控制孔径大小，影响景深

- 快门时间 shutter time （t，单位秒）：控制孔径打开时间，影响运动模糊

- 传感器灵敏度 sensor sensitivity/gain（S，单位 ISO）：控制光子的影响因子

  > https://fotomen.cn/2018/06/25/what-ios/

给定参数后，可以用 Exposure Value (EV) 整合。ISO 100 的 EV，记为 $EV_\text{100}$，有关系
$$
E V_{100}=\log _{2}\left(\frac{N^{2}}{t}\right)-\log _{2}\left(\frac{S}{100}\right)
$$
不同的参数组合可以得到相同的 EV，这使得 artist 可以在 motion blur、depth of field 和 noise 中做权衡

![1561205743568](assets/1561205743568.jpg)

> 示例
>
> ![1561208087769](assets/1561208087769.jpg)
>
> abc 只变化了光圈大小
>
> def 通过调整 ISO 使得 EV 不变

除了 apeture、shutter speed 和 sensitivity，artist 还能使用曝光补偿 exposure compensation（EC，单位光圈）来 over-expose 或 under-expose 图像，通常只是曝光值的偏移
$$
E V_{100}^{\prime}=E V_{100}-E C
$$

> [正确掌握曝光补偿](https://fotomen.cn/2009/09/17/baoguang/) 

相机可以将入射光转变成 EV。
$$
E V_{100}=\log _{2}\left(\frac{L_{\mathrm{avg}} S}{K}\right)
$$
其中 S 是 ISO，K 是 reflected-light meter calibration constant，$K=12.5$。游戏中，通常平均所有像素的 log luminance 来得到 $L_\text{avg}$（算出的值应该是 $\log_2{L_\text{avg}}$），为了稳定，可以使用 histogram 来移除过大值。

### 5.1.2 Exposure

EV 不同于 luminous exposure 或 photometric exposure H，描述了到达传感器的 luminance，定义为
$$
H=\frac{q t}{N^{2}} L
$$
其中 L 是 incident luminance，q 是透镜和光晕衰减 lens and vignetting attenuation（经典值为 0.65）。

ISO 定义了三种关联 H 和 sensityvity 的方式

- SOS: Standard Output Sensitivity
- SBS: Saturation Based Sensitivity
- NSB: Noise Based Sensitivity

SBS 是为不会导致相机输出 clipped or bloomed 的最大可能曝光量，关系为
$$
H_{\mathrm{sbs}}=\frac{78}{S_{\mathrm{sbs}}}
$$
可推得
$$
\begin{aligned} H_{\mathrm{sbs}} &=\frac{78}{S} \\ \frac{q t}{N^{2}} L_{\max } &=\frac{78}{S} \\ L_{\max } &=\frac{78}{S} \frac{N^{2}}{q t} \end{aligned}
$$
最终的像素值可以用 $L_\text{max}$ 来标准化其 incident luminance。

代码实现如下

```c++
float computeEV100 ( float aperture , float shutterTime , float ISO )
{
    // EV number is defined as:
    // 2^ EV_s = N^2 / t and EV_s = EV_100 + log2 (S /100)
    // This gives
    // EV_s = log2 (N^2 / t)
    // EV_100 + log2 (S /100) = log2 (N^2 / t)
    // EV_100 = log2 (N^2 / t) - log2 (S /100)
    // EV_100 = log2 (N^2 / t . 100 / S)
    return log2 ( sqr ( aperture ) / shutterTime * 100 / ISO );
}

float computeEV100FromAvgLuminance ( float avgLuminance )
{
    // We later use the middle gray at 12.7% in order to have
    // a middle gray at 18% with a sqrt (2) room for specular highlights
    // But here we deal with the spot meter measuring the middle gray
    // which is fixed at 12.5 for matching standard camera
    // constructor settings (i.e. calibration constant K = 12.5)
    // Reference : http :// en. wikipedia . org / wiki / Film_speed
    return log2 ( avgLuminance * 100.0 f / 12.5 f);
}

float convertEV100ToExposure ( float EV100 )
{
    // Compute the maximum luminance possible with H_sbs sensitivity
    // maxLum = 78 / ( S * q ) * N^2 / t
    // = 78 / ( S * q ) * 2^ EV_100
    // = 78 / (100 * 0.65) * 2^ EV_100
    // = 1.2 * 2^ EV
    // Reference : http :// en. wikipedia . org / wiki / Film_speed
    float maxLuminance = 1.2 f * pow (2.0f, EV100 );
    return 1.0 f / maxLuminance ;
}

// usage with manual settings
float EV100 = computeEV100 ( aperture , shutterTime , ISO );
// usage with auto settings
float AutoEV100 = computeEV100FromAvgLuminance ( Lavg );

float currentEV = useAutoExposure ? AutoEV100 : EV100 ;
float exposure = convertEV100toExposure ( currentEV );

// exposure can then be used later in the shader to scale luminance
// if color is decomposed into XYZ
...
float exposedLuminance = luminance * exposure ;
...
// or it can be applied directly on color
...
finalColor = color * exposure
...
```

### 5.1.3 Emissive and bloom effects

```c++
float3 computeBloomLuminance ( float3 bloomColor ,
float bloomEC , float currentEV )
{
    // currentEV is the value calculated at the previous frame
    float bloomEV = currentEV + bloomEC ;
    // convert to luminance
    // See equation (12) for explanation about converting EV to luminance
    return bloomColor * pow (2, bloomEV -3) ;
}
```

> 没有怎么讲 bloom 的细节。。。

### 5.1.4 Sunny 16

...

### 5.1.5 Color space

一般用 sRGB，常见的问题是用 gamma 2.2，这可以用更精确的公式代替，如代码所示

```c++
float3 approximationSRgbToLinear (in float3 sRGBCol )
{
    return pow ( sRGBCol , 2.2) ;
}

float3 approximationLinearToSRGB (in float3 linearCol )
{
    return pow ( linearCol , 1 / 2.2) ;
}

float3 accurateSRGBToLinear (in float3 sRGBCol )
{
    float3 linearRGBLo = sRGBCol / 12.92;
    float3 linearRGBHi = pow (( sRGBCol + 0.055) / 1.055 , 2.4) ;
    float3 linearRGB = ( sRGBCol <= 0.04045) ? linearRGBLo : linearRGBHi ;
    return linearRGB ;
}

float3 accurateLinearToSRGB (in float3 linearCol )
{
    float3 sRGBLo = linearCol * 12.92;
    float3 sRGBHi = ( pow( abs ( linearCol ), 1.0/2.4) * 1.055) - 0.055;
    float3 sRGB = ( linearCol <= 0.0031308) ? sRGBLo : sRGBHi ;
    return sRGB ;
}
```

对比如下

![1561212121316](assets/1561212121316.jpg)

## 5.2 Manipulation of high values

HDR 存储常用的格式是 `Float32`，`Float16`，`R11F_G11F_B10F` 和 `RGB9_E5`。后两种格式无符号，`RGB9_E5` 对与 RGB 有单独的尾数位，但共享相同的指数位。

各种位数的 float 对应的精度和限制为

![1561221278949](assets/1561221278949.jpg)

> Decimal digits of precision 意义不明 >_<

Float formats 适合存储光照信息，因为他们是非线性的。Integer formats 也有。

在 Frostbite 中

- lightmap `RGB9_E5` 
- HDRI `Float16` 
- llight buffer `Float16`. Exposure is pre-applied. Shader 里精度是 Float32，存储时进行 exposure。



## 5.3 Antialiasing

PBR 增加了 aliasing，因为 NDF，强光，反射。主要原因是估计下式时 pixel 的样本缺少
$$
I(\mathbf{v})=\int_{\text { pixel }} L(\mathbf{v}) \mathrm{d} A
$$
一般情况每个像素只有一个样本。

有两种主要解决技术

- Supersampling
  - MSAA multisample anti-aliasing
  - SSAA supersample anti-aliasing
  - TAA temporal anti-aliasing
- Pre-Filtering

# 6. 转移到 PBR Transition to PBR

需要同时考虑 technical 和 artistic。

第一步是训练 TA。

第二步是让引擎同时维持 PBR 和 non-PBR。

将已存在的资源进行自动转化

- 材质
- 灯光：使用基于物理的单位很难

第三步是给游戏团队安利 PBR。

# 附录 Appendix

## A. Listing for reference mode 

## B. Oren-Nayar and GGX’s diffuse term derivation 

## C. Energy conservation

## D. Optimization algorithm for converting to Disney’s parametrization

## E. Rectangular area lighting 

## F. Local light probe evaluation

### Sphere

```c++
float3 dominantR = getSpecularDominantDir (N, R, NdotV , roughness );
float2 intersections;

if ( sphereRayIntersect ( intersections , worldPos - spherePos , dominantR , sphereRadius ))
{
    // Compute the actual direction to sample , only consider far intersection
    // No need to normalize for fetching cubemap
    float3 localR = ( worldPos + intersections .y * dominantR ) - spherePos ;
    
    // We use normalized R to calc the intersection , thus intersections .y is
    // the distance between the intersection and the receiving pixel
    float distanceReceiverIntersection = intersections .y;
    float distanceSphereCenterIntersection = length ( localR );
    
    // Compute the modified roughness based on the travelled distance
    float localRoughness = evaluateDistanceBasedRoughness ( roughness ,
    distanceReceiverIntersection , distanceSphereCenterIntersection );
    
    // Specular sampling
    // Limit artifacts introduce with high roughness
    localR = lerp ( localR , MainR , linearRoughness );
    float4 result = evaluateIBLSpecular (NdotV , localR , localRoughness , f_0 , f_90 );
    specularResult = result . rgb ;
    specularWeight = result .a;
    
    // Reflection .a contains fading information for reflection data not
    // available or barely accurate . Here we want to manage a soft
    // transition at boundary of the sphere shape to avoid hard cutoff .
    // Decrease the sphere radius with the influence distance for the test
    float localDistance = length ( worldPos - spherePos );
    float alpha = saturate (( sphereRadius - localDistance ) /
    max ( fadeDistance , 0.0001) );

    // Get local weight taking into account IBL alpha and receiver alpha
    // Smoothstep provide a nicer transition
    float alphaAttenuation = smoothstep ( alpha );
    specularWeight *= alphaAttenuation ;
}
```

### Box

```c++
float3 dominantR = getSpecularDominantDir (N, R, NdotV , roughness );

// Perform Box collision to parallax correct the cubemap
// invTransform go from worldspace to local box space without scaling
float3 localPos = mul( float4 ( worldPos , 1) , lightInvTransform ). xyz ;
float3 localDir = mul( dominantR , ( float3x3 ) lightInvTransform );

float2 intersections = boxRayIntersect ( localPos , localDir , -lightExtend , lightExtend );

// Specular contribution
specularResult = float3 (0, 0, 0);
specularWeight = 0;

if ( intersections .y > intersections .x)
{
    // retrieve local intersection position ( Localized cubemap are generated in local space not world space )
    float3 localR = localPos + intersections .y * localDir ;
    // take into account offset (in local space ) to retrieve the correct reflection vector
    localR = localR - light . localOffset ;
    
    // We use normalized R to calc the intersection , thus " intersections .y" is the distance
    between the intersection and the receiving pixel
    float distanceReceiverIntersection = intersections .y;
    float distanceBoxCenterIntersection = length ( localR );
    
    // Compute the modified roughness based on the traveled distance
    float localRoughness = evaluateDistanceBasedRoughness ( data . roughness , distanceReceiverIntersection , distanceBoxCenterIntersection );
    
    // Specular sampling
    // Limit artifacts introduce with high roughness
    localR = lerp ( localR , MainR , linearRoughness );
    float4 result = evaluateIBLSpecular (NdotV , localR , localRoughness , f_0 , f_90 );
    specularResult = result . rgb ;
    specularWeight = result .a;
    
    // Reflection .a contain fading information for reflection data not available or barely accurate
    // Here we want to manage a soft transition at boundary of the box shape to avoid hard cutoff . Do it from the boundary of the box .
    float boxPointDistance = distanceBoxPoint ( light . influenceFadeDistance . xxx - light . extend , light . extend - light . influenceFadeDistance .xxx , localPos );
    float alpha = 1.0 f - saturate ( boxPointDistance / max ( light . influenceFadeDistance , 0.0001) );
    
    // Get local weight taking into account IBL alpha and receiver alpha
    // Smoothstep provide a nicer transition
    float alphaAttenuation = smoothstep_ ( alpha );
    specularWeight *= alphaAttenuation ;
}
```

# 参考文献

[^Bur12]: B. Burley. "[**Physically Based Shading at Disney**](http://selfshadow.com/publications/s2012-shading-course/)". In: Physically Based Shading in Film and Game Production, ACM SIGGRAPH 2012 Courses. SIGGRAPH ’12. Los Angeles, California: ACM, 2012, 10:1{7. isbn: 978-1-4503-1678-1. doi: 10.1145/2343483.2343493.

[^CH05]: G. Coombe and M. Harris. "**Global Illumination Using Progressive Refinement Radiosity**". In: GPU Gems 2. Ed. by M. Pharr. Addison-Wesley, 2005, pp. 635-647.

[^Dro13]: M. Drobot. "[**Lighting of Killzone: Shadow Fall**](http://www.guerrilla-games.com/publications/)". In: Digital Dragons. 2013.

[^Dro14b]: M. Drobot. "**Physically Based Area Lights**". In: GPU Pro 5. Ed. by W. Engel. CRC Press, 2014, pp. 67-100.
[^Got13]: Y. Gotanda. "[**Real-time Physically Based Rendering**](http://research.tri-ace.com)". In: CEDEC 2013. 2013.

[^Hei14]: E. Heitz. "[**Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs**](http://jcgt.org/published/0003/02/03/)". In: Journal of Computer Graphics Techniques (JCGT) 3.2 (June 2014), pp. 32-91. issn: 2331-7418.

[^HSM10b]: J. R. Howell, R. Siegel, and M. P. Meng¨u¸c. 2010. http://www.thermalradiation.net/sectionb/B-13.html

[^Kar13]: B. Karis. "[**Real Shading in Unreal Engine 4**](http://selfshadow.com/publications/s2013-shading-course/)". In: Physically Based Shading in Theory and Practice, ACM SIGGRAPH 2013 Courses. SIGGRAPH ’13. Anaheim, California: ACM, 2013, 22:1-22:8. isbn: 978-1-4503-2339-0. doi: 10.1145/2504435.2504457.

[^KC08]: J. Kˇriv´anek and M. Colbert. "[**Real-time Shading with Filtered Importance Sampling**](http://dcgi.felk.cvut.cz/publications/2008/krivanek-cgf-rts)". In: Computer Graphics Forum 27.4 (2008). Eurographics Symposium on Rendering, EGSR ’08, pp. 1147-1154. issn: 1467-8659. doi: 10.1111/j.1467-8659.2008.01252.x.

[^KK07]: O. Kozlowski and J. Kautz. "[**Is Accurate Occlusion of Glossy Reflections Necessary ?**](http://web4.cs.ucl.ac.uk/staff/j.kautz/publications/glossyAPGV07.pdf)" In: Proceedings of Symposium on Applied Perception in Graphics and Visualization 2007 (July 2007), pp. 91-98.

[^Koj+13]: H. Kojima, H. Sasaki, M. Suzuki, and J. Tago. "[**Photorealism Through the Eyes of a FOX: The Core of Metal Gear Solid Ground Zeroes**](http://www.gdcvault.com/play/1018086/Photorealism-Through-the-Eyes-of)". In: Game Developers Conference. 2013.

[^LH13]: S. Lagarde and L. Harduin. "[**The Art and Rendering of Remember Me**](http://seblagarde.wordpress.com/2013/08/22/gdceurope-2013-talk-the-art-and-rendering-of-remember-me/)". In: Game Developers Conference Europe. 2013.

[^LZ12]: S. Lagarde and A. Zanuttini. "[**Local Image-based Lighting with Parallax-corrected Cubemaps**](http://seblagarde.wordpress.com/2012/11/28/siggraph-2012-talk/)". In: ACM SIGGRAPH 2012 Talks. SIGGRAPH ’12. Los Angeles, California: ACM, 2012, 36:1-36:1. isbn: 978-1-4503-1683-5. doi: 10.1145/2343045.2343094.

[^Mar14]: I. Mart´ınez. [**Radiative view factors**](http://webserver.dmt.upm.es/~isidoro/tc3/Radiation%5C%20View%5C%20factors.pdf). 1995-2014.

[^Pla]: PlanetMath. [**Solid angle of rectangular pyramid**](http://planetmath.org/solidangleofrectangularpyramid).

[^Qui06]: I. Qu´ılez. [**Sphere ambient occlusion**](http://www.iquilezles.org/www/artiles/sphereao/sphereao.htm). 2006.

[^Rye]: A. Ryer. [**Light Measurement Handbook**](http://www.intl-lighttech.com/services/ilt-light-measurement-handbook). International Light Technologies Inc.

[^Sch09]: C. Sch¨uler. "**An efficient and Physically Plausible Real-Time Shading Model**". In: ShaderX7: Advanced Rendering Techniques. Ed. by W. Engel. Charles River Media, 2009. Chap. 2.5.

[^Ulu14]: Y. Uludag. "**Hi-Z Screen-Space Cone-Traced Reflections**". In: GPU Pro 5. Ed. by W. Engel. CRC Press, 2014, pp. 149-192.

[^UFK13]: C. Ure~na, M. Fajardo, and A. King. “[**An Area-Preserving Parametrization for Spherical Rectangles**](https://www.solidangle.com/arnold/research/ )". In: Computer Graphics Forum 32.4 (2013), pp. 59-66. doi: 10.1111/cgf. 12151.

