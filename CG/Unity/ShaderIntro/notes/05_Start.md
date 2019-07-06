# 第 5 章  开始 Unity Shader 学习之旅

[TOC]

## 5.1  本书使用的软件和环境

5.2.1，更高版本通常不会有什么影响

## 5.2 一个最简单的顶点 / 片元着色器

顶点 / 片元着色器的结构

```c++
Shader "MyShaderName" {
    Properties {
        // 属性
    }
    SubShader {
        // 针对显卡 A 的 SubShader
        Pass {
            // 设置渲染状态和标签
            
            // 开始 CG 代码片段
            CGPROGRAM
            // 该代码片段的编译指令，例如
            #pragma vertex vert // vert 函数包含顶点着色器代码
            #pragma fragment frag // frag 函数包含片元着色器代码
            
            /* CG 代码 */
            
            ENDCG
            
            // 其他设置
        }
        // 其他需要的 Pass
    }
    SubShader {
        // 针对显卡 B 的 SubShader
    }
    
    // 上述 SubShader 都失败后用于回调的 Unity Shader
    Fallback "VertexLit"
}
```

简化版结构

```c++
Shader "MyShaderName" {
    Properties {
        // 属性
    }
    SubShader {
        Pass {
            CGPROGRAM
            
            #pragma vertex vert
            #pragma fragment frag
            
            /* CG 代码 */
            
            ENDCG
        }
    }
    Fallback "VertexLit"
}
```

一个简单的 Unity Shader

```c++
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Unity Shaders Book/Chapter 5/Simple Shader" {
    Properties {
        _Color ("Color Tint", Color) = (1, 1, 1, 1)
    }
    SubShader {
        Pass {
            CGPROGRAM

            #pragma vertex vert
            #pragma fragment frag
            
            uniform fixed4 _Color;

            struct a2v {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 texcoord : TEXCOORD0;
            };
            
            struct v2f {
                float4 pos : SV_POSITION;
                fixed3 color : COLOR0;
            };
            
            v2f vert(a2v v) {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.color = v.normal * 0.5 + fixed3(0.5, 0.5, 0.5);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target {
                fixed3 c = i.color;
                c *= _Color.rgb;
                return fixed4(c, 1.0);
            }

            ENDCG
        }
    }
}
```

## 5.3  强大的援手：Unity 提供的内置文件和变量

### 5.3.1  内置的包含文件

类似 C++ 的 include，文件后缀 `.cginc`。

示例

```c++
CGPROGRAM
// ...
#include "UnityCG.cginc"
// ...
ENDCG
```

https://unity3d.com/cn/get-unity/download/archive 选择下载->内置着色器来下载这些文件

CGIncludes 中主要文件及作用

![1562407662296](assets/1562407662296.png)

UnityCG.cginc 有预定义的结构体作为定点着色器的输入和输出

![1562407767050](assets/1562407767050.png)

还有一些常用的帮助函数

![1562407794743](assets/1562407794743.png)

### 5.3.2  内置的变量

很多内置变量位于 UnityShaderVariables.cginc 中，与光照有关的内置变量位于 Lighting.cginc、AutoLight.cginc 中。

## 5.4  Unity 提供的 CG/HLSL 语义

### 5.4.1  什么是语义

vs 和 fs 的输入输出变量后有全部大写的名称，他们是 CG/HLSL 提供的语义 semantics[^semantic]。

### 5.4.2  Unity 支持的语义

a2v 支持的常用语义

![1562408565611](assets/1562408565611.png)

TEXCOORDn 中的 n 取决于 Shader Model，如 Shader Model 3 中 n 等于 8，Shader Model 4 和 Shader Model 5 中，n 等于 16。

v2f 支持的常用语义

![1562409936209](assets/1562409936209.png)

片元着色器输出支持的常用语义

![1562409855766](assets/1562409855766.png)

## 5.5  程序员的烦恼：Debug

输出颜色，Assets/Scripts/Chapter5/ColorPicker.cs

https://docs.unity3d.com/Manual/SL-DebuggingD3D11ShadersWithVS.html

Window -> Analytics -> Frame Debugger

VS 插件、Intel GPA、RenderDoc、NVIDIA NSight、AMD GPU PerfStudio

## 5.6  小心：渲染平台的差异

### 5.6.1  渲染纹理的坐标差异

![2d_cartesian_opengl_directx.jpg-33.1kB](assets/2d_cartesian_opengl_directx(1).jpg)

### 5.6.2  Shader 的语法差异

### 5.6.3  Shader 的语义差异

SV_POSITION、SV_Target

### 5.6.4  其他平台差异

## 5.7  Shader 整洁之道

### 5.7.1  float、half 还是 fixed

![1562414921536](assets/1562414921536.png)

尽可能使用精度较低的类型，fixed 存储颜色和单位矢量，更大范围使用 half，最差情况使用 float

### 5.7.2  规范语法

使用和变量类型相匹配的参数数目来对变量进行初始化

### 5.7.3  避免不必要的计算

减少 Shader 的运算

### 5.7.4  慎用分支和循环语句

### 5.7.5  不要除以 0

## 5.8  扩展阅读

## 参考

[^semantic]: https://docs.microsoft.com/zh-cn/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics#VS 

