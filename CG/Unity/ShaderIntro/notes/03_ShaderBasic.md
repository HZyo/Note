# 第 3 章  Unity Shader 基础

[TOC]

## 3.1  Unity Shader 概述

### 3.1.1  材质和 Unity Shader

Unity 中配合使用材质（Material）和 Unity Shader 才能达到效果。

流程

1. 创建一个材质
2. 创建一个 Unity Shader，并把它赋给上一步中的材质
3. 把材质赋给要渲染的对象
4. 在材质面板中调整 Unity Shader 的属性

![material_shader.jpg-125.8kB](assets/material_shader.jpg)

Unity Shader 定义了顶点着色器、片元着色器、属性、指令等，而材质允许调节这些属性，并将其最终赋给相应的模型。

### 3.1.2  Unity 中的材质

材质需要结合 GameObject 的 Mesh 或 Particle Systems 组件来工作。

![mesh_renderer.jpg-41kB](assets/mesh_renderer.jpg)

![material_inspector.jpg-119.4kB](assets/material_inspector.jpg)

> 1 改变形状、2 改变光照

### 3.1.3  Unity 中的 Shader

Unity Shader 本质上是一个文本文件，有相应的导入设置（Import Settings）面板

![shader_import_settings.jpg-38kB](assets/shader_import_settings.jpg)

## 3.2  Unity Shader 的基础：ShaderLab

渲染很繁琐，Unity Shader 解决了这个问题，相应的语言是 ShaderLab。

Unity Shader 是 Unity 为开发者提供的高层级的渲染抽象层，让开发者更加轻松地控制渲染。

![shaderlab_abstract.jpg-63.4kB](assets/shaderlab_abstract.jpg)

说明性语言，基本结构为

```c++
Shader "ShaderName"{
    Properties {
        // 属性
    }
    SubShader {
        // 显卡 A 使用的子着色器
    }
    SubShader {
        // 显卡 B 使用的子着色器
    }
    Fallback "VertexLit"
}
```

## 3.3  Unity Shader 的结构

### 3.3.1  给我们的 Shader 起个名字

Shader 的名字会出现在下拉框，可以用斜杠（`/`）来控制层级

如 `"Custom/MyShader"`，代码为

```c++
Shader "Custom/MyShader" { /*...*/ }
```

相应的结果如下

![shader_name.jpg-55.5kB](assets/shader_name.jpg)

### 3.3.2  材质和 Unity Shader 的桥梁：Properties

```c++
Properties{
    InternalName("DisplayName", PropertyType) = DefaultValue
    // 更多属性
}
```

常见的属性类型如下

![1562397899609](assets/1562397899609.png)

`Int`、`Float` 和 `Range` 是数字类型，默认值是单独的数字，`Color` 和 `Vector` 的默认值四维向量。`2D`、`Cube` 和 `3D` 是纹理类型，默认值是字符串跟一个花括号，字符串要么空，要么是内置的纹理名称，如`"white"`、`"black"`、`"gray"` 或 `"bump"`。花括号原本用于指定一些纹理属性，5.0 后废除了。

示例

```c++
Shader "Custom/ShaderLabProperties" {
    Properties {
        // Numbers and Sliders
        _Int ("Int", Int) = 2
        _Float ("Float", Float) = 1.5
        _Range ("Range", Range(0.0, 5.0)) = 3.0
        
        // Colors and Vectors
        _Color ("Color", Color) = (1,1,1,1)
        _Vector ("Vector", Vector) = (2,3,6,1)
        
        // Textures
        _2D ("2D", 2D) = "" {}
        _Cube ("Cube", Cube) = "white" {}
        _3D ("3D", 3D) = "black" {}
    }
}
```

![shaderlab_properties.jpg-33.2kB](assets/shaderlab_properties.jpg)

