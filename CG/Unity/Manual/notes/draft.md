[TOC]

# Shaders: ShaderLab and fixed function shaders

## Getting started

Unity 的着色器语言是 ShaderLab（类似 CgFX 和 .FX）。着色器的属性暴露在 Unity 的 Material inspector 上，含有多个着色器实现（SubShaders），描述渲染状态和 vertex/fragment 程序（Cg/HLSL）。

**Assets > Create > Shader > Unlit Shader**，双击 Shader 图标即可编辑

fixed-function shader 非常简单，载入时会被转变成 vertex 和 fragment 程序

> fixed-function shader 就相当于固定管线

一个简单着色器如下

```c++
Shader "Tutorial/Basic" { // 着色器名字
    Properties { // 属性
        _Color ("Main Color", Color) = (1,0.5,0.5,1)
    }
    SubShader {
        Pass { // 用一个 pass 来渲染物体
            Material {
                Diffuse [_Color]
            }
            Lighting On // 逐定点着色
        }
    }
}
```

创建一个材质，选择着色器为 `Tutorial/Basic`。

## Basic vertex lighting

仔细研究内置的 VertexLit

```c++
Shader "VertexLit" { // Shader 是关键字，"VertexLit" 是名字
    Properties {
        // internal name("inspector title", property type) = default value
        _Color ("Main Color", Color) = (1,1,1,0.5)
        _SpecColor ("Spec Color", Color) = (1,1,1,1)
        _Emission ("Emmisive Color", Color) = (0,0,0,0)
        _Shininess ("Shininess", Range (0.01, 1)) = 0.7
        _MainTex ("Base (RGB)", 2D) = "white" { }
    }

    SubShader {
        Pass {
            Material {
                Diffuse [_Color]
                Ambient [_Color]
                Shininess [_Shininess]
                Specular [_SpecColor]
                Emission [_Emission]
            }
            Lighting On // 开启 standard vertex lighting
            SeparateSpecular On // 使用分离的颜色来定义高光
            SetTexture [_MainTex] {
                constantColor [_Color]
                // Combine ColorPart, AlphaPart
                // primary 是顶点色
                // constant 就是上边的 constantColor
                // DOUBLE 是双倍
                Combine texture * primary DOUBLE, texture * constant
            }
        }
    }
}
```

![img](assets/ShaderTutProperties.png)

可选的属性类型可参考 https://docs.unity3d.com/Manual/SL-Properties.html

## The shader body

图形硬件有多种，支持能力不同。因此一个 shader 里边有多个 SubShader，Unity 会使用硬件支持的最前边的 subshader。

```c++
Shader "Structure Example" {
    Properties { /* ...shader properties... */ }
    SubShader {
        // ...subshader that requires DX11 / GLES3.1 hardware...
    }
    SubShader {
        // ...subshader that might look worse but runs on anything :)
    }
}
```

在 subshader 中设置所有 pass 共享的渲染状态，并且定义 pass，支持的命令参考 https://docs.unity3d.com/Manual/SL-SubShader.html

## Passes

每个 subshader 有一个 pass 集合，每个 pass 里物体几何被渲染，至少要有 1 个 pass。

