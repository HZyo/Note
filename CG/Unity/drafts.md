# Drafts

[TOC]

## 1. 生命周期

![img](assets/052339397497301.jpg)

### 1. 静态构造函数

程序被加载后就会执行，只会执行一次，不可主动调用

```csharp
class A{
    public static int num;
    static A(){// 不可有参数
        num = 1;// 初始化静态成员
    }
}
```

### 2. （非静态）构造函数

Component 会在 Unity 的编辑器里使用，构造函数会用于初始化

因此开发者不应该去使用这个构造函数

可以在 awake 里完成自己的功能

### 3. Awake

>Awake is called when the script instance is being loaded.Awake is used to initialize any variables or game state before the game starts. Awake is called only once during the lifetime of the script instance. Awake is called after all objects are initialized so you can safely speak to other objects or query them using eg. `GameObject.FindWithTag`. Each GameObject's Awake is called in a random order between objects. Because of this, you should use Awake to set up references between scripts, and use Start to pass any information back and forth. Awake is always called before any Start functions. This allows you to order initialization of scripts. Awake can not act as a coroutine.
脚本实例载入时会调用，无论脚本是否 enbaled 用于初始化参数和游戏状态。awake 在所有的对象初始化后调用，因此可以引用其他对象。

### 4. Start

在第一次 enable 后会被调用，在 Update 之前，只调用一次。尽量使用 awake 进行初始化，除非两个脚本的初始化存在依赖关系。awake 会在 start 之前调用

### 5. Update

每帧执行一次，执行频率依赖于帧率。

### 6. FixedUpdate

固定时间间隔执行，不受帧率影响，可在 `Edit --> Project Settings --> Time` 中设置

![outPut](assets/c584f169gw1f9l0nci75fj20cc05674c.jpg)

### 7. LateUpdate

类似于 Update，但是会在所有的 Update 执行完后才执行。

### 8. OnGUI

GUI 绘制，每帧擦除

### 9. OnDestroy

脚本销毁时调用

### 10. OnEnable

在 `awake` 后调用 `OnEnable` 

### 11. OnDisable

脚本不可用时会执行，程序结束时也会执行一次

## 2. 对象

![img](assets/052344532342805.jpg)

### Object

含有 ID 和 name，ID 是唯一的，name 不唯一

### GameObject

所有 entity 的基类，包含 children，parent 和 components

### Component

组件，绑定在一个 GameObject 上，在方法上包含了 GameObject 的部分

### Colider

用于允许碰撞，只有两个物体都有 Colider，且都不是 trigger，且其中一个物体有 Rigidbody 时才会发生碰撞

### Behavior

可以 enable 的 component

### Monobahaviour

脚本基类，会有一个 checkbox 用于控制一些函数，包括

[Start](https://docs.unity3d.com/ScriptReference/MonoBehaviour.Start.html)()
[Update](https://docs.unity3d.com/ScriptReference/MonoBehaviour.Update.html)()
[FixedUpdate](https://docs.unity3d.com/ScriptReference/MonoBehaviour.FixedUpdate.html)()
[LateUpdate](https://docs.unity3d.com/ScriptReference/MonoBehaviour.LateUpdate.html)()
[OnGUI](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnGUI.html)()
[OnDisable](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnDisable.html)()
[OnEnable](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnEnable.html)()

含有很多 Messages，包括 awake、start 等

关于事件机制的讨论，可参考 https://www.zhihu.com/question/27752591

因为很多事件，而很多脚本其实不需要那些事件，所以重点需要优化的是避免空调用。

还有调用协程和延迟调用。

## 3. 协程

### 迭代器 IEnumerator 与协程 Coroutine

https://blog.csdn.net/lijianpeng1024/article/details/79214280

`IEnumerator` 接口

```csharp
public interface IEnumerator
{
    object Current { get; }
    bool MoveNext(); // 注意返回值
    void Reset();
}
```

```csharp
IEnumerator Func()
{
    Debug.Log("Hello world.");
}

void Do()
{
    Func(); // 不会执行 Func，也就不会输出 "Hello world."
}
```

返回值为 `IEnumerator` 的函数并不是函数，更类似于**函数迭代器**。C# 编译时会将其当做一种特殊的对象。

> 其实就是语法糖

https://blog.csdn.net/a1459078670/article/details/74853254

![img](assets/052340394846616.jpg)