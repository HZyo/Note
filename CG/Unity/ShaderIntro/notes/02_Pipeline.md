# 第 2 章  渲染流水线

[TOC]

## 2.1  综述

### 2.1.1  什么是流水线

![流水线](assets/流水线.jpg)

### 2.1.2  什么是渲染流水线

![概念流水线](assets/概念流水线.jpg)

## 2.2  CPU 和 GPU 之间的通信

应用阶段

1. 把数据加载到显存中
2. 设置渲染状态
3. 调用 Draw Call

### 2.2.1  把数据加载到显存中

![CopyDataToGPU.jpg-86.5kB](assets/CopyDataToGPU.jpg)

### 2.2.2  设置渲染状态

渲染状态定义了网格的渲染方式。如顶点着色器、片源着色器、光源属性、材质等。如果不更改，则会使用同一种状态

![SetRenderState.jpg-157.1kB](assets/SetRenderState.jpg)

### 2.2.3  调用 Draw Call

Draw Call 仅仅会指向一个需要被渲染的图元（primitive）列表，不包含任何材质信息。

![DrawCall.jpg-59.1kB](assets/DrawCall.jpg)

## 2.3  GPU 流水线

### 2.3.1  概述

![GPU流水线.jpg-82.2kB](assets/GPU流水线.jpg)

绿色可编程，黄色可配置，蓝色固定，虚线可选

### 2.3.2  顶点着色器

![VertexShaderProcess.jpg-43kB](assets/VertexShaderProcess.jpg)

![Vertex Shader.jpg-34.9kB](assets/Vertex Shader.jpg)

### 2.3.3  裁剪

![Clipping.jpg-25.5kB](assets/Clipping.jpg)

### 2.3.4  屏幕映射

![ScreenMapping.jpg-22.6kB](assets/ScreenMapping.jpg)

### 2.3.5  三角性设置

计算光栅化网格所需的信息，具体就是计算边的方程等。

### 2.3.6  三角形遍历

![TriangleSetupAndTraversal.jpg-80kB](assets/TriangleSetupAndTraversal.jpg)

### 2.3.7  片元着色器

![FragmentShader.jpg-42.4kB](assets/FragmentShader.jpg)

### 2.3.8  逐片元操作

任务

- 可见性（深度测试、模板测试）
- 片元颜色值和颜色缓冲区的颜色合并（高度可配置）

![Per-fragment Operations.jpg-23.1kB](assets/Per-fragment Operations.jpg)

深度测试和模板测试如下

![Stencil Test_Depth Test.jpg-93.5kB](assets/Stencil Test_Depth Test.jpg)

混合操作如下

![Blending.jpg-67.6kB](assets/Blending.jpg)

### 2.3.9  总结

...

## 2.4  一些容易困惑的地方

### 2.4.1  OpenGL/DirectX

图形接口、驱动与 GPU 的关系

![OpenGLåDirectX.jpg-56.1kB](assets/OpenGL和DirectX.jpg)

### 2.4.2  HLSL、GLSL、CG

GLSL 跨平台，因为其将编译任务交给可显卡驱动。HLSL 是微软控制着色器编译。CG 完全跨平台，其跨平台性主要取决于与微软合作，因此像 HLSL。

Unity Shader 可以使用 CG/HLSL 或 GLSL。

### 2.4.3  Draw Call

Draw Call 是 CPU 调用图像编程接口（如 OpenGL 的 `glDrawElements` 或 DirectX 的 `DrawIndexedPrimitive`），以命令 GPU 进行渲染的操作。

#### 问题一：CPU 和 GPU 是如何实现并行工作的？

CPU 和 GPU 并行工作靠的是命令缓冲区（Command Buffer）。命令缓冲区包含一个命令队列，由 CPU 向其中添加命令，而由 GPU 从中读取命令，添加和读取的过程是相互独立的。命令缓冲区是的 CPU 和 GPU 可以相互独立工作。当 CPU 需要渲染一些对象时，它可以向命令缓冲区中添加命令，而当 GPU 完成了上一次的渲染任务后， 它就可以从命令队列中再取出一个命令并执行它。

其中的命令有多个类型，如 Draw Call，改变渲染状态

![CommandBuffer.jpg-49.9kB](assets/CommandBuffer.jpg)

改变渲染状态更加耗时，因此用红色标记

#### 问题二：为什么 Draw Call 多了会影响帧率？

渲染速度往往快于 CPU 提交命令的速度。如果 Draw Call 太多，CPU 会把大量时间花费在提交 Draw Call 上，造成 CPU 过载

![SmallCommand.jpg-107.7kB](assets/SmallCommand.jpg)

#### 问题三：如何减少 Draw Call？

方法很多，这里讨论批处理（Batching）。把很多小的 Draw Call 合并成一个大的 Draw Call。

![Batching.jpg-70.3kB](assets/Batching.jpg)

我们需要在 CPU 内存中合并网格，合并需要消耗时间，因此适合静态物体。

### 2.4.4  固定管线渲染

固定函数的流水线（Fixed-Function Pipeline），淘汰了

## 2.5  那么，你明白什么是 Shader 了吗？

## 2.6 扩展阅读

RTR4[^Akenine]、Batch[^Wloka]、OpenGL Rendering Pipeline[^OGL]、DierctX Rendering Pipeline[^DX]。

## 参考

[^Akenine]: Akenine-Moller T, Haines E, Hoffman N. [**Real-time rendering**](http://www.realtimerendering.com/)[M]. AK Peters/CRC Press, 2019.

[^Wloka]: Wloka M. Batch, batch, batch: [**What does it really mean**](http://www.nvidia.com/docs/io/8230/batchbatchbatch.ppt)[C]//Presentation at game developers conference. 2003.

[^OGL]: Khronos. [**Rendering Pipeline Overview**](https://www.khronos.org/opengl/wiki/Rendering_Pipeline_Overview).

[^DX]:Microsoft. [**Graphics Pipeline**](https://docs.microsoft.com/zh-cn/windows/win32/direct3d11/overviews-direct3d-11-graphics-pipeline).