[VertexLit](#Basic vertex lighting) 只有一个 pass，相关的内容写在了注释中。

# Shaders: vertex and fragment programs

着色器一般结构

```c++
Shader "MyShaderName"
{
    Properties
    {
        // material properties here
    }
    SubShader // subshader for graphics hardware A
    {
        Pass
        {
            // pass commands ...
        }
        // more passes if needed
    }
    // more subshaders if needed
    FallBack "VertexLit" // optional fallback
}
```

最后使用了 [Fallback](https://docs.unity3d.com/Manual/SL-Fallback.html) 命令。当所有 SubShader 都不支持时，就使用该命令后边的着色器。相当于 include 了其 SubShader。[Properties](https://docs.unity3d.com/Manual/SL-Properties.html)，[SubShaders](https://docs.unity3d.com/Manual/SL-SubShader.html) 和 [Passes](https://docs.unity3d.com/Manual/SL-Pass.html) 

可以使用 `UsePass "ShaderName/PassName"` 来使用其他 shader 的 pass，因此需要给 pass 命名 `Name "PassName"`。

#### Vertex 和 fragment programs

当使用 vertex 和 fragment 程序（也叫可编程管线 programmable pipeline）。

#### Using Cg/HLSL in ShaderLab

ShaderLab 使用 [Cg](http://developer.nvidia.com/page/cg_main.html)/[HLSL](http://msdn.microsoft.com/en-us/library/bb509561(VS.85).aspx)。他们会被编译成 low-level 着色器，游戏中只包含 low-level 汇编 assembly 或字节码 bytecode。

格式

```c++
Pass {
    // ... the usual pass state setup ...

    CGPROGRAM
    // compilation directives for this snippet, e.g.:
    #pragma vertex vert
    #pragma fragment frag

    // the Cg/HLSL code itself

    ENDCG
    // ... the rest of pass setup ...
}
```

示例如下，将法向作为颜色

```c++
Shader "Tutorial/Display Normals" {
    SubShader {
        Pass {

            CGPROGRAM

            #pragma vertex vert // 包含 vertex 程序
            #pragma fragment frag // 包含 fragment 程序
            #include "UnityCG.cginc"

            struct v2f { // vertex to fragment
                float4 pos : SV_POSITION;
                fixed3 color : COLOR0;
            };

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.color = v.normal * 0.5 + 0.5;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4 (i.color, 1);
            }
            ENDCG

        }
    }
}
```

#### Using shader properties in Cg/HLSL code

使用属性时，在 Cg/HLSL 内需要定义相同类型和名字的变量，参考 [properties in shader programs](https://docs.unity3d.com/Manual/SL-PropertiesInPrograms.html)。

示例

```c++
Shader "Tutorial/Textured Colored" {
    Properties {
        _Color ("Main Color", Color) = (1,1,1,0.5)
        _MainTex ("Texture", 2D) = "white" { }
    }
    SubShader {
        Pass {

        CGPROGRAM
        #pragma vertex vert
        #pragma fragment frag

        #include "UnityCG.cginc"

        fixed4 _Color;
        sampler2D _MainTex;

        struct v2f {
            float4 pos : SV_POSITION;
            float2 uv : TEXCOORD0;
        };

        float4 _MainTex_ST;

        v2f vert (appdata_base v)
        {
            v2f o;
            o.pos = UnityObjectToClipPos(v.vertex);
            o.uv = TRANSFORM_TEX (v.texcoord, _MainTex);
            return o;
        }

        fixed4 frag (v2f i) : SV_Target
        {
            fixed4 texcol = tex2D (_MainTex, i.uv);
            return texcol * _Color;
        }
        ENDCG

        }
    }
}
```

## Writing Surface Shaders

与光照交互的 shader 很复杂，包含多种光源，多个阴影选项，不同渲染路径（forward 和 deferred），而 shader 需要处理所有这些。

Surface Shaders 是一个 code generation 方法，以简化 vertex/pixel shader 的编写。

简单的示例可查看 [Surface Shader Examples](https://docs.unity3d.com/Manual/SL-SurfaceShaderExamples.html)。这里贴一下简单的 `Diffuse Simple` 和 `Diffuse Texture` 

```c++
  Shader "Example/Diffuse Simple" {
    SubShader {
      Tags { "RenderType" = "Opaque" }
      CGPROGRAM
      #pragma surface surf Lambert // built-in Lambert (diffuse) lighting model
      struct Input {
          float4 color : COLOR;
      };
      void surf (Input IN, inout SurfaceOutput o) {
          o.Albedo = 1;
      }
      ENDCG
    }
    Fallback "Diffuse"
  }
```

```c++
  Shader "Example/Diffuse Texture" {
    Properties {
      _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader {
      Tags { "RenderType" = "Opaque" }
      CGPROGRAM
      #pragma surface surf Lambert
      struct Input {
          float2 uv_MainTex; // 纹理坐标
      };
      sampler2D _MainTex; // 类型和名字同于 properties 中的 _MainTex
      void surf (Input IN, inout SurfaceOutput o) {
          o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb;
      }
      ENDCG
    } 
    Fallback "Diffuse"
  }
```

### How it works

用 surf 函数输入各种各样的参数，然后输出 `SurfaceOutput`，描述表面的性质（albedo，normal，emission，specularity 等）。

标准的 `SurfaceOutput` 结构如下

```c++
struct SurfaceOutput
{
    fixed3 Albedo;  // diffuse color
    fixed3 Normal;  // tangent space normal, if written
    fixed3 Emission;
    half Specular;  // specular power in 0..1 range
    fixed Gloss;    // specular intensity
    fixed Alpha;    // alpha for transparencies
};
```

Unity 5 加入了 PBR，相应的结构为

```c++
struct SurfaceOutputStandard
{
    fixed3 Albedo;      // base (diffuse or specular) color
    fixed3 Normal;      // tangent space normal, if written
    half3 Emission;
    half Metallic;      // 0=non-metal, 1=metal
    half Smoothness;    // 0=rough, 1=smooth
    half Occlusion;     // occlusion (default 1)
    fixed Alpha;        // alpha for transparencies
};

struct SurfaceOutputStandardSpecular
{
    fixed3 Albedo;      // diffuse color
    fixed3 Specular;    // specular color
    fixed3 Normal;      // tangent space normal, if written
    half3 Emission;
    half Smoothness;    // 0=rough, 1=smooth
    half Occlusion;     // occlusion (default 1)
    fixed Alpha;        // alpha for transparencies
};
```

### Surface Shader compile directives

surface shader 放在 `CGPROGRAM..ENDCG` 内，与一般的 shader 不同之处有

- 放在 SubShader 内，不是 pass 内。其会被编译成多个 pass

- 使用 `#pragma surface ...` 指令来指示其是一个 surface shader

  格式为

  ```c++
  #pragma surface <surfaceFunction> <lightModel> [optional params]
  ```

  其中

  - `surfaceFunction` 格式为 `void surf (Input IN, inout SurfaceOutput o)`，`Input` 可自己定义
  - `lightModel` 内置的有 `Standard`、`StandardSpecular`、`Lambert`（diffuse） 和 `BlinnPhong`（specular），自定义参考 [Custom Lighting Models](https://docs.unity3d.com/Manual/SL-SurfaceShaderLighting.html)。

