# Dynamic rain and its effects

[上一节](1_ObserveRainyWorld.md) 讨论了多种雨效。主要参考 ATI 的 [“Toy Shop” demo](http://www.youtube.com/watch?v=LtxvpS5AYHQ)，专注于城市环境。

## Rain Effects

### Rain splashes  / Falling drops splashes

水滴撞击表面会产生飞溅 splash。在高处聚积的水流会产生掉落。在雨滴撞击场景时生成一个水花粒子。当有很多雨滴产生水花时，难以分辨水花是由哪滴雨滴产生的。基于此事实，出于性能考虑，我们可以用两个分离的系统来分别处理雨滴和水花。

许多游戏通过发出随机射线并与场景（简化版）相交来确定水花生成位置，可只在屏幕附近产生水花。简单点可以手动设置水花产生点。我们使用了 depthmap 方法，步骤如下

- 渲染深度图
- 将深度图从 GPU 传到 CPU
- 使用深度图来生成随机位置
- 在这些位置生成水花

从上往下看的深度图

![DepthMap](assets/depthmap1.jpg)

...

### Rain / Raindrops

雨效难以观察，除非有亮光或者雨很大。

雨滴物理性质为

- 0.5 - 10 mm，小雨滴球形，大雨滴扁球形
- 雨滴大小影响速度
- ...

模拟雨滴有两种方法：粒子和大贴图

粒子系统方法可以生成真实的运动，受风影响，且能用 GPU 高效模拟。缺点是缺乏扩展性。

大贴图方法使用了贴图动画（程序性或者手写）。有扩展性，但没有深度和运动。向下看时雨滴平行于地面。

![img](assets/atisushi00.jpg)

“Flight simulator 2004” 将四张贴图动画映射到一个 double cone 上

![img](assets/rainconemesh.jpg)

越远的贴图越缩小（更多雨滴），滚动越慢，模拟出深度视差的效果（雨滴更小移动更慢）。

为了实现不同强度的雨，我们将相机前方的空间分割成 4 层。

![Layer](assets/layer.jpg)

每层使用了相同的预先运动模糊的雨滴贴图

![RainTexture](assets/raintexture.jpg)

我们平移和缩放不同层的纹理坐标

![UVPattern](assets/uvpattern.jpg)

不同层使用不同的贴图

![RainLayer](assets/rainlayer.jpg)

为了将深度和视差感融入雨效，我们使用深度缓冲来遮挡雨滴。我们使用高度图来确定雨滴的深度，可以程序化生成高度贴图。

