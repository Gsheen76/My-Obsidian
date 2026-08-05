这个作业将教你使用一个基于Nvidia Cuda的重建软件包。

# step1

解压Release.zip压缩包。我们将使用压缩包中的mgfpj.exe（用于Radon变换正投影）和mgfbp.exe（用于滤波反投影重建）程序。程序可模拟平板探测器扇束（锥束）的正投影和重建，将利用外部jsonc格式配置文件作为重建或正投影的参数。为方便使用，可将程序所在目录加入windows系统路径。
![300](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260418212341005.png)![391](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260418212543884.png)

# step2

用于正投影的原始图像：将img/img_test.raw文件拖入imagej。用如下参数打开该文件。观察图像。
![244](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260418212724785.png)![296](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260418212741718.png)

# step3

利用mgfpj.exe程序对img/img_test.raw做Radon变换。假设img_test.raw每个像素尺寸为$0.4 mm × 0.4 mm$，像素值的单位是$mm^{-1}$. 使用平行束正投影，在360度内投影360个投影角；探测器像素大小为0.5mm，一行有400个像素。针对以上要求，更改config_mgfpj.jsonc文件：

a)      文件选项. Input/Outputdir代表输入和输出目录（即用于正投影图像所在目录和正投影图像的输出存储目录）。InputFiles代表输入文件名，该处使用正则表达式，截图中的设置会读取输入目录中以“img”开头“.raw”结尾的文件用于正投影。OutputFilePrefix为输出文件同一前缀，可为空（如截图）。OutputFileReplace为输出文件对输入文件名的替换。例如，截图中的设置会将img/img_test.raw文件做正投影后存入sgm/sgm_test.raw文件中。**注：若输出文件夹不存在，需要手动新建输出文件夹，否则程序会报错！**
```json
  /*********************************************************
  * input and output directory and files
  *********************************************************/
  "InputDir": "./img/",
  "OutputDir": "./sgm",

  // all the files in the input directory, use regular expression
  "InputFiles": "img_.*.raw",
  // output file name (prefix, replace)
  "OutputFilePrefix": "",
  // replace substring in input file name
  "OutputFileReplace": [ "img_", "sgm_" ],
```
b)     原始图像维度信息。ImageDimension为原始图像沿x或y的像素数（程序默认原始图像为方形）。PixelSize为原始图像的像素大小（单位：毫米）。根据之前提到的参数将相应值填入。
```json
  /*********************************************************
  * image parameters
  *********************************************************/
  // image dimension (integer)
  "ImageDimension": 512,
  /* pixel size or image size, just use one of them */
  // image pixel size [mm]
  "PixelSize": 0.4,
```
c)       正投影信息。SourceIsocenterDistance，SourceDetectorDistance分别为光源至转轴中心距离以及光源至探测器距离（单位：毫米）。由于问题要求的是平行束投影，可将这两个值设置成相对于探测器尺寸很大的值（例如同时设置为10000）以模拟平行束投影（思考：为什么可以这么做）。DetectorElementCount为探测器像素数，Views为投影数（默认360度full scan），DetectorElementSize为探测器像素大小（单位：毫米）。根据之前提到的参数将相应值填入。
```json
  /*********************************************************
  * geometry and detector parameters
  *********************************************************/
  // source to isocenter distance [mm]
  "SourceIsocenterDistance": 10000,
  // source to detector distance [mm]
  "SourceDetectorDistance": 10000,
  //`SourceIsocenterDistance` 和 `SourceDetectorDistance` 设为 10000 mm，远大于物体尺寸（约 512×0.4 = 204.8 mm），可近似模拟平行束投影
  
  // number of detector elements
  "DetectorElementCount": 400,
  // number of views for reconstruction
  "Views": 360,
  // the physical size of detector element size [mm]
  "DetectorElementSize": 0.5,
```
d)     以下为默认参数，无需更改。
```json
  /*********************************************************
  * parameters by default
  *********************************************************/
  // number of slices in each image file
  "SliceCount": 1,
  // start angle (positive counterclockwise) [degree]
  "StartAngle": 0,
  // oversample sinogram by increasing the number of detector elements by the factor of number below
  "OversampleSize": 2,
    // the position (coordinate) of detector center [mm]
    "DetectorOffcenter": 0,
    // (OPTIONAL) Whether the cone beam recon is needed
  // in case of "false", all other items related to cone beam recon will be null
  "ConeBeam": false
```
e)      在windows命令行或者powershell运行mgfpj.exe程序，以config_mgfpj.jsonc为配置文件，如果运行正确，你将会看到如下返回信息：
![](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260419120919564.png)
正投影所得数据将存入sgm/sgm_test.raw，将该文件拖入imagej中，设置如下参数打开该文件，观察图像。判断图像哪一个方向是探测器方向，哪一个是投影角方向（横向或者纵向）。
![234](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260419120944119.png)![293](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260419121202729.png)
f)      假设原始图像的像素大小不是0.4 mm而是0.2 mm，其余条件相对于e）不变，重复上述流程，观察所得sgm/sgm_test.raw文件，比较与e）中模拟结果的差异（包括图像值得差异），思考差异产生的原因。
![278](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260419121635581.png)
```text
像素尺寸直接影响物体物理大小
在像素数量固定（512×512）的情况下，`PixelSize` 越小，物体实际尺寸越小。Radon 变换的线积分与物体尺寸成正比。
```
g)     假设探测器的像素大小不是0.5mm而是1 mm，其余条件相对于e）不变，重复上述流程，观察所得sgm/sgm_test.raw文件，比较与e）中模拟结果的差异（包括图像值得差异），思考差异产生的原因。
![279](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260419123131100.png)
```text
探测器总宽度变化（因像素数固定）
    像素数 400 不变，像素尺寸加倍 → 总宽从 200 mm 变为 400 mm → 完全覆盖物体，消除截断伪影。
```
# step4

使用mgfbp.exe程序对sgm/sgm_test.raw做Radon变换进行图像重建。重建图像为512 x 512像素，重建图像像素大小为0.4 mm。针对以上要求，更改config_mgfpj.jsonc文件：

a)      文件选项.意义与config_mgfpj.jsonc类似。例如，截图中的设置会将sgm/sgm_test.raw文件做重建后存入rec/rec_test.raw文件中。**注：若输出文件夹不存在，需要手动新建输出文件夹，否则程序会报错**！
```json
  /*********************************************************
  * input and output directory and files
  *********************************************************/
  "InputDir": "./sgm",
  "OutputDir": "./rec",
  // all the files in the input directory, use regular expression
  "InputFiles": "sgm_.*.raw",
  // output file name (prefix, replace)
  "OutputFilePrefix": "",
  // replace substring in input file name
  "OutputFileReplace": [ "sgm_", "rec_" ],
```
b)     正投影图信息。SinogramWidth为正弦图宽度，即探测器一行像素数；SinogramHeight和Views为正弦图高度，即投影角数目（当前应用下SinogramHeight和Views设置为一样的值）；SliceCount为正弦图层数，设置为1；DetectorElementSize为探测器像素大小（单位：毫米）；SourceIsocenterDistance，SourceDetectorDistance分别为光源至转轴中心距离以及光源至探测器距离（单位：毫米），此处设置为之前config_mgfpj中的值。根据3 e) 中config_mgfpj中的参数设置以上参数。
```json
/*********************************************************
  * sinogram and slice parameters
  *********************************************************/
  // number of detector elements
  "SinogramWidth": 400,
  // number of frames
  "SinogramHeight": 360,
  // number of views for reconstruction
  "Views": 360,
  // number of slices in each sinogram file
  "SliceCount": 1,
  // the physical size of detector element size [mm]
  "DetectorElementSize": 0.5,
  // source to isocenter distance [mm]
  "SourceIsocenterDistance": 10000,
  // source to detector distance [mm]
  "SourceDetectorDistance": 10000,
```
c)      重建参数：ImageDimension为重建图像沿某一方向像素数（默认重建图像为正方形）；PixelSize为重建图像像素尺寸。依据所给的重建要求更改参数。最下方为重建滤波核，可选四种，格式为“重建核名：参数”。较常用的重建核为“HammingFilter”和“GaussianApodizedRamp”，具体含义见注释。重建核先按照截图中设置。
```json
/*********************************************************
  * reconstruction parameters
  *********************************************************/
  // image dimension (integer)
  "ImageDimension": 512,
  // image pixel size [mm]
  "PixelSize": 0.4,
   /* reconstruction kernel, avaliable list:
  *  1. "HammingFilter": t + (1-t)*cos(pi*k/ 2*kn), 1 for ramp kernel, 0 for consine kernel, others are in-between
  *  2. "QuadraticFilter": (for bone-plus kernel) tow parameters for t and h, three parameters for a, b, c
  *  3. "Polynomial": an*k^n + ... + a1*k + a0, (n <= 6)
  *     (For Bone plus kernel: [ -15.9236, -2.1540, 3.1106, 2.3872, 1.0000 ], rebin detector element to 0.7 mm
  *  4.  "GaussianApodizedRamp": delta (delta=1 match MDCT if sinogram pixel size 0.4 mm), Ramp kernel apodized by a gaussian kernel (exp(-n^2/2/delta^2)), delta is in number of pixels
  */
  "HammingFilter": 3,
```
d)     默认的参数：
```json
  /*********************************************************
  * parameters by default
  *********************************************************/
  // rotate the image (positive counterclockwise) [degree]
  "ImageRotation": 0,
  // image center [x(mm), y(mm)]
  "ImageCenter": [ 0, 0 ],
  // (OPTIONAL) set water mu to convert the pixel values to HU
  // unit: mm^-1
  //"WaterMu": 0.02,  // save filtered sinogram data
  "SaveFilteredSinogram": false,  // the position (coordinate) of detector center [mm]
  "DetectorOffcenter": 0
```
e)      重建3 e)生成的投影图：在windows命令行或者powershell运行mgbp.exe程序,，以config_mgfbp.jsonc为配置文件，如果运行正确，你将会看到如下返回信息：
![](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114346882.png)
重建所得图像将存入rec/rec_test.raw，将该文件拖入imagej中，设置如下参数打开该文件，观察图像，比较重建图像和原始图像img/img_test.raw的值。
![192](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114402049.png)![235](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114419715.png)
f)      假设重建像素大小不是0.4 mm而是0.2 mm，其余条件相对于e）不变，重复上述流程，观察所得rec/rec_test.raw文件，比较与e）中模拟结果的差异（包括图像值的差异），思考差异产生的原因。
![262](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114436786.png)
```text
更小的像素大小可以获得更高的空间分辨率（更多细节信息），但也会带来更大的噪声。
```
g)     假设重建图像不是512 x512而是1024x1024，其余条件相对于e）不变，重复上述流程，观察所得rec/rec_test.raw文件，比较与e）中模拟结果的差异（包括图像值的差异），思考差异产生的原因。
![313](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114444050.png)
```text
视野扩大，空间分辨率不变，噪声水平不变（均匀区域标准差相近）
```
h)     将重建核改为“GaussianApodizedRamp”，参数依次设置为0.5或1或2或3，其余条件相对于e）不变，重复上述流程，观察所得rec/rec_test.raw文件，比较与e）中模拟结果的差异（包括图像值的差异），思考差异产生的原因。
![216](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114552774.png)![216](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114609575.png)![216](assets/任务2%20使用mgfpj和mgfbp正投影反投影程序/file-20260420114624495.png)
```
随着高斯变迹参数增大（0.5→3），图像噪声逐渐降低，但空间分辨率下降、边缘变模糊。
```