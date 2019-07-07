# 第 6 章

## 6.1  我们是如何看到这个世界的

- 光线从光源中被发射出来
- 光线与场景物体相交：一部分被吸收，一部分被散热到其他方向
- 摄像机吸收一些光，产生一张图像

### 6.1.1  光源

用辐照度 irradiance 来量化光

到达表面的辐照度与 $\cos\theta$ 成正比

![irradiance.jpg-60.3kB](assets/irradiance.jpg)

### 6.1.2  吸收和散射

光线与物体相交的结果：散射 scattering 和吸收 absorption

散射只改变光线的方向，不改变光线的密度和颜色。吸收只改变光线的密度和颜色，不改变光线方向。

散射后有两种方向：一种将会散射到物体内部，称为折射 refraction 或透射 transmission，另一种散射到外部，称为反射 reflection。对于不透明物体，折射进入物体内部的光线还会继续与内部的颗粒进行相交，其中一些光线最后会重新发射出物体表面，而另一些被物体吸收。那些从物体表面重新发射出的光线将具有和入射光线不同的方向分布和颜色。

![scattering.jpg-37.1kB](assets/scattering.jpg)

为了区分这两种不同的散射方向，我们在光照模型中使用了不同的部分来计算它们：高光反射 specular 部分表示物体表面是如何反射光线的，而漫反射 diffuse 部分则表示由多少光线会被折射、吸收和散射出表面。

出射度 exitance 描述出射光的数量和方向，辐照度与出射度满足线性关系，比值就是材质的漫反射和高光反射属性。

### 6.1.3  着色

着色 shading 指的是，根据材质属性、光源信息，使用一个等式去计算沿某个观察方向的出射度的过程，这个等式称为光照模型 lighting model。

### 6.1.4  BRDF 光照模型

Bidirectional Reflectance Distribution BRDF 描述了入射和出射的规律。

本章的光照模型是经验模型，更真实的就是基于物理的 BRDF 模型。

计算机图形学的第一定律：如果它看起来是对的，那么它就是对的

## 6.2  标准光照模型

标准光照模型只关心直接光照 direct ligh

分成四部分

- 自发光 emissive，自发光不照亮周围物体
- 高光反射 specular
- 漫反射 diffuse
- 环境光 ambient

### 6.2.1  环境光

标准光照模型忽略了间接光照 indirect light。
$$
c_\text{ambient}=g_\text{ambient}
$$

### 6.2.2  自发光

$$
\boldsymbol{c}_{\text {emissive}}=\boldsymbol{m}_{\text {emissive}}
$$

### 6.2.3  漫反射

Lambert law 兰伯特定律
$$
\boldsymbol{c}_{\text {diffuse}}=\left(\boldsymbol{c}_{\text {light}} \cdot \boldsymbol{m}_{\text {diffuse}}\right) \max (0, \boldsymbol{n} \cdot \boldsymbol{I})
$$

### 6.2.4  高光反射

#### Phong 模型

![specular.jpg-31.2kB](assets/specular.jpg)

反射方向
$$
\mathbf{r}=2(\hat{\mathbf{n}} \cdot \mathbf{I}) \hat{\mathbf{n}}-\mathbf{I}
$$
specular
$$
\mathbf{c}_{\text {spscular}}=\left(\boldsymbol{c}_{\text {light}} \cdot \boldsymbol{m}_{\text {specular}}\right) \max (0, \hat{\mathbf{v}} \cdot \mathbf{r})^{m_\text{gloss}}
$$
其中 $m_\text{gloss}$ 是光泽度 gloss，也称为反光度 shininess，用于控制高光域大小，$m_\text{gloss}$ 高光域越小。$\boldsymbol{m}_\text{specular}$ 是高光反射颜色。

#### Blinn 模型

![Blinn.jpg-32.1kB](assets/Blinn.jpg)
$$
\hat{\mathbf{h}}=\frac{\hat{\mathbf{v}}+\mathbf{I}}{|\hat{\mathbf{v}}+\mathbf{I}|}
$$
specular
$$
\mathbf{c}_{\text {spscular}}=\left(\boldsymbol{c}_{\text {light}} \cdot \boldsymbol{m}_{\text {specular}}\right) \max (0, \hat{\mathbf{n}} \cdot \mathbf{h})^{m_\text{gloss}}
$$

### 6.2.5  逐像素还是逐顶点

计算光照模型位置

- 片元着色器：逐像素光照 per-pixel lighting，Phong 着色，法线插值着色技术
- 顶点着色器：逐顶点光照 per-vertex lighting，Gouraud 着色

### 6.2.6  总结

Blinn-Phong 光照模型

无法表达

- 菲涅尔反射
- 各向异性

## 6.3  Unity 中的环境光和自发光

Unity 中 Window -> Lighting -> Ambient Soruce/Ambient Color/Ambient Intensity 控制环境光

![ambient.jpg-35.3kB](assets/ambient.jpg)

Shader 中使用 `UNITY_LIGHTMODEL_AMBIENT` 来得到环境光的颜色和强度

## 6.4  在 Unity Shader 中实现漫反射光照模型

### 6.4.1  实践：逐顶点光照

设置光照模式

```c++
Tags { "LightMode"="ForwardBase" }
```

只有正确设置了模型，才能得到一些内置变量

为了使用内置变量，需要包含内置文件

```c++
#include "Lighting.cginc"
```

光源方向为

```c++
fixed3 worldLight = normalize(_WorldSpaceLightPos0.xyz);
```

上述就算不具有通用性，假设只有一个光源，且为平行光

效果如下

![diffuse_vertex_level.jpg-40.4kB](assets/diffuse_vertex_level.jpg)

### 6.4.2  实践：逐像素光照

顶点着色器输出世界方向，片元着色器计算光照

![diffuse_pixel_level.jpg-40.1kB](assets/diffuse_pixel_level.jpg)

### 6.4.3  半兰伯特模型

$$
\mathbf{c}_{\text {dititise}}=\left(\mathbf{c}_{\text {light}} \cdot \mathbf{m}_{\text {ditfise}}\right)(\alpha(\hat{\mathbf{n}} \cdot \mathbf{I})+\beta)
$$

一般 $\alpha$ 和 $\beta$ 取 0.5，有
$$
\mathbf{c}_{\text {diffuse}}=\left(\mathbf{c}_{\text {light}} \cdot \mathbf{m}_{\text {diffuse}}\right)(0.5(\hat{\mathbf{n}} \cdot \mathbf{I})+0.5)
$$
效果对比如下

![diffuse_compare_all.jpg-86.9kB](assets/diffuse_compare_all.jpg)

## 6.5  在 Unity Shader 中实现高光反射光照模型

### 6.5.1  实践：逐顶点光照

![specular_vertex_level.jpg-41.5kB](assets/specular_vertex_level.jpg)

### 6.5.2  实践：逐像素光照

![specular_pixel_level.jpg-40.8kB](assets/specular_pixel_level.jpg)

### 6.5.3  Blinn-Phong 光照模型

![specular_compare_all.jpg-82.5kB](assets/specular_compare_all.jpg)

## 6.6  召唤神龙：使用 Unity 内置的函数

- `UnityObjectToWorldNormal`，无需 `normalize` 
- `UnityWorldSpaceLightDir`，需 `normalize` 
- `UnityWorldSpaceViewDir`，需 `normalize` 

