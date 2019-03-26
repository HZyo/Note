# GPU

## 1. 软件

必须要按照官网上的**软件要求**来安装

**2019/01/18** 

- NVIDIA GPU 驱动程序：最新版本即可 `(>=384.x)`
- CUDA：**CUDA 9.0**，安装时**不要安装驱动**，里边的是老版本的
- cuDNN：最新版本即可 `(>=7.2)` ，但必须是对应 **CUDA 9.0** 的

> 如果需要支持其他版本的CUDA，需要自行从源码编译

## 2. 设置

cuDNN 下载下来是个压缩包，文件夹的名字为 `cuda` 

- 可以把里边的文件和文件夹直接拷贝到 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0` 中，这样就免得再为其专门设置环境变量了

- 也可以放在 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\extras` 中

- 或者自行选择一个位置

第2和3种方案要专门为它设置环境变量，就是把 `bin` 放到 `Path` 中

```
CUDA_ROOT = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA
CUDA_PATH_V9_0 = %CUDA_PATH_ROOT%\v9.0
CUDA_PATH = %CUDA_PATH_V9_0%
%CUDA_PATH%\bin
%CUDA_PATH%\libnvvp
```

## 3. tensorflow-gpu

```bash
pip install tensorflow-gpu
```

## 4. 更新库

```bash
pip list --outdated #列出所有过期的库
```

```python
# -*- coding: utf-8 -*-
import pip
# pip V10.0.0以上版本需要导入下面的包
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call
from time import sleep
 
for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
```

## 5. 注意事项

刚开始运行时会出现卡顿，因为加载gpu需要一定时间，稍等即可