可以自定义 Shader 的 GUI，例子 Assets->Material->Chapter3->RedifyMat，参考了官方手册的 [Custom Shader GUI](http://docs.unity3d.com/Manual/SL-CustomShaderGUI.html)。需要在 CG 代码中定义和这些属性类型相匹配的变量。即使不在 `Properties` 语义块中声明这些属性，也可以直接在 CG 代码片中定义变量，此时可以通过脚本向 Shader 传递这些属性。`Properties` 语句块的作用仅仅是为了让这些属性可以出现在材质面板中。

### 3.3.3  重量级成员：SubShader

每个 Unity Shader 包含一个至多个 SubShader 语义块。根据目标机器选择其中一个 SubShader，都不支持则使用 `Fallback` 指定的 Unity Shader。

SubShader 语义块中包含的定义通常如下

```C++
SubShader {
    // 标签，可选的
    [Tags]
    
    // 状态，可选的
    [RenderSetup]
    
    Pass {
        /*...*/
    }
    // Other Passes
}
```

Pass 定义了一次完整的渲染流程，多 Pass 往往造成渲染性能的下降，尽量用最小数目的 Pass。Pass 内也可以设置状态和标签，不同的是，SubShader 中的一些标签设置是特定的。状态设置的话两者语法相同，但 SubShader 设置的状态会用于所有 Pass。

状态设置很多，常见的如下

| 状态名称 | 设置指令                                                     | 解释                               |
| -------- | ------------------------------------------------------------ | ---------------------------------- |
| Cull     | Cull Back \| Front \| Off                                    | 设置剔除模式：剔除背面、正面、关闭 |
| ZTest    | ZTest Less Greater \| LEqual \| GEqual \| Equal \| NotEqual \| Always | 设置深度测试时使用的函数           |
| ZWrite   | ZWrite On \| Off                                             | 开启 / 关闭深度写入                |
| Blend    | Blend SrcFactor DstFactor                                    | 开启并设置混合模式                 |

标签是键值对，键和值都是字符串，结构如下

```c++
Tags{
    "TagName1" = "Value1"
    "TagName2" = "Value2"
}
```

支持的标签如下

![1562401025393](assets/1562401025393.png)

Pass 语义块包含的语义如下

```c++
Pass {
    // Name "MyPassName"，可选的
    [Name]
    [Tags]
    [RenderSetup]
    // Other code
}
```

通过这个名词，可以使用 `UsePass` 命令来直接使用其他 Unity Shader 中的 Pass

```c++
// Untiy 会将 Pass 的名字大写
UsePass "MyShader/MYPASSNAME"
```

Pass 中可以设置的标签如下

![1562401479163](assets/1562401479163.png)

GrabPass 可以抓取屏幕并存储在一张纹理中

### 3.3.4  留一条后路：Fallback

```c++
Fallback "name"
Fallback Off
```

### 3.3.5  其他语义

CustomEditor、Category

## 3.4  Unity Shader 的形式

着色器代码可以写在 SubShader 中（表面着色器），也可以卸载 Pass 中（顶点 / 片元着色器和固定函数着色器。不管哪种形式，真正意义上的 Shader 代码都需要包含在 SubShader 语义块中

```c++
Shader "MyShader" {
    Properties {
        // 属性
    }
    
    SubShader {
        // 真正意义的 Shader 代码会出现在这里
    }
}
```

### 3.4.1  Untiy 的宠儿：表面着色器

表面着色器是一种着色器代码类型，需要代码量很少，最后会转换成对于的顶点 / 片元着色器，Unity 为我们处理了很多光照细节。

示例

```c++
Shader "Custom/Simple Surface Shader" {
    SubShader {
        Tags { "RenderType" = "Opaque" }
        
        CGPROGRAM
        #pragma surface surf Lambert
        struct Input {
            float color : COLOR;
        }
        
        void surf(Input IN, inout SurfaceOutput o) {
            o.Albedo = 1;
        }
        ENDCG
    }
    
    Fallback "Diffuse"
}
```

### 3.4.2  最聪明的孩子：顶点 / 片元着色器

懂点 / 片元着色器复杂但灵活

示例

```c++
Shader "Custom/Simple VertexFragment Shader" {
    SubShader {
        Pass {
            CGPROGRAM
            
            #pragma vertex vert
            #pragma fragment frag
            
            float4 vert(flaot4 v : POSITION) : SV:POSITION {
                return mul(UNITY_MATERIX_MVP, v);
            }
            
            fixed4 frag() : SV_TARGET {
                return fixed4(1.0,0.0,0.0,1.0);
            }
            
            ENDCG
        }
    }
}
```

### 3.4.3  被抛弃的角落：固定函数着色器

```c++
Shader "Tutirial/Basic" {
    Properties {
        _Color ("Main Color", color) = (1,0.5,0.5,1)
    }
    SubShader {
        Pass {
            Material {
                Diffuse [_Color]
            }
            Lighting On
        }
    }
}
```

固定函数着色器会被 Unity 编译成对应的顶点 / 片元着色器

### 3.4.4  选择哪种 Unity Shader 形式

- 旧设备用固定函数着色器
- 处理各种光源则使用表面着色器，注意移动平台的性能表现
- 光照数目少则使用顶点 / 片元着色器
- 自定义渲染效果使用顶点 / 片元着色器

## 3.5  本书使用的 Unity Shader 形式

顶点 / 片元着色器

## 3.6  答疑解惑

...

## 3.7  扩展阅读

 https://docs.unity3d.com/Manual/SL-Reference.html