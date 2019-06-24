# 光圈值 f-number

[Wiki | F-number](https://en.wikipedia.org/wiki/F-number) 

[百度百科 | 光圈值](https://baike.baidu.com/item/光圈值/10310445) 

光学系统（如照相机镜头）的光圈值 f-number 是系统焦距 focal length 与入射光瞳直径的比值。也叫作 focal ratio，f-ratio 或 f-stop。它是相对孔径 [relative aperture](https://baike.baidu.com/item/%E7%9B%B8%E5%AF%B9%E5%AD%94%E5%BE%84) 的倒数。常记为 $f/N$，其中 N 是 f-number。

定义公式为
$$
N=\frac{f}{D}
$$
其中 f 是焦距 focal length，D 是入射光瞳的直径。

> 如焦距 10mm，入射光瞳直径 5mm，则 f-number 为 2，记为 f/2，此时孔径记为 f/2。

f-number 越大，孔径越小，图像越暗。2 倍 f-number，则亮度变为 1/4。

![320px-Aperture_diagram.svg](assets/320px-Aperture_diagram.svg.jpg)

Sunny 16 rule
An example of the use of f-numbers in photography is the sunny 16 rule: an approximately correct exposure will be obtained on a sunny day by using an aperture of f/16 and the shutter speed closest to the reciprocal of the ISO speed of the film; for example, using ISO 200 film, an aperture of f/16 and a shutter speed of 1⁄200 second. The f-number may then be adjusted downwards for situations with lower light. Selecting a lower f-number is "opening up" the lens. Selecting a higher f-number is "closing" or "stopping down" the lens.

# exposure

https://en.wikipedia.org/wiki/Exposure_(photography)

在摄影中，曝光是指单位面积内到达胶片或电子图像传感器的光量（像面照度 illuminance 乘以曝光时间），由快门速度、镜头光圈和场景亮度 luminance 决定。曝光量以勒克斯秒 lux.s 为单位测量，可由特定区域的曝光值（EV）和场景亮度计算。

luminous exposure 为
$$
H_\mathrm{v}=E_\mathrm{v}t
$$
其中 $E_\mathrm{v}$ 是 illuminance，单位 lx，t 是曝光时间 exposure duration，单位 s。

# film speed

胶片速度 film speed 描述胶片对光的敏感度，由 [sensitometry](https://en.wikipedia.org/wiki/Sensitometry) 决定，并在各种数值尺度上测量，最近的是ISO 系统。ISO 系统用于描述 exposure 和输出图像亮度的关系。低 ISO 需要高曝光，高 ISO 只需低曝光。

luminous exposure H 为
$$
H=\frac{qLt}{N^2}
$$
其中 q 为因子，常见值为 0.65。

saturation-based speed
$$
S_\text{sat}=\frac{78\ \text{lx.s}}{H_\text{sat}}
$$
其中 $H_\text{sat}$ 是不使相机输出发生 clipped 或 bloom 的最大 exposure。saturation speed 的下限由传感器本身决定，通过 A/D 可以提升 saturation speed。

# exposure value

https://en.wikipedia.org/wiki/Exposure_value

在摄影 photography 中，exposure value EV 是一个表示 shutter speed 和 [f-number](#光圈值 f-number) 两参数组合的数值。对于任意静态场景，只要有相同的曝光值，那就可以得到相同的曝光 [exposure](#exposure)。

定义为
$$
EV=\log_2\frac{N^2}{t}
$$
其中 N 是 f-number，t 是曝光时间。

luminous exposure H 和相机设定的关系
$$
H\varpropto\frac{t}{N^2}
$$

> 与曝光时间成正比，与光圈值成平方反比
>
> 我们观察到 EV 是 $t/N^2$ 的倒数对数，EV 越大，H 越小。EV 增加 1，HV 变为 1/4。
>
> 对于亮的场景，EV 要调大些，使得 H 足够小，这样才能捕获场景

“正确”的曝光要求 N、t、L、S 满足曝光方程
$$
\frac{N^2}{t}=\frac{LS}{K}
$$
其中 $L$ 是场景**平均** luminance，S 是 ISO arithmetic speed，K 是常数 12.5（reflected-light meter calibration constant）。

> 换个理解方式
> $$
> L=K\frac{N^2}{tS}
> $$
> 一个场景对应了一个 L，那么我们为了能较好地拍摄场景，需要调节 N、t、S，使得其满足上式。这么设置不一定就是我们想要的结果。

代入 EV 的定义，有
$$
EV=\log_2\frac{LS}{K}
$$

> 上述公式是从“正确”曝光推出来的，所以这里的 EV 是指在特定场景（决定 L）和特定 S 下的“正确” EV，这个 EV 可以指导我们选择合适的 t 和 N。
>
> 注意这里 EV 由两个变量决定

对于 ISO 100，L（由场景决定）与 EV 就有对应关系，如下

|                      Lighting condition                      |                            EV100                             |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
|                           Daylight                           |                                                              |
| Light sand or snow in full or slightly hazy sunlight (distinct shadows) |                              16                              |
| Typical scene in full or slightly hazy sunlight (distinct shadows) |                              15                              |
|        Typical scene in hazy sunlight (soft shadows)         |                              14                              |
|          Typical scene, cloudy bright (no shadows)           |                              13                              |
|                Typical scene, heavy overcast                 |                              12                              |
|             Areas in open shade, clear sunlight              |                              12                              |
|                    Outdoor, natural light                    |                                                              |
|                           Rainbows                           |                                                              |
|                     Clear sky background                     |                              15                              |
|                    Cloudy sky background                     |                              14                              |
|                     Sunsets and skylines                     |                                                              |
|                      Just before sunset                      |                            12–14                             |
|                          At sunset                           |                              12                              |
|                      Just after sunset                       |                             9–11                             |
| The Moon, [altitude](https://en.wikipedia.org/wiki/Altitude_(astronomy)) > 40° |                                                              |
|                             Full                             |                              15                              |
|                           Gibbous                            |                              14                              |
|                           Quarter                            |                              13                              |
|                           Crescent                           |                              12                              |
|     [Blood](https://en.wikipedia.org/wiki/Lunar_eclipse)     | 0 to 3[[6\]](https://en.wikipedia.org/wiki/Exposure_value#cite_note-6) |
|                Moonlight, Moon altitude > 40°                |                                                              |
|                             Full                             |                           −3 to −2                           |
|                           Gibbous                            |                              −4                              |
|                           Quarter                            |                              −6                              |
|                Aurora borealis and australis                 |                                                              |
|                            Bright                            |                           −4 to −3                           |
|                            Medium                            |                           −6 to −5                           |
|                  Milky Way galactic center                   |                          −11 to −9                           |
|                  Outdoor, artificial light                   |                                                              |
|                 Neon and other bright signs                  |                             9–10                             |
|                         Night sports                         |                              9                               |
|                 Fires and burning buildings                  |                              9                               |
|                     Bright street scenes                     |                              8                               |
|           Night street scenes and window displays            |                             7–8                              |
|                    Night vehicle traffic                     |                              5                               |
|                  Fairs and amusement parks                   |                              7                               |
|                    Christmas tree lights                     |                             4–5                              |
|         Floodlit buildings, monuments, and fountains         |                             3–5                              |
|              Distant views of lighted buildings              |                              2                               |
|                   Indoor, artificial light                   |                                                              |
|                          Galleries                           |                             8–11                             |
|           Sports events, stage shows, and the like           |                             8–9                              |
|                      Circuses, floodlit                      |                              8                               |
|                     Ice shows, floodlit                      |                              9                               |
|                    Offices and work areas                    |                             7–8                              |
|                        Home interiors                        |                             5–7                              |
|                    Christmas tree lights                     |                             4–5                              |

对于不同的 ISO speed $S$，有关系
$$
EV_S=EV_\text{100}+\log_2\frac{S}{100}
$$

> 示例
>
> 对于 ISO 400，其与 $EV_\text{100}$ 的关系为
> $$
> EV_\text{400}=EV_\text{100}+\log_2\frac{400}{100}=EV_\text{100}+2
> $$
> 对于 night sports，查表得 9，则 $EV_\text{400}=11$。

简单等式变换后得 s
$$
EV_\text{100}=EV_S-\log_2\frac{S}{100}=\log_2\frac{N^2}{t}-\log_2\frac{S}{100}
$$

# Sunny 16 rule

https://en.wikipedia.org/wiki/Sunny_16_rule

也称为 sunny f/16 rule。

在晴天 sunny day，将孔径设置成 f/16，快门速度 shutter speed 设置成 ISO speed 的导数。

> 示例
>
> ISO 100，则 shutter speed 设置为 1/100 s

