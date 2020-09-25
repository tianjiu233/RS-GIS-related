# Lidar

[toc]

如今，激光雷达技术（“光探测和测距”）在遥感界蓬勃发展。我们可以看到如今应用已经较为广泛，例如空中激光扫描（ALS），可用于大规模建筑测量、道路和森林；地面激光扫描（TLS），可用于室外和室内环境中更详细但速度较慢的城市测量；移动激光扫描（MLS）精度比TLS低，但由于传感器安装在在同一辆车上而具有更高的效率。 由于这些技术的发展，近年来可用的三维地理数据和处理技术数量激增。针对三维城市点云的分析，已有许多半自动和自动的方法。这是一个有着良好发展前景的研究领域。然而，对于最佳的检测、分割和分类方法还没有达成共识。所以我们搜集了一些Lidar数据集，供大家使用，希望不断提出新的检测、分割和分类的方法。 

## Lidar相关应用

1. 高精度DEM的制作与生成
2. 基础设施制图
3. 地表变化监测
4. 地表覆盖分类
5. 森林资源调查
6. 矿山测量
7. 电力巡检
8. 数字城市建模



## Lidar点云处理软件

 Lidar点云处理软件

1. [CloudCompare](https://github.com/CloudCompare/CloudCompare) (免费开源)
2. ENVI的Lidar模块(需要License)，能够自动提取DEM/DSM/建筑物/植被等三维模型

go on



## 开源Lidar数据集

### DublinCity数据集

DublinCity数据集是都柏林大学学院（UCD）的城市建模小组通过ALS设备扫描都柏林市中心的主要区域（大约5.6平方公里）。在总共的14亿个点云中包含大约2.6亿个标记点标记（图1）。标记区域位于点云的最密集采样部分内，并且被航空影像完全覆盖。

数据集被被标注为3个级别共13个类。

Level 1：此级别包含粗略的标签，包括四个类别：（a）Building；（b）Ground；（c）Vegetation；（d）Undefined。建筑物都是可居住的城市结构的形状（例如房屋，办公室，学校和图书馆）。地面主要包含位于地形高程的点。植被类别包括所有类型的植物。最后，未定义的点是那些不太受欢迎的点，可以包含在城市元素中（例如垃圾桶，装饰雕塑，汽车，长凳，电线杆，邮政信箱和非静态物体）。大约10％的被标记为未定义，它们主要是河流，铁路和建筑工地的点。

Level 2：在此级别中，级别1的前三个类别进一步精细分类。建筑物被标记为屋顶和外墙；植被被分为不同的植物（例如树木和灌木丛）；地面点分为街道，人行道和草地。

Level 3：包括屋顶（例如屋顶窗和天窗）和外墙上的任何类型的门窗。 

* paper: [DublinCity: Annotated LiDAR Point Cloud and its Applications](https://arxiv.org/abs/1909.03613?context=cs.LG)
* [website](https://v-sense.scss.tcd.ie/DublinCity/ )

### WHU-TLS数据集

武大空间智能研究所课题组结合课题组近十年来的数据积累，联合慕尼黑工业大学、芬兰大地所、挪威科技大学、代尔夫特理工大学发布全球最大规模和最多样化场景类型的TLS点云配准基准数据集。目前公开的WHU-TLS基准数据集涵盖了地铁站、高铁站、山地、森林、公园、校园、住宅、河岸、文化遗产建筑、地下矿道、隧道等11种不同的环境，共包含115个测站、17.4亿个三维点以及点云之间的真实转换矩阵。此外，该基准数据集也为铁路安全运营、河流勘测和治理、森林结构评估、文化遗产保护、滑坡监测和地下资产管理等应用提供了典型有效数据。 

* paper: ["Registration of large-scale terrestrial laser scanner point clouds: A review and benchmark"](https://www.sciencedirect.com/science/article/abs/pii/S0924271620300836)
* [website](http://3s.whu.edu.cn/ybs/en/benchmark.htm)

### Paris-rue-Madame数据集

 Paris-rue-Madame数据集包是由三维移动激光扫描仪收集得到。数据收集于法国巴黎第六区的一个街道rue Madame，试验区包含从rue Mézières至rue Vaugirard的160米长的街道；数据获取时间为2013年2于8日13:30。

这个数据集是在TerraMobilita项目的框架下开发的。它是由位于法国普里斯帕里斯蒂奇矿山的机器人实验室（CAOR）的LARA2-3D三维激光扫描仪获得的。数据标注是由法国枫丹白露矿业中心（MINES ParisTech）的数学形态学中心（CMM）以人工辅助的方式进行的。

数据集包含两个ply文件，每个ply文件包含有1000万个点。每个文件包含一个点列表（x, y, z, reflective, label, class），其中x, y, z对应于Lambert 93和altitude IGN1969（grid RAF09）参考坐标系中的地理参考坐标（E, N, U），reflective是激光强度，label是分割后获得的对象标签，class是对象类别。 

* paper:[Paris-rue-Madame database: a 3D mobile laser scanner  dataset for benchmarking urban detection, segmentation and  classification methods](https://hal.archives-ouvertes.fr/hal-00963812)
* [website]( http://www.cmm.mines-paristech.fr/~serna/rueMadameDataset.html)



Reference:

* https://www.shangyexinzhi.com/article/2297289.html