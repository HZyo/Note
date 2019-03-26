# 安装

官网 https://tensorflow.google.cn/

## 1. 安装 Python 开发环境

- 安装 Microsoft Visual C++ 2015 Redistributable 更新 3

  > vs2015和vs2017自带，有的话就不需要安装了
  >
  > 不确定的话也可以尝试安装，如果已安装会有提示
  >
  > 1. 转到 [Visual Studio 下载页面](https://visualstudio.microsoft.com/vs/older-downloads/)，
  > 2. 选择“可再发行组件和生成工具”，
  > 3. 下载并安装 Microsoft Visual C++ 2015 Redistributable 更新 3。

- 安装 python

  > 需要 Python 3.4、3.5 或 3.6，**3.7不可以** 

- 安装 pip

  > pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from [python.org](https://www.python.org/) or if you are working in a [Virtual Environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments) created by [virtualenv](https://packaging.python.org/key_projects/#virtualenv) or [pyvenv](https://packaging.python.org/key_projects/#venv).
  >
  > **Upgrading pip** 
  >
  > ```bash
  > python -m pip install -U pip
  > ```

- 安装 virtualenv

  > ```bash
  > pip install virtualenv
  > # 如果已安装，则更新一下
  > # pip install -U pip virtualenv
  > ```

## 2. 创建虚拟环境

Python 虚拟环境用于将软件包安装与系统隔离开来。

创建一个新的虚拟环境，方法是选择 Python 解释器并创建一个 `./venv` 目录来存放它：

```bash
virtualenv --system-site-packages -p python ./venv
```

> venv 创建在 当前用户 的根目录

激活虚拟环境：

```bash
.\venv\Scripts\activate
```

在不影响主机系统设置的情况下，在虚拟环境中安装软件包。首先升级 `pip`：

```bash
pip install --upgrade pip

pip list  # show packages installed within the virtual environment
```

之后要退出 virtualenv，请使用以下命令：

```bash
deactivate  # don't exit until you're done using TensorFlow
```

## 3. 安装 TensorFlow pip 软件包

请[从 PyPI](https://pypi.org/project/tensorflow/) 中选择以下某个 TensorFlow 软件包来进行安装：

- `tensorflow` - 仅支持 CPU 的当前版本（建议新手使用）
- `tensorflow-gpu` - [支持 GPU](https://tensorflow.google.cn/install/gpu) 的当前版本（Ubuntu 和 Windows）
- `tf-nightly` - 仅支持 CPU 的每夜版（不稳定）
- `tf-nightly-gpu` - [支持 GPU](https://tensorflow.google.cn/install/gpu) 的每夜版（不稳定，Ubuntu 和 Windows）

> 根据建议，先安装 tensorflow

要在 虚拟环境 中安装

```bash
#(venv)
pip install --upgrade tensorflow
```

验证安装效果：

```bash
python -c "import tensorflow as tf; tf.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
```

> i5 8400 支持 AVX 扩展，而 TensorFlow cpu 版本不支持这个
>
> 所以会报警告
>
> ```
> Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
> ```
>
> 因为cpu版本仅做学习用，以后用gpu版本，所以现在忽略这个警告就行
>
> 添加一下代码
>
> ```python
> import os
> os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
> ```
>
> 故使用以下代码验证安装效果
>
> ```python
> python -c "import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'; import tensorflow as tf; tf.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
> ```
>
> 输出结果为
>
> ```
> tf.Tensor(-113.32004, shape=(), dtype=float32)
> ```

## 4. 其他

**安装其他依赖项** 

```bash
pip install matplotlib
pip install h5py
pip install pyyaml
```

