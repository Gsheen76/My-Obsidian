# Normalized metal artifact reduction （NMAR） in computed tomography

**归一化金属伪影抑制（NMAR）在计算机断层扫描中的应用**

View online: [http://dx.doi.org/10.1118/1.3484090](http://dx.doi.org/10.1118/1.3484090)

# abstract 摘要

### Purpose:

While modern clinical CT scanners under normal circumstances produce high quality images, severe artifacts degrade the image quality and the diagnostic value if metal prostheses or other metal objects are present in the field of measurement. Standard methods for metal artifact reduction MAR replace those parts of the projection data that are affected by metal the so-called metal trace or metal shadow by interpolation. However, while sinogram interpolation methods efficiently remove metal artifacts, new artifacts are often introduced, as interpolation cannot com pletely recover the information from the metal trace. The purpose of this work is to introduce a generalized normalization technique for MAR, allowing for efficient reduction of metal artifacts while adding almost no new ones. The method presented is compared to a standard MAR method, as well as MAR using simple length normalization. 

目的：虽然现代临床CT扫描仪在正常情况下能产生高质量的图像，但如果测量场中存在金属假体或其他金属物体，严重的伪影会降低图像质量和诊断价值。金属伪影抑制（MAR）的**标准方法**是用插值法替换受金属影响的投影数据部分（所谓的金属轨迹或金属阴影）。然而，虽然投影图插值法能有效地去除金属伪影，但由于插值法无法完全恢复金属轨迹中的信息，因此常常会引入新的伪影。本工作的目的是介绍一种通用的MAR归一化技术，能够有效抑制金属伪影，同时几乎不引入新的伪影。将所提出的方法与标准的MAR方法以及使用简单长度归一化的MAR方法进行了比较。

### Methods:

In the first step, metal is segmented in the image domain by thresholding. A 3D forward projection identifies the metal trace in the original projections. Before interpolation, the projections are normalized based on a 3D forward projection of a prior image. This prior image is obtained, for example, by a multithreshold segmentation of the initial image. The original rawdata are divided by the projection data of the prior image and, after interpolation, denormalized again. Simulations and measurements are performed to compare normalized metal artifact reduction NMAR to standard MAR with linear interpolation and MAR based on simple length normalization.

方法：在第一步中，通过阈值分割在图像域中分割金属。三维前向投影识别原始投影中的金属轨迹。在插值之前，基于先前图像的三维前向投影对投影进行归一化。该先前图像例如通过初始图像的多阈值分割获得。原始原始数据除以先前图像的投影数据，并在插值后再次反归一化。进行模拟和测量以比较归一化金属伪影校正（NMAR）与线性插值的标准MAR以及基于简单长度归一化的MAR。

### Results:

Promising results for clinical spiral cone-beam data are presented in this work. Included are patients with hip prostheses, dental ﬁllings, and spine ﬁxation, which were scanned at pitch values ranging from 0.9 to 3.2. Image quality is improved considerably, particularly for metal implants within bone structures or in their proximity. The improvements are evaluated by comparing proﬁles through images and sinograms for the different methods and by inspecting ROIs. NMAR outperforms both other methods in all cases. It reduces metal artifacts to a minimum, even close to metal regions. Even for patients with dental ﬁllings, which cause most severe artifacts, satisfactory results are obtained with NMAR. In contrast to other methods, NMAR prevents the usual blurring of structures close to metal implants if the metal artifacts are moderate.

结果：本研究展示了临床螺旋锥束数据的有希望的结果。其中包括带有髋关节假体、牙科填充物和脊柱固定器的患者，这些患者以 0.9 至 3.2 的螺距值进行扫描。图像质量得到了显著改善，特别是对于骨骼结构内或其附近的金属植入物。通过比较不同方法的图像和正弦图的剖面以及检查感兴趣区域 (ROI) 来评估改进。NMAR 在所有情况下均优于其他两种方法。它将金属伪影减少到最低限度，即使在靠近金属区域也是如此。即使对于引起最严重伪影的牙科填充物患者，使用 NMAR 也获得了满意的结果。与其他方法相比，如果金属伪影适中，NMAR 可以防止金属植入物附近结构的通常模糊。

### Conclusions:

Conclusions: NMAR clearly outperforms the other methods for both moderate and severe artifacts. The proposed method reliably reduces metal artifacts from simulated as well as from clinical CT data. Computationally efficient and inexpensive compared to iterative methods, NMAR can be used as an additional step in any conventional sinogram inpainting-based MAR method. © 2010 Ameri can Association of Physicists in Medicine. 

结论：对于中度和重度伪影，NMAR 的性能明显优于其他方法。所提出的方法能够可靠地减少模拟 CT 数据和临床 CT 数据中的金属伪影。与迭代方法相比，NMAR 在计算上更有效且成本更低，可以作为任何传统投影图修复方法的附加步骤。© 2010 美国医学物理学家协会。

### Key words:

metal artifact reduction, metal artifact correction, metal artifacts, image quality, sinogram inpainting

关键词：金属伪影抑制，金属伪影校正，金属伪影，图像质量，投影数据修复


I. INTRODUCTION

引言

I.A. Overview

概述

Modern CT scanners are able to produce high quality images, and under ideal circumstances共a water cylinder in a well-calibrated scanner兲, CT values can reach an accuracy of 1 HU.1 However, if metal objects are present in the ﬁeld of measurement, severe artifacts with a magnitude of up to several hundred HU degrade the image quality and diagnostic value.

现代CT扫描仪能够产生高质量的图像，在理想情况下（例如，在校准良好的扫描仪中对水体进行扫描），CT值可以达到1 HU的精度。1然而，如果测量场中存在金属物体，高达数百HU的严重伪影会降低图像质量和诊断价值。

There are various effects that lead to the formation of artifacts in the presence of metal objects. Metals have much higher densities and higher atomic numbers compared to body tissue. Also, metal implants usually have sharply deﬁned boundaries. Because of these reasons, noise, beam hardening artifacts, scatter artifacts, and nonlinear partial volume artifacts are much more severe than in cases without metal. The term metal artifact is a generic term for all of these artifacts.

在金属物体存在的情况下，有多种效应会导致伪影的形成。与人体组织相比，金属的密度和原子序数要高得多。此外，金属植入物通常具有清晰定义的边界。由于这些原因，与没有金属的情况相比，噪声、束硬化伪影、散射伪影和非线性部分容积伪影更为严重。金属伪影一词是所有这些伪影的总称。

Low-contrast structures may be easily obscured by metal artifacts. Tumors in the tongue, for example, might remain undetected in the presence of dental ﬁllings. Additional scans with higher tube current and higher tube voltage or with a patient position avoiding metal implants in the scan plane might be necessary. Thus, the patient dose is increased.

低对比度结构可能很容易被金属伪影所遮蔽。例如，在存在牙科填充物的情况下，舌部肿瘤可能仍未被检测到。可能需要进行额外的扫描，提高管电流和管电压，或者调整患者体位以避开扫描平面内的金属植入物。因此，患者剂量增加。

Various types of metal artifact reduction共MAR兲methods have been proposed since the ﬁrst publications on MAR.2,3 They can be grouped into sinogram inpainting methods, iterative methods, statistical methods, and ﬁltering methods. To our knowledge, no commercially available CT scanner is currently providing metal artifact reduction software, and therefore, metal implants remain a major source of artifacts in computed tomography.

自首次发表关于金属伪影减除（MAR）的文献以来，已提出了多种金属伪影减除（MAR）方法。2,3 这些方法可分为投影数据修复法、迭代法、统计法和滤波法。据我们所知，目前没有商用CT扫描仪提供金属伪影减除软件，因此，金属植入物仍然是计算机断层扫描中伪影的主要来源。

Sinogram inpainting methods, which are most common MAR methods, use interpolation3–5 or forward projections6–8,24 to complete the sinogram, where metalaffected values are treated as missing data. Filtering methods try to make use of all the available information and not to replace parts of projections.9,10 Iterative methods provide a means of incorporating additional knowledge, as, for example, the physics behind the acquisition process or photon statistics.11–14 Statistical methods are less sensitive to noise than ﬁltered backprojection. As shown in Ref. 15, a combination of different methods can be advantageous. Another interesting approach that has been pursued is MAR with total variation minimization.16

正弦图修复方法是最常用的金属伪影去除（MAR）方法，它们通过插值3–5或前向投影6–8,24来补全正弦图，其中将受金属影响的值视为缺失数据。滤波方法试图利用所有可用信息，而不是替换投影的一部分。9,10 迭代方法提供了一种结合额外知识的途径，例如，采集过程背后的物理原理或光子统计学。11–14 统计方法比滤波反投影对噪声的敏感度较低。如文献15所示，结合不同方法可能是有益的。另一种被追求的有趣方法是具有全变分最小化的金属伪影去除（MAR）。16

I.B. Sinogram inpainting

正弦图修复

Sinogram inpainting methods, which are most widely spread among MAR methods, treat those parts of the projection data that are affected by metal共the so-called metal trace or metal shadow兲as missing data. The underlying idea is to consider any sinogram values as completely unreliable if the corresponding rays have intersected metal objects.

在金属伪影去除（MAR）方法中最为广泛的 असं，正弦图修复方法将受金属影响的投影数据部分（所谓的金属轨迹或金属阴影）视为缺失数据。其基本思想是，如果相应的射线与金属物体相交，则认为任何正弦图值都完全不可靠。

These methods make use of interpolation3–5 or forward projection6–8 to complete the sinogram by inpainting the surrogate data into the metal trace. The simplest example is linear interpolation in the channel direction, as proposed in Ref. 3. This method is referred to as MAR1 this work. Metal is found by a thresholding operation in the uncorrected image. The metal-only image is subject to a forward projection. Nonzero entries in the obtained metal sinogram deﬁne the metal trace, which determines the part of the original rawdata that has to be replaced. After interpolation, the image is reconstructed. A major drawback of pure interpolation methods is the loss of information, especially edge information in the metal trace, which results in blurring of the corresponding edges in the image. Another negative effect is the formation of streak artifacts tangent to metal objects, which are introduced if the transition between original and interpolated projection data is not smooth enough.17 These effects are most prominent in regions close to metal objects because a greater part of surrogate sinogram values contributes here. The severely reduced image quality close to implants is especially disturbing when the prostheses are related to the reason for scheduling a patient for CT. It is therefore necessary to pay attention to the proximity of metal objects and to avoid the creation of new artifacts there. Besides linear interpolation 共MAR1兲, many different and more complex interpolation schemes have been applied in order to obtain more accurate surrogate data. For example, distance weighted, directional, spline vs. Fourier-based, and smooth interpolation have been investigated in Refs. 4 and 18–21. The problem itself—the loss of information in the metal trace and hence the introduction of new artifacts—remains the same.

这些方法利用插值3-5或前向投影6-8，通过修复替代数据到金属轨迹中来完成 the sinogram。最简单的例子是在通道方向上的线性插值，如文献3中所提出的。本工作中将此方法称为MAR1。金属通过在未校正图像中的阈值操作来检测。仅包含金属的图像进行前向投影。获得的金属 the sinogram 中的非零项定义了金属轨迹，该轨迹确定了需要替换的原始原始数据的部分。插值后，重建图像。纯插值方法的一个主要缺点是信息丢失，尤其是在金属轨迹中的边缘信息丢失，这会导致图像中相应边缘的模糊。另一个负面影响是形成与金属物体相切的条纹伪影，如果原始和插值投影数据之间的过渡不够平滑，就会引入这些伪影。17 这些效应在靠近金属物体的区域最为明显，因为替代 the sinogram 值在这些区域的贡献更大。靠近植入物的图像质量严重下降，当假体与患者安排CT的原因相关时，尤其令人不安。因此，有必要注意金属物体的邻近性，并避免在那里产生新的伪影。除了线性插值 共MAR1兲 外，还应用了许多不同且更复杂的插值方案，以获得更准确的替代数据。例如，在文献4和18-21中研究了距离加权、定向、样条与傅里叶基和光滑插值。例如，在文献4和18-21中研究了距离加权、定向、样条与傅里叶基和光滑插值。问题本身——金属轨迹中的信息丢失以及由此引入的新伪影——仍然存在。

In Ref. 17, a length normalization of the sinogram prior to interpolation is used to obtain better contrast between air and objects of water-equivalent material. This method is referred to as MAR2 in this work. However, regions close to bone structures and between bone and metal are still impaired. This work introduces the normalized metal artifact reduction 共NMAR兲to overcome these drawbacks.22

在参考文献17中，在插值之前对 ज्यामितीय (sinogram) 进行长度归一化，以获得空气与水当量材料物体之间更好的对比度。该方法在本工作中称为 MAR2。然而，靠近骨骼结构以及骨骼和金属之间的区域仍然受到损害。本工作引入了归一化金属伪影抑制 共NMAR兲以克服这些缺点。22

II. METHOD

方法

II.A. Idea

思路

In this work, it is shown how typical drawbacks of pure sinogram interpolation methods are overcome with normalized metal artifact reduction共NMAR兲. One problem with interpolation in the sinogram is the lack of smoothness of the transition region from original to interpolated data, which causes streak artifacts. Interpolation is less problematic in homogeneous data. The idea of a proper normalization is to transform the sinogram in a way that it becomes comparatively ﬂat. If the interpolation is performed on a nearly ﬂat, normalized sinogram, the transition between original data and interpolated values is very smooth.

本研究展示了如何通过归一化金属伪影去除（NMAR）[NT0]克服纯粹的投影图插值方法的典型缺点。投影图插值的一个问题是原始数据和插值数据过渡区域的平滑度不足，这会导致条状伪影。在均匀数据中，插值问题较小。适当归一化的思想是通过某种方式转换投影图，使其变得相对平坦。如果在近乎平坦的归一化投影图上执行插值，则原始数据和插值之间的过渡将非常平滑。

One way to transform a sinogram into a more homogeneous form is described in Ref. 17. This method is referred to as MAR2 in this work. In the ﬁrst step, an uncorrected image is reconstructed. The metal trace is determined exactly as for MAR1共thresholding and forward projection of metal兲. The uncorrected sinogram is then normalized by dividing each entry by the intersection length of its corresponding ray and the scanned object. The metal projections determine where data in the normalized sinogram are replaced by interpolation共for example linear interpolation兲. Subsequently, the corrected sinogram is obtained by denormalization. This is done by multiplying the interpolated and normalized sinogram with the intersection lengths again. Reconstruction of this corrected sinogram yields the corrected image.

一种将投影图转换为更均匀形式的方法在文献17中有描述。本研究将此方法称为MAR2。在第一步中，重建一个未经校正的图像。金属伪影的确定方法与MAR1完全相同（阈值化和金属前向投影）。然后，通过将投影图中的每个条目除以其对应射线与被扫描对象的交集长度来对未经校正的投影图进行归一化。金属投影决定了归一化投影图中的数据将被何处插值替换（例如线性插值）。随后，通过反归一化获得校正后的投影图。这是通过将插值和归一化后的投影图再次乘以交集长度来实现的。对该校正后投影图的重建产生校正后的图像。

In contrast to MAR1, MAR2 leads to exact results for the simple case of objects that only consist of one material plus air and metal: Projection values p = Rf共with Rf being the Radon transform or x-ray transform of the scanned object f兲 depend not only on the attenuation coefﬁcients of the materials that f consists of but also on the intersection length of the rays with the material. The sinogram of an object consisting only of metal, one material other than metal and air, would attain an average attenuation value everywhere outside the metal trace if each projection value was divided by the corresponding intersection length. These lengths can be computed by the forward projection of a binarized version of the considered object, which can be found by thresholding. After the division, interpolation of the metal trace is carried out. The whole sinogram now attains an average attenuation value everywhere. The sinogram is multiplied with the intersection lengths afterward.

与MAR1相反，MAR2对于仅由一种材料加上空气和金属组成的简单对象可以得到精确结果：投影值p = Rf共，其中Rf是扫描对象f兲的Radon变换或x射线变换，它不仅取决于材料的衰减系数，还取决于射线与材料的交线长度。如果将每个投影值除以相应的交线长度，那么仅由金属、一种非金属材料和空气组成的对象的投影图将在金属轨迹外部的任何地方获得平均衰减值。这些长度可以通过对所考虑对象的二值化版本的正向投影来计算，二值化版本可以通过阈值处理找到。除法之后，进行金属轨迹的插值。整个投影图现在在任何地方都获得平均衰减值。之后，将投影图与交线长度相乘。

MAR2 leads to excellent results for cases without high contrast. However, in the presence of bones, the normalization with intersection lengths does not lead to a very ﬂat sinogram and new artifacts cannot be avoided. To generalize this idea to more materials, NMAR uses a prior image fprior, which takes bone and potentially other high-contrast structures into account, too.

MAR2在无高对比度的情况下可获得优异的结果。然而，在骨骼存在的情况下，具有交集长度的归一化并未产生非常平坦的正弦图，并且无法避免新的伪影。为了将此思想推广到更多材料，NMAR使用先验图像fprior，该图像也考虑了骨骼及其他潜在的高对比度结构。

Another drawback of pure interpolation methods, as mentioned in the previous section, is the loss of edge information in the metal trace, especially for high-contrast structures. With denormalization, as described later in this section, NMAR restores traces of high-contrast objects in the metal shadow. The information of the shape of these traces is contained in the sinogram of the prior image. In contrast to just replacing sinogram values by sinogram values of the prior image, NMAR ensures a seamless ﬁt of the surrogate data and a recovery of traces of objects that are contained in the prior image. At the same time, the interpolation at least approximately connects the traces that are not included in the sinogram of the prior image and which therefore were not completely ﬂattened in the normalized sinogram.

纯粹插值方法的另一个缺点，如前一节所述，是金属痕迹中的边缘信息丢失，特别是对于高对比度结构。通过本节后面将介绍的去归一化，NMAR 恢复了金属阴影中高对比度物体的痕迹。这些痕迹的形状信息包含在先前图像的投影图中。与仅仅用先前图像的投影图值替换投影图值不同，NMAR 确保了代理数据的无缝拟合以及先前图像中包含的物体的痕迹的恢复。同时，插值至少近似地连接了未包含在先前图像的投影图中的痕迹，因此在归一化投影图中没有被完全展平。

今日阅读近万字，加油！免费翻译额度剩余不足5%

II.B. Algorithm

算法

Figure 1 provides a diagram of the different steps of NMAR. From the original rawdata, an uncorrected image is reconstructed. By thresholding, the metal image is obtained. The prior image is computed by segmentation of soft tissue and bone. Forward projection yields the corresponding sinograms. The original sinogram is then normalized by dividing it by the forward projected prior image. The division is carried out pixelwise. A small positive value teps has to be chosen as threshold for performing the division in order to not divide by zero. Strictly speaking, only the values close to the metal trace need to be normalized and denormalized because only those contribute to the interpolation. The normalized projections pnorm are subject to an interpolation-based MAR operation M共MAR1 in this work兲. Subsequently, the corrected sinogram pcorr is obtained by denormalization of the interpolated, normalized sinogram. This is done by multiplying it with the projection values pprior,

图1展示了NMAR不同步骤的示意图。从原始数据中重建出未校正的图像。通过阈值处理获得金属图像。先验图像通过软组织和骨骼的分割计算得出。前向投影得到相应的投影图。然后通过除以前向投影的先验图像来归一化原始投影图。该除法是逐像素进行的。为了避免除以零，必须选择一个小的正值teps作为执行除法的阈值。严格来说，只有接近金属轨迹的值才需要归一化和反归一化，因为只有这些值才对插值有贡献。归一化后的投影pnorm进行基于插值的MAR运算M（本工作中为MAR1）。随后，通过对插值后的归一化投影图进行反归一化，得到校正后的投影图pcorr。这是通过将其与投影值pprior相乘来实现的，

In this step, the structure information from the prior image is brought back to the metal trace. Traces of high-contrast objects are contained in the sinogram of the prior image. The normalization and multiplication procedure ensures that there is no offset between original and completed data. Traces of low-contrast objects in soft tissue that are not included in the prior image, for example tumors, are still approximately connected by interpolation of the normalized sinogram. After reconstruction, the metal is inserted back into the corrected image. This is done for NMAR, as well as for MAR1 and MAR2.

在此步骤中，来自先前图像的结构信息被带回到金属轨迹。先前图像的 असंरेखित (sinogram) 中包含高对比度物体的痕迹。归一化和乘法过程确保原始数据和完成数据之间没有偏移。软组织中低对比度物体（例如肿瘤）的痕迹，这些痕迹未包含在先前图像中，仍然可以通过归一化 असंरेखित (sinogram) 的插值来近似连接。重建后，将金属插回校正后的图像。这是为 NMAR、MAR1 和 MAR2 完成的。

坚持阅读，收获满满！免费翻译额度剩余约20%

In order to explain the effect of the different steps of NMAR and their difference from MAR2, Fig. 2 shows a correction with NMAR and MAR2 using the example of the simulated hip phantom. Images and the corresponding sinograms are shown and proﬁles through the sinograms are compared.

为了解释NMAR不同步骤的效果及其与MAR2的区别，图2展示了使用模拟髋部体模的NMAR和MAR2校正。展示了图像和相应的投影图，并比较了通过投影图的剖面。

For a reliable replacement of the metal projections, the forward projections need to be performed in 3D, in the exact geometry of the uncorrected projections. A 3D version of the Joseph method is used. The Joseph forward projector is a ray-driven forward projector that applies the trapezoidal rule to approximate line integrals through the volume. The values at the sampling points are determined by linear interpolation between the grid points of the discrete volume.23 To obtain sufﬁcient accuracy of the forward projection, slices of 1.2 mm thick were reconstructed on 0.6 mm increment for the patients scanned with the Deﬁnition Flash scanner共slices of 1 mm thick and 1 mm increment for the patient scanned with the Sensation 16 scanner兲. To reduce aliasing, an aperture of two is simulated by threefold oversampling in the channel direction, i.e., three rays per detector pixel are averaged.

为了可靠地替换金属投影，需要以三维方式执行前向投影，并采用未校正投影的精确几何形状。使用了约瑟夫方法的三维版本。约瑟夫前向投影器是一种射线驱动的前向投影器，它应用梯形法则来近似通过体积的线积分。采样点的数值通过离散体积的网格点之间的线性插值来确定。23 为了获得前向投影的足够精度，对于使用 Definition Flash 扫描仪扫描的患者，以 1.2 毫米的切片厚度和 0.6 毫米的增量进行重建（对于使用 Sensation 16 扫描仪扫描的患者，切片厚度为 1 毫米，增量为 1 毫米）。为了减少混叠，通过在通道方向上进行三倍过采样来模拟孔径为 2，即对每个探测器像素进行三个射线的平均。

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/4/figures/fig.1.4.jpg?ver=1)

FIG. 1. Scheme of NMAR—From the original rawdata, an uncorrected image is reconstructed. By thresholding, the metal image and the prior image are obtained. Forward projection yields the corresponding sinograms. The original sinogram is then normalized by dividing it by the sinogram of the prior. The metal projections determine where data in the normalized sinogram are replaced by interpolation. The interpolated and normalized sinogram is denormalized by multiplying it with the sinogram of the prior image again. Reconstruction yields the corrected image.

图 1. NMAR 方案—从原始数据中重建未校正图像。通过阈值处理得到金属图像和先验图像。前向投影得到相应的投影图。然后通过将原始投影图除以先验图像的投影图进行归一化。金属投影决定了归一化投影图中的哪些数据被插值替换。插值和归一化后的投影图通过再次乘以先验图像的投影图进行去归一化。重建得到校正后的图像。

For MAR1, MAR2, and NMAR, a 3D forward projection has to be computed ﬁrst to identify the metal shadow. Due to the need for projection data of the prior image, NMAR has some additional computational cost compared to pure interpolation methods like MAR1. However, the extra costs are marginal: Merely sinogram values close to and inside the metal trace are needed for normalization and denormalization. Thus, depending on the size of the implants, only very small parts of the prior image have to be forward projected. One additional reconstruction is needed for NMAR if a precorrection with MAR1 is used.

对于MAR1、MAR2和NMAR，首先需要计算三维前向投影以识别金属阴影。由于需要先前图像的投影数据，与MAR1等纯插值方法相比，NMAR具有一些额外的计算成本。然而，额外的成本是微不足道的：仅需要金属轨迹附近和内部的投影图值来进行归一化和反归一化。因此，根据植入物的大小，只需要对先前图像的非常小部分进行前向投影。如果使用MAR1进行预校正，NMAR需要一次额外的重建。

II.C. Prior image

II.C. 先前图像

An important step for NMAR is to ﬁnd a good prior image. It should model the images as close as possible, but contain no artifacts. In order to achieve this, air regions, soft tissue regions, and bone regions have to be identiﬁed. In this work, a simple thresholding was applied to segment air, soft tissue, and bone after the image was smoothed with a Gaussian. To reduce the streak artifacts prior to the segmentation, smoothing in the metal trace, as described in Ref. 17, is also beneﬁcial. An automatic procedure to ﬁnd proper thresholds is described in Ref. 7. The air regions are then set to ⫺1000 HU, the soft tissue parts to 0 HU. Bone pixels keep their values, as they vary too much to properly model them with one value. The value that is assigned to metal is arbitrary. It does not affect the normalization and interpolation because only the sinogram parts close to, but not inside, the metal trace contribute. In the corrected image, the original metal values are ﬁnally reinserted to visualize the implants.

对于NMAR而言，寻找一个好的先验图像是一个重要的步骤。它应该尽可能地模拟图像，但不包含任何伪影。为了实现这一点，必须识别出空气区域、软组织区域和骨骼区域。在这项工作中，在图像用高斯平滑后，应用了一个简单的阈值分割来分割空气、软组织和骨骼。为了在分割之前减少条状伪影，按照参考文献17中所述，在金属轨迹中进行平滑也是有益的。参考文献7描述了一种寻找合适阈值的自动程序。然后将空气区域设置为-1000 HU，软组织部分设置为0 HU。骨骼像素保留其值，因为它们变化太大，无法用一个值来恰当地模拟它们。分配给金属的值是任意的。它不影响归一化和插值，因为只有靠近金属轨迹但不在其内部的正弦图部分才有贡献。在校正后的图像中，最终重新插入原始金属值以可视化植入物。

今日阅读近万字，加油！免费翻译额度剩余约10%

For smaller metal objects of medium density, segmentation can be performed in the uncorrected image. NMAR has the advantage that correction results are not impaired compared to the uncorrected images for volume slices only displaying minor artifacts with just few and small metal implants. This is often the case with MAR1 and MAR2, where the regions close to metal are blurred. More details are provided in the next section. For high artifact content, more reliable results are obtained by segmenting bones from an image that is precorrected, for example, with MAR1. Patients 2 and 3 were precorrected with MAR1. In this case, an MAR1 corrected image is reconstructed ﬁrst. In these cases, NMAR comprises three reconstructions instead of two. Other methods for precorrection can be used, of course.

对于密度中等的较小金属物体，可以在未校正的图像中进行分割。与仅显示少量和小型金属植入物引起的轻微伪影的体积切片相比，NMAR的优点在于校正结果不会受到影响。这在MAR1和MAR2中很常见，其中靠近金属的区域会被模糊化。更多细节将在下一节中提供。对于伪影含量较高的情况，通过分割预校正图像（例如使用MAR1校正）中的骨骼可以获得更可靠的结果。患者2和患者3使用MAR1进行了预校正。在这种情况下，首先需要重建一个MAR1校正后的图像。在这些情况下，NMAR包含三次重建而非两次。当然，也可以使用其他的预校正方法。

今日阅读近万字，加油！免费翻译额度剩余约10%

III. SIMULATIONS AND MEASUREMENTS

III. 模拟与测量

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/5/figures/fig.2.5.jpg?ver=1)

FIG. 2. In order to illustrate the steps of NMAR and their difference from MAR2, images, the corresponding sinograms and proﬁles through sinograms are shown for the hip phantom. Correction results for MAR1 and MAR2 are found in Fig. 5. The uncorrected data are shown in the top row, the correction results at the bottom row. The column on the right hand side shows proﬁles of the sinograms of the corresponding steps of MAR2. For NMAR, the normalized sinogram is obtained by dividing the uncorrected sinogram by the sinogram of the prior image共second row兲. For MAR2, each entry of the uncorrected sinogram is divided by the intersection length共second row兲of the corresponding ray and the scanned object. Third row: The dashed lines in the proﬁles indicate the linearly interpolated values in the metal trace. The MAR2 proﬁle is more homogeneous than the original data, but the bone traces are still visible. The NMAR proﬁle is even more homogeneous than the MAR2 proﬁle. Bottom row: Denormalization of the interpolated proﬁles yields the corrected data. The solid curves in the graphs are the corrected proﬁles, while the dashed curves show the MAR1 result for comparison. Both the MAR2 and the NMAR results are smoother than the MAR1 result. The MAR2 result, however, has less accurate values in the bone trace.共C=0 HU/W=1000 HU兲.

图 2. 为了说明 NMAR 的步骤及其与 MAR2 的区别，展示了包含金属伪影校正（MAR）的髋部模型图像、相应的投影图和穿过投影图的剖面图。MAR1 和 MAR2 的校正结果见图 5。未校正的数据显示在上行，校正结果显示在下行。右侧列显示了 MAR2 相应步骤的投影图剖面。对于 NMAR，通过将未校正的投影图除以先验图像的投影图共第二行兲 来获得归一化投影图。对于 MAR2，未校正投影图的每个条目除以相应射线与扫描物体相交的长度共第二行。第三行：剖面图中的虚线表示金属轨迹中线性插值的值。MAR2 剖面图比原始数据更均匀，但骨骼轨迹仍然可见。NMAR 剖面图比 MAR2 剖面图更均匀。底行：插值剖面的去归一化得到校正后的数据。图中的实线是校正后的剖面，虚线显示了 MAR1 的结果以供比较。MAR2 和 NMAR 的结果都比 MAR1 的结果更平滑。然而，MAR2 的结果在骨骼轨迹中的值不够准确。共 C=0 HU/W=1000 HU兲。

III.A. Simulations

III.A. 模拟

To evaluate the potential of NMAR, scans of phantoms for two clinical situations where metal artifacts occur are simulated: Hip replacement by titanium prostheses and spinal fusion using pedicle screws. Semianthropomorphic software phantoms from the FORBILD group [共http://www.imp.uni-erlangen.de/phantoms/](http://www.imp.uni-erlangen.de/phantoms/兲were)[兲were](http://www.imp.uni-erlangen.de/phantoms/兲were) simulated using DRASIM共Siemens Healthcare, Forchheim, Germany兲. The geometry of the phantoms is presented in Fig. 3. Simulations of the phantoms without metal and without noise are displayed in Fig. 3, too, and serve as reference. Noise, beam hardening, and nonlinear partial volume effects are taken into account during simulation. Realistic material compositions for soft tissues and bone tissues are simulated. Simulation parameters were 120 kV, 0.6 mm slice width, 672 channels, and 1160 views per rotation. To have a ﬁnite beam width, 25 rays per detector element were simulated.

为评估NMAR的潜力，模拟了两种发生金属伪影的临床情况下的模体扫描：钛合金假体行髋关节置换术和椎弓根螺钉行脊柱融合术。使用DRASIM（西门子医疗，福希海姆，德国）模拟了来自FORBILD小组[共http://www.imp.uni-erlangen.de/phantoms/](http://www.imp.uni-erlangen.de/phantoms/兲were)[NT1]兲的半人体模型软件模体。模体的几何结构如图3所示。图3也显示了无金属、无噪声模体的模拟结果，并作为参考。模拟中考虑了噪声、束硬化和非线性部分容积效应。模拟了软组织和骨组织的真实材料成分。模拟参数为120 kV，0.6 mm层宽，672通道，每次旋转1160个视角。为了获得有限的束宽，模拟了每个探测器单元25条射线。

III.B. Measurements

III.B. 测量

To demonstrate the beneﬁts of NMAR in comparison to MAR1 and MAR2, results for four patients are presented in this work, scanned at pitch values ranging from 0.9 to 3.2. Uncorrected images of each patient are shown in Fig. 4. Patient 1 is a case with bilateral hip endoprostheses. Patient 2 has one hip total endoprosthesis, while patient 3 has metallic dental ﬁllings. The spine of patient 4 is ﬁxed with a Harrington rod. The scan of patient 1 was acquired with a Somatom Sensation 16共140 kV, 320 mA s, 16⫻ 0.75 mm collimation, and 1.0 spiral pitch兲. Patients 2–4 were acquired with a Somatom Deﬁnition Flash scanner. This scanner is a third generation clinical dual source scanner with 64 detector rows per detector, ﬂying focal spot and allows for pitch values up to 3.4.

为了展示NMAR相对于MAR1和MAR2的优势，本研究展示了四名患者的结果，其扫描螺距值范围为0.9至3.2。图4显示了每位患者的未校正图像。患者1是一名患有双侧髋关节假体的病例。患者2有一侧全髋关节假体，而患者3有金属牙科填充物。患者4的脊柱用Harrington杆固定。患者1的扫描使用Somatom Sensation 16共140 kV、320 mAs、16×0.75 mm准直和1.0螺旋螺距获得。患者2-4使用Somatom Definition Flash扫描仪获得。该扫描仪是第三代临床双源扫描仪，每个探测器有64个探测器排，具有飞行焦点，并且允许的螺距值高达3.4。

IV. RESULTS

IV. 结果

Results for simulations and clinical data sets, corrected with MAR1, MAR2, and NMAR, are presented in this section. Solid arrows are used to highlight the position of artifacts that are introduced by a correction method. For comparison, outlined arrows mark the same position in an image that does not show an artifact there, and thus imply that the used correction method is superior. The metal artifacts in the uncorrected images, streaks which go through metal, are obvious. Arrows in the uncorrected images mark the position of the metal parts. The results for the patients are presented in two window settings—a narrow window for a better evaluation of streak artifacts and a wider window in order to examine bones and the location and shape of the metal implants.

本节将展示使用 MAR1、MAR2 和 NMAR 方法校正后的模拟和临床数据集的结果。实心箭头用于突出显示由校正方法引入的伪影的位置。为了进行比较，轮廓箭头标记了图像中不存在伪影的相同位置，从而暗示所使用的校正方法更优。未校正图像中的金属伪影，即穿过金属的条纹，是显而易见的。未校正图像中的箭头标记了金属部件的位置。患者的结果以两种窗口设置呈现——一种窄窗口用于更好地评估条纹伪影，另一种宽窗口用于检查骨骼以及金属植入物的位置和形状。

IV.A. Simulation

IV.A. 模拟

Reconstructions of the simulated hip phantom and the simulated thorax phantom, without correction and corrected with MAR1, MAR2, and NMAR are displayed in Fig. 5. The original streak artifacts are removed successfully by each method. However, MAR1 leads to severe new artifacts in both cases: Blurring of the bone near the implant due to loss of edge information and streak artifacts tangent to the former region of the implant. Compared to MAR1, MAR2 visibly enhances image quality for the thorax phantom, but not for the hip phantom. In the thorax phantom, the lungs are ﬁlled with air. The binary image, which is used with MAR2 to compute the intersection lengths, contains the information about the shape of the lungs. Therefore, artifacts that are introduced by errors in the traces of the lungs can be avoided. Artifacts close to bones are still present after the correction with MAR2. After correction with NMAR, images exhibit considerably less artifacts for both phantoms. The simulations show that even ﬁne bone structures can be preserved.

图 5 显示了模拟髋部模型和模拟胸部模型的重建图像，包括未校正以及使用 MAR1、MAR2 和 NMAR 进行校正后的图像。原始的条纹伪影被每种方法成功去除。然而，MAR1 在两种情况下都会导致严重的新的伪影：由于边缘信息丢失导致植入物附近的骨骼模糊，以及切线于植入物先前区域的条纹伪影。与 MAR1 相比，MAR2 明显提高了胸部模型的图像质量，但对髋部模型无效。在胸部模型中，肺部充满空气。与 MAR2 一起用于计算交集长度的二值图像包含有关肺部形状的信息。因此，可以避免由肺部轨迹误差引起的伪影。使用 MAR2 校正后，靠近骨骼的伪影仍然存在。使用 NMAR 校正后，两种模型的图像伪影明显减少。模拟表明，即使是精细的骨骼结构也可以被保留。

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/6/figures/fig.3.6.jpg?ver=1)

FIG. 3. FORBILD hip phantom and FORBILD thorax phantom. The arrows mark the position of the metal implants. On the left hand side, the geometry of the phantoms is presented. On the right hand side, simulations of the phantoms without metal and without noise are displayed.共C=0 HU/W=1000 HU兲and 共C=500 HU/W=2500 HU兲.

图 3. FORBILD 髋部模型和 FORBILD 胸部模型。箭头标示了金属植入物的位置。左侧展示了模型的几何结构。右侧展示了无金属、无噪声模型的模拟结果。共C=0 HU/W=1000 HU兲和 共C=500 HU/W=2500 HU兲。

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/6/figures/fig.4.6.jpg?ver=1)

FIG. 4. The four patients considered in this work. Patient 1: Bilateral hip prostheses共C=0 HU/W=500 HU兲. Patient 2: Unilateral hip prosthesis共C =0 HU/W=500 HU兲. Patient 3: Dental ﬁllings共C=100 HU/W=750 HU兲and共C=300 HU/W=1500 HU兲. Patient 4: Harrington rod for spine ﬁxation 共C=0 HU/W=1000 HU兲. The arrows mark the locations of the metal implants.

图 4. 本工作中考虑的四位患者。患者 1：双侧髋关节假体共C=0 HU/W=500 HU兲。患者 2：单侧髋关节假体共C =0 HU/W=500 HU兲。患者 3：牙科填充物共C=100 HU/W=750 HU兲和共C=300 HU/W=1500 HU兲。患者 4：用于脊柱固定的 Harrington rod 共C=0 HU/W=1000 HU兲。箭头标示了金属植入物的位置。

IV.B. Measurements

IV.B. 测量

IV.B.1. Patient 1

IV.B.1. 患者 1

For patient 1, the patient with two implants, the results are shown in Fig. 6. The uncorrected image suffers from ﬁne streak artifacts and a prominent beam hardening artifact between the two implants. MAR1, MAR2, and NMAR all remove these artifacts. However, MAR1 introduces spurious streaks tangent to the implants. MAR2 introduces them, too, but some are less severe. MAR1 and MAR2 also result in blurring, which is most severe in the upper region of the bone around the prosthesis on the right hand side. Only NMAR results in an image where almost no new streaks are introduced and also does not blur the region close to the implants. The bone surrounding the prostheses is clearly visible after NMAR.

对于患者1，即植入了两个植入物的患者，结果如图6所示。未经校正的图像在两个植入物之间存在细条纹伪影和明显的束硬化伪影。MAR1、MAR2和NMAR均消除了这些伪影。然而，MAR1引入了与植入物相切的虚假条纹。MAR2也引入了虚假条纹，但有些不太严重。MAR1和MAR2还会导致模糊，在右侧假体周围骨骼的上部区域最为严重。只有NMAR能够生成几乎没有引入新条纹且不会模糊植入物附近区域的图像。NMAR处理后，假体周围的骨骼清晰可见。

IV.B.2. Patient 2

IV.B.2. 患者 2

The images of patient 2, a patient with a hip prosthesis, presented in Figs. 7–9, exhibit much stronger artifacts. All three MAR methods clearly lead to better image quality in the whole volume. Slices in which the metal consists of a single object with a round cross section, as shown in Fig. 7, are the ideal case for interpolation-based MAR. Still, there are improvements of MAR2 and NMAR compared to MAR1. Correction with MAR2 and NMAR leads to a more homogeneous result and less artifacts tangent to the prosthesis. After correction with MAR2, however, some dark artifacts close to the bone structures are visible. They are the consequence of too low sinogram values in the metal trace, as MAR2 does not account for the higher attenuation of the bone tissue. In Fig. 8, the described effects are more pronounced, as the cross section of the metal is greater.

图示了患者2（一位接受了髋关节置换术的患者）的影像，其在图7-9中呈现出更强的伪影。所有三种金属伪影去除（MAR）方法均显著提高了整个容积的图像质量。金属由具有圆形横截面的单个物体组成的切片（如图7所示）是基于插值的金属伪影去除（MAR）的理想情况。尽管如此，与MAR1相比，MAR2和NMAR仍有改进。使用MAR2和NMAR进行的校正可获得更均匀的结果，并减少与假体相切的伪影。然而，使用MAR2校正后，骨骼结构附近会出现一些黑暗伪影。这是由于金属轨迹中的投影图值过低所致，因为MAR2未考虑骨组织的更高衰减。在图8中，由于金属的横截面更大，所述效应更为明显。

The results for a slice intersecting the very end of the ﬁxation of the prosthesis are shown in Fig. 9. The artifacts in the uncorrected image are very mild. However, if the whole volume is corrected, this slice is corrected as well. The correction results for MAR1 and MAR2 are worse than the uncorrected version; the ﬁne bone structures close to the ﬁxation are blurred. In the NMAR corrected image, blurring and streak artifacts are no longer visible.

图9展示了与假体固定端部相交的切片的测量结果。未校正图像中的伪影非常轻微。然而，如果对整个体积进行校正，该切片也会被校正。MAR1和MAR2的校正结果比未校正版本更差；固定端附近的精细骨骼结构变得模糊。在NMAR校正图像中，模糊和条状伪影不再可见。

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/7/figures/fig.5.7.jpg?ver=1)

FIG. 5. Comparison for the hip phantom and the thorax phantom. The arrows in the uncorrected images mark the position of the metal implants. In the corrected images, the solid arrows highlight the position of artifacts that are introduced by a correction method. Outlined arrows mark the same posi tion in an image which does not show an artifact there, and thus imply that the used correction method is superior. The original streak artifacts are successfully corrected by each method. However, MAR1 and MAR2 introduce new artifacts. Images exhibit considerably less artifacts after performing NMAR and the simulations show that even ﬁne bone structures can be preserved共C=0 HU/W=500 HU兲.

图 5. 髋部模型和胸部模型的对比。未校正图像中的箭头标记了金属植入物的位置。在校正后的图像中，实心箭头突出了校正方法引入的伪影的位置。轮廓箭头标记了图像中相同的位置，但该位置没有伪影，因此表明所使用的校正方法更优越。原始的条纹伪影被每种方法成功校正。然而，MAR1和MAR2引入了新的伪影。执行NMAR后，图像显示的伪影明显减少，并且模拟显示即使是精细的骨骼结构也能被保留共C=0 HU/W=500 HU兲。

坚持阅读，收获满满！免费翻译额度剩余约20%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/7/figures/fig.6.7.jpg?ver=1)

FIG. 6. Patient 1 with bilateral hip endoprostheses. Arrows in analogy to Fig. 5. MAR1 and MAR2 result in blurring of bone and introduce streak artifacts. New streak artifacts are slightly reduced with MAR2 compared to MAR1. NMAR results in an image with almost no new streaks. The magniﬁcation at the bottom row shows that the bone surrounding the right hand side of the prosthesis is clearly visible only after NMAR. Top row: 共C=0 HU/W=500 HU兲. Middle and bottom row:共C=500 HU/W=1500 HU兲.

图 6. 患者 1 接受双侧髋关节假体植入术。箭头指示与图 5 类似。MAR1 和 MAR2 导致骨骼模糊并引入条纹伪影。与 MAR1 相比，MAR2 的新条纹伪影略有减少。NMAR 可生成几乎没有新条纹的图像。底部行的放大图显示，只有在 NMAR 后，右侧假体周围的骨骼才清晰可见。顶行：共C=0 HU/W=500 HU兲。中间行和底行：共C=500 HU/W=1500 HU兲。

IV.B.3. Patient 3

IV.B.3. 患者 3

Three slices of patient 3, the patient with dental ﬁllings, are presented in Figs. 10–12. Metal artifact reduction in the presence of dental ﬁllings or crowns is especially challenging. There are often multiple metal objects of high density and irregular shape. Also, dental enamel is the densest material that is found naturally in the human body. The absolute error that can be made by interpolation is therefore higher than in other cases.

图10-12展示了患者3（有牙科填充物）的三张切片。在存在牙科填充物或牙冠的情况下，金属伪影的减少尤其具有挑战性。通常存在多个高密度和不规则形状的金属物体。此外，牙釉质是人体中天然存在的最致密材料。因此，通过插值可能产生的绝对误差比其他情况更高。

坚持阅读，收获满满！免费翻译额度剩余约30%

Figure 10 shows a slice through the lower jaw with a ﬁlling in a back tooth. Artifacts obscure the region of the tongue in large parts. The correction with MAR1 and MAR2 removes the strong streak artifacts as well as the excessive beam hardening artifacts. With NMAR, the image is restored even in regions close to the ﬁlling and the newly introduced artifacts are least prominent.

图 10 显示了下颌骨的切片，其中一颗后牙有充填物。伪影在很大程度上遮挡了舌头区域。使用 MAR1 和 MAR2 进行校正可以去除强烈的条纹伪影以及过度的束硬化伪影。使用 NMAR，图像在靠近充填物的区域也能得到恢复，并且新引入的伪影最不明显。

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/8/figures/fig.7.8.jpg?ver=1)

FIG. 7. Patient 2 with unilateral total hip endoprosthesis. Arrows in analogy to Fig. 5. All three MAR methods lead to better image quality. The single prosthesis with its round cross section is an ideal case for interpolation-based MAR. Compared to MAR1, both MAR2 and NMAR lead to a more homogeneous result and less artifacts tangent to the prosthesis. After correction with MAR2, dark artifacts close to bone structures are visible, which are avoided by NMAR. Top and middle row:共C=0 HU/W=750 HU兲. Bottom row:共C=500 HU/W=1500 HU兲.

图 7. 患者 2 的单侧全髋关节假体。箭头指示类比图 5。所有三种 MAR 方法均可提高图像质量。具有圆形横截面的单个假体是基于插值法的 MAR 的理想情况。与 MAR1 相比，MAR2 和 NMAR 均可获得更均匀的结果，并减少假体切线方向的伪影。使用 MAR2 校正后，可见骨骼结构附近的暗伪影，NMAR 可避免这些伪影。顶行和中间行：共C=0 HU/W=750 HU兲。底行：共C=500 HU/W=1500 HU兲。

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/8/figures/fig.8.8.jpg?ver=1)

FIG. 8. Patient 2 with unilateral total hip endoprosthesis—shown is a slice with a greater metal cross section than in Fig. 7. Arrows in analogy to Fig. 5. Correction with MAR2 and NMAR leads to a more homogeneous result and less artifacts tangent to the prosthesis. As in Fig. 7, after correction with MAR2, dark artifacts close to bone structures are visible, which are avoided with NMAR. Top and middle row:共C=0 HU/W=750 HU兲. Bottom row:共C =500 HU/W=1500 HU兲.

图 8. 患者 2 的单侧全髋关节假体—显示了一个金属横截面大于图 7 的切片。箭头指示类似于图 5。使用 MAR2 和 NMAR 进行校正可获得更均匀的结果，并减少假体切线方向的伪影。与图 7 相同，使用 MAR2 校正后，骨骼结构附近可见暗伪影，而 NMAR 可避免这些伪影。顶行和中行：共C=0 HU/W=750 HU兲。底行：共C =500 HU/W=1500 HU兲。

The slice presented in Fig. 11 can be almost regarded as a worst case scenario: Multiple dental ﬁllings on both sides of

图 11 所示的切片几乎可以看作是最坏情况的场景：两侧均有多个牙科填充物

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/9/figures/fig.9.9.jpg?ver=1)

FIG. 9. Patient 2 with unilateral total hip endoprosthesis. Arrows in analogy to Fig. 5. The presented slice intersects the end of the ﬁxation of the prosthesis. The artifacts in the uncorrected image are very mild. In the correction results for MAR1 and MAR2, the ﬁne bone structures close to the ﬁxation are blurred. In the NMAR corrected image, no blurring and no streak artifacts are visible. Top and middle row:共C=0 HU/W=750 HU兲. Bottom row:共C =500 HU/W=1500 HU兲.

图 9. 患者 2 接受单侧全髋关节假体植入术。箭头指示同图 5。所显示的切片与假体固定端相交。未校正图像中的伪影非常轻微。在 MAR1 和 MAR2 的校正结果中，固定件附近的精细骨骼结构变得模糊。在 NMAR 校正图像中，未见模糊或条状伪影。顶行和中行：共C=0 HU/W=750 HU兲。底行：共C =500 HU/W=1500 HU兲。

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/9/figures/fig.10.9.jpg?ver=1)

FIG. 10. Patient 3, slice through a dental ﬁlling in a molar in the lower jaw. Arrows in analogy to Fig. 5. In the uncorrected image, artifacts obscure large parts of the region of the tongue. The correction with MAR1 and MAR2 removes the strong streak artifacts as well as the excessive beam hardening artifacts, but some new streak artifacts and blurring are introduced. With NMAR, the image is restored even in regions close to the ﬁlling. Top and middle row:共C =100 HU/W=750 HU兲. Bottom row:共C=1000 HU/W=4000 HU兲.

图 10. 患者 3，穿过下颌牙齿填充物的切片。箭头类比图 5。在未校正的图像中，伪影遮挡了舌部的大部分区域。使用 MAR1 和 MAR2 进行校正可去除强烈的条状伪影以及过度的束硬化伪影，但引入了一些新的条状伪影和模糊。使用 NMAR，即使在靠近填充物的区域，图像也得到了恢复。顶行和中行：共C =100 HU/W=750 HU兲。底行：共C=1000 HU/W=4000 HU兲。

坚持阅读，收获满满！免费翻译额度剩余约20%

the jaw. In the narrow window, anatomical features are hardly visible in the anterior part. Again, metal artifacts can be removed with MAR1 and MAR2 to some extent, but at the cost of new and severe interpolation artifacts. Unfortunately, even with NMAR, some artifacts remain. However, the result is better than with MAR1 and MAR2, which impair the image quality in large parts of the slice.

下颌骨。在狭窄的窗口中，解剖学特征在前部几乎不可见。同样，金属伪影可以在一定程度上通过MAR1和MAR2去除，但代价是引入新的且严重的插值伪影。不幸的是，即使使用NMAR，一些伪影仍然存在。然而，结果优于MAR1和MAR2，后两者会损害切片大部分区域的图像质量。

坚持阅读，收获满满！免费翻译额度剩余约20%

In the third slice, which is shown in Fig. 12, the lower end of a dental ﬁlling is intersected, which has only a small cross section. Fine streak artifacts are visible mostly in the posterior part. They can be removed with MAR1, MAR2, and NMAR, with MAR1 and MAR2 introducing new artifacts, mainly in the region of the teeth, whereas the result obtained with NMAR is free of artifacts.

在第三个切片（图12所示）中，可以看到一个牙科填充物的下端被截断，该填充物仅具有很小的横截面。精细条纹伪影主要出现在后部。可以使用MAR1、MAR2和NMAR去除这些伪影，其中MAR1和MAR2会引入新的伪影，主要出现在牙齿区域，而使用NMAR获得的结果则没有伪影。

IV.B.4. Patient 4

IV.B.4. 患者 4

Results for patient 4 are shown in Fig. 13. The patient’s spine is ﬁxed with a Harrington rod. The metal rod has a relatively small cross section and causes ﬁne streak artifacts and moderate beam hardening artifacts. MAR1 and MAR2 even impair the image quality. The right hand side transverse process of the vertebra is blurred and dark artifacts between bones appear after the correction with MAR1 or MAR2. NMAR corrects the metal artifacts while perfectly preserving the bone structures.

患者4的结果如图13所示。患者的脊柱用Harrington棒固定。金属棒的横截面相对较小，会引起细条伪影和中度束硬化伪影。MAR1和MAR2甚至会损害图像质量。使用MAR1或MAR2校正后，椎骨的右侧横突模糊，骨骼之间出现暗伪影。NMAR在完美保留骨骼结构的同时校正了金属伪影。

坚持阅读，收获满满！免费翻译额度剩余约30%

From this example, as well as from the results presented in Fig. 9 and 12, an important advantage of NMAR is found: Images from slices with only small metal implants, which only suffer from less severe artifacts, are not made worse than the uncorrected images. NMAR preserves all structures, as it uses the prior image, which is very accurate in these cases.

从该示例以及图9和12中展示的结果来看，NMAR的一个重要优势在于：即使是仅有少量金属植入物、伪影不严重的切片图像，经过NMAR校正后也不会比校正前的图像效果更差。NMAR保留了所有结构，因为它使用了先验图像，而先验图像在这些情况下非常准确。

坚持阅读，收获满满！免费翻译额度剩余约20%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/10/figures/fig.11.10.jpg?ver=1)

FIG. 11. Patient 3, with multiple dental ﬁllings on both sides of the jaw. Arrows in analogy to Fig. 5. In the uncorrected image in the top row, anatomical features are hardly visible in the anterior part. Some artifacts can be removed with MAR1 and MAR2, but at the cost of new artifacts. Even with NMAR some artifacts remain in this worst case scenario. The remaining artifacts are much less strong compared to the artifacts introduced with MAR1 and MAR2, which impair large parts of the slice. The middle row shows a part of a reconstruction with a ﬁeld of view of 100 cm. Top row and middle row:共C =100 HU/W=750 HU兲. Bottom row:共C=1000 HU/W=4000 HU兲.

图 11. 患者 3，颌骨两侧有多处牙齿填充物。箭头指示同图 5。在顶部行未校正的图像中，解剖结构在前方区域几乎不可见。使用 MAR1 和 MAR2 可以去除一些伪影，但会产生新的伪影。即使使用 NMAR，在这种最坏的情况下仍然存在一些伪影。与 MAR1 和 MAR2 引入的伪影相比，剩余的伪影强度要小得多，后者会影响切片的很大一部分。中间行显示了视场为 100 厘米的重建的一部分。顶部行和中间行：共C =100 HU/W=750 HU兲。底部行：共C=1000 HU/W=4000 HU兲。

V. DISCUSSION

V. 讨论

NMAR has shown to deliver promising results for different types of metal implants. However, the evaluation of the results for patient data in this work is of course subjective. By visual inspection, NMAR outperforms both other methods. A quantitative assessment is problematic, as no ground truth is available for the patient data and results with phantoms are not fully transferable. To fully prove the effectiveness of this algorithm, a clinical study involving more cases and the systematic evaluation by trained radiologists is planned.

NMAR已显示出为不同类型的金属植入物提供有希望的结果。然而，本工作中对患者数据结果的评估当然是主观的。通过目视检查，NMAR优于其他两种方法。定量评估存在问题，因为患者数据没有真实情况，并且使用模体的结果不能完全转移。为充分证明该算法的有效性，计划进行一项涉及更多病例的临床研究，并由训练有素的放射科医生进行系统评估。

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/11/figures/fig.12.11.jpg?ver=1)

FIG. 12. Patient 3, slice through the lower end of a dental ﬁlling, which has only a small cross section. Arrows in analogy to Fig. 5. Fine streak artifacts are visible mostly in the posterior part. MAR1 and MAR2 introduce artifacts in the same order of magnitude as those which are removed. NMAR removes the artifacts and preserve all structures. Top and middle row:共C=100 HU/W=750 HU兲. Bottom row:共C=1000 HU/W=4000 HU兲.

图 12. 患者 3，穿过牙科填充物下端的切片，该填充物仅具有很小的横截面。箭头类比于图 5。细条状伪影主要在后部可见。MAR1 和 MAR2 引入的伪影幅度与去除的伪影幅度相同。NMAR 去除了伪影并保留了所有结构。顶行和中行：共C=100 HU/W=750 HU兲。底行：共C=1000 HU/W=4000 HU兲。

Finding a good prior image is an essential point of this algorithm. Faulty segmentation results can lead to residual artifacts, as seen in Fig. 11. A more advanced segmentation algorithm would surely enhance the results compared to simple thresholding, but this is out of the scope of this work. Patient 3 demonstrates the limitations of the proposed algorithm. If the prior image contains segmentation errors even after precorrection, residual artifacts are unavoidable. This is likely if there are too many or too big metal implants, and especially if those implants are close to bone. In this case, as seen in Fig. 11, the remaining artifacts are found in the NMAR result. Parts of the dark beam hardening artifacts were mistakenly segmented as air and some bright parts as bone. These wrong values were segmented from the MAR1 corrected image and the correction result therefore cannot be worse than this image. On the other hand, only artifacts in the MAR1 image that are severe enough to fall in a wrong tissue class will have a negative effect. Still, some streaks and blurring can be removed and the result is clearly better than the MAR1 result.

寻找一个好的先验图像是该算法的一个关键点。错误的分割结果可能导致残留伪影，如图11所示。更高级的分割算法无疑会比简单的阈值分割增强结果，但这超出了本工作的范围。患者3证明了所提出算法的局限性。如果先验图像即使在预处理后仍包含分割错误，则残留伪影是不可避免的。如果存在过多或过大的金属植入物，特别是当这些植入物靠近骨骼时，这种情况很可能发生。在这种情况下，如图11所示，在NMAR结果中发现了剩余的伪影。部分暗的束硬化伪影被错误地分割为空气，一些亮的区域被错误地分割为骨骼。这些错误值是从MAR1校正图像分割出来的，因此校正结果不会比该图像更差。另一方面，只有足够严重以至于落入错误组织类别的MAR1图像中的伪影才会产生负面影响。尽管如此，一些条纹和模糊可以被去除，结果明显优于MAR1结果。

VI. CONCLUSION

六. 结论

Applying NMAR to simulation as well as clinical data yields excellent results. Even for high metal artifact content and close to metal implants, NMAR reduces artifacts in large part. In regions further away from metal implants, almost no artifacts remain after a correction with NMAR. While MAR2 performs better than MAR1 in some cases, NMAR performs better than MAR1 and MAR2 in all the cases that were considered in this work. For images with very small metal implants and few artifacts MAR1 and MAR2 can even reduce image quality, while NMAR delivers almost artifact-free results in these situations.

将NMAR应用于模拟数据和临床数据均可获得优异的结果。即使在金属伪影含量高且靠近植入物的情况下，NMAR也能在很大程度上减少伪影。在距离金属植入物较远的区域，经过NMAR校正后几乎没有伪影残留。虽然MAR2在某些情况下优于MAR1，但在本研究考虑的所有情况下，NMAR均优于MAR1和MAR2。对于具有非常小的金属植入物和少量伪影的图像，MAR1和MAR2甚至会降低图像质量，而在这些情况下NMAR可提供几乎无伪影的结果。

坚持阅读，收获满满！免费翻译额度剩余约30%

![](https://pdf2html.com/files/server/afedca863b0b063c99db0f8b3d1ffa63.pdf/12/figures/fig.13.12.jpg?ver=1)

FIG. 13. Shown is patient 4 with a Harrington rod for spinal ﬁxation. Arrows in analogy to Fig. 5. In the image, the rod is located below the vertebra. Fine streak artifacts and moderate beam hardening artifacts emerge from there. This patient with few metal and medium metal artifacts is an example where MAR1 and MAR2 even impair the image quality. The transverse process on the right hand side of the vertebra is blurred and dark artifacts between bones appear after correction with MAR1 or MAR2. NMAR corrects the metal artifacts while preserving the bone structures. Top and middle row:共C=0 HU/W=1000 HU兲. Bottom row:共C=500 HU/W=1500 HU兲.

图 13. 展示了接受脊柱固定术的 4 号患者。箭头指示类似于图 5。图像中，金属棒位于椎骨下方。由此产生细条状伪影和中度束硬化伪影。该患者金属伪影少且中等，是 MAR1 和 MAR2 甚至会损害图像质量的一个例子。椎骨右侧的横突模糊，使用 MAR1 或 MAR2 校正后，骨骼之间出现暗伪影。NMAR 在保留骨骼结构的同时校正了金属伪影。顶行和中行：共C=0 HU/W=1000 HU兲。底行：共C=500 HU/W=1500 HU兲。

坚持阅读，收获满满！免费翻译额度剩余约20%

VII. SUMMARY

VII. 总结

Sinogram interpolation-based methods are the most common type of MAR methods, but they often introduce new artifacts because the full information from the metal shadow cannot be recovered. These artifacts are especially severe when high-contrast structures, for example, teeth, are present. To overcome this drawback, a generalized sinogram normalization technique is introduced and evaluated in this work. NMAR is designed to efﬁciently reduce metal artifacts and to prevent the introduction of new artifacts. The normalization is based on the 3D forward projection of a prior image, which is obtained by a multithreshold segmentation. The prior image models air, soft tissue, and bone regions. The normalized projections are subject to an interpolation-based MAR operation. In this work, NMAR is used with linear interpolation. Any interpolation scheme that is suitable for MAR could be chosen, but we did not ﬁnd additional advantages of using more complex interpolation schemes for NMAR. The corrected sinogram is obtained by denormalization of the interpolated, normalized sinogram.

基于塞诺图插值的方法是最常见的金属伪影抑制（MAR）方法类型，但由于无法完全恢复金属阴影的全部信息，它们常常引入新的伪影。当存在高对比度结构（例如牙齿）时，这些伪影尤其严重。为了克服这一缺点，本研究介绍并评估了一种广义塞诺图归一化技术。NMAR旨在有效减少金属伪影并防止引入新的伪影。归一化基于先验图像的3D前向投影，该先验图像通过多阈值分割获得。先验图像模拟了空气、软组织和骨骼区域。归一化后的投影经过基于插值的MAR操作。在本工作中，NMAR与线性插值一起使用。可以选择任何适合MAR的插值方案，但我们没有发现使用更复杂的插值方案对NMAR有额外的好处。校正后的塞诺图是通过对插值后的、归一化后的塞诺图进行反归一化得到的。

Results from four patients, with hip endoprostheses, dental ﬁllings, and spine ﬁxation are presented in this work. Three were scanned with a Somatom Deﬁnition Flash scanner at pitch values ranging from 0.9 to 3.2, one was scanned on a Somatom Sensation 16 scanner at pitch 1. NMAR reliably reduces metal artifacts in images reconstructed from simulated as well as from clinical data. Image quality, in general, is increased compared to MAR using linear interpolation and MAR with a simple length normalization. Details, especially close to metal objects and bones, are much better preserved. Compared to iterative methods, the presented method is computationally inexpensive and can be used as an additional step in conventional sinogram interpolation-based MAR methods. Even for patients with dental ﬁllings, satisfactory results are obtained with the presented method, which is important as those patients with dental ﬁllings make up the major part of patients with metal inside their body, and the artifacts are especially severe here.

本文展示了四例患有髋关节假体、牙科填充物和脊柱固定术的患者的治疗结果。三名患者使用 Somatom Definition Flash 扫描仪以 0.9 至 3.2 的螺距值进行扫描，一名患者使用 Somatom Sensation 16 扫描仪以 1 的螺距进行扫描。NMAR 可可靠地减少从模拟数据和临床数据重建的图像中的金属伪影。与使用线性插值的 MAR 和简单的长度归一化 MAR 相比，图像质量总体上有所提高。细节，尤其是在靠近金属物体和骨骼的细节，得到了更好的保留。与迭代方法相比，所提出的方法计算成本低廉，并且可以作为常规基于正弦图插值的 MAR 方法的附加步骤。即使对于有牙科填充物的患者，所提出的方法也能获得满意的结果，这一点很重要，因为有牙科填充物的患者占体内有金属的患者的大部分，而且这里的伪影尤其严重。

坚持阅读，收获满满！免费翻译额度剩余约20%

Pure interpolation methods, as MAR1, disregard the information from the metal trace completely and lead to blurring close to metal implants. NMAR also completely replaces the metal trace, but by using the projections of the prior image, which contain information from the whole image, some of the information from the metal trace is used indirectly. MAR1 and MAR2 introduce some new artifacts in all the cases considered in this work. NMAR reduces artifacts even close to metal implants. In the case of mild to moderate artifacts, NMAR does not suffer from the loss of information close to implants. In these cases, almost no artifacts remain after a correction with NMAR in regions further away from metal implants. A clinical study involving more cases is planned to fully prove the effectiveness of the algorithm.

纯粹的插值方法，如MAR1，完全忽略了金属伪影的信息，导致金属植入物附近的图像模糊。NMAR也完全替换了金属伪影，但通过使用包含整个图像信息的先验图像的投影，间接利用了部分金属伪影的信息。MAR1和MAR2在本次工作中考虑的所有情况下都引入了一些新的伪影。NMAR减少了即使在金属植入物附近的伪影。在轻度至中度伪影的情况下，NMAR不会遭受植入物附近信息丢失的问题。在这些情况下，使用NMAR校正后，远离金属植入物的区域几乎没有伪影残留。计划进行一项涉及更多病例的临床研究，以充分证明该算法的有效性。

a兲Author to whom correspondence should be addressed. Electronic mail: esther.meyer@imp.uni-erlangen.de; Telephone: 49共9131兲85 25535; Fax: 49共9131兲85 22824.

1W. Kalender, Computed Tomography: Fundamentals, System Technology, Image Quality, Applications共Publicis, Erlangen, 2005兲.

2G. H. Glover and N. J. Pelc, “An algorithm for the reduction of metal clip artifacts in CT reconstructions,” Med. Phys. 8共6兲, 799–807共1981兲.

3W. A. Kalender, R. Hebel, and J. Ebersberger, “Reduction of CT artifacts caused by metallic implants,” Radiology 164共2兲, 576–577共1987兲.

4A. H. Mahnken, R. Raupach, J. E. Wildberger, B. Jung, N. Heussen, T. G. Flohr, R. W. Günther, and S. Schaller, “A new algorithm for metal artifact reduction in computed tomography: In vitro and in vivo evaluation after total hip replacement,” Invest. Radiol. 38共12兲, 769–775共2003兲.

5J. Wei, L. Chen, G. A. Sandison, Y. Liang, and L. X. Xu, “X-ray CT high-density artifact suppression in the presence of bones,” Phys. Med. Biol. 49共24兲, 5407–5418共2004兲.

6K. Y. Jeong and J. B. Ra, “Reduction of artifacts due to multiple metallic objects in computed tomography,” Medical Imaging 2009: Physics of Medical Imaging, Vol. 7258, p. 72583E, 2009共unpublished兲.

7M. Bal and L. Spies, “Metal artifact reduction in CT using tissue-class modeling and adaptive preﬁltering,” Med. Phys. 33共8兲, 2852–2859 共2006兲.

8D. Prell, Y. Kyriakou, M. Beister, and W. Kalender, “A novel forward projection-based metal artifact reduction method for ﬂat-detector computed tomography,” Phys. Med. Biol. 54共21兲, 6575–6591共2009兲.

9M. Kachelrieß, O. Watzke, and W. A. Kalender, “Generalized multidimensional adaptive ﬁltering共MAF兲for conventional and spiral singleslice, multi-slice and cone-beam CT,” Med. Phys. 28共4兲, 475–490共2001兲.

10M. Bal, H. Celik, K. Subramanyan, K. Eck, and L. Spies, “A radial adaptive ﬁlter for metal artifact reduction,” Proc. SPIE 5747, 2075–2082 共2005兲.

11G. Wang, D. L. Snyder, J. A. O’Sullivan, and M. W. Vannier, “Iterative deblurring for CT metal artifact reduction,” IEEE Trans. Med. Imaging 15共5兲, 657–664共1996兲.

12B. De Man, J. Nuyts, P. Dupont, G. Marchal, and P. Suetens, “An iterative maximum-likelihood polychromatic algorithm for CT,” IEEE Trans. Med. Imaging 20共10兲, 999–1008共2001兲.

13M. Oehler and T. M. Buzug, “Modiﬁed MLEM algorithm for artifact suppression in CT,” IEEE Medical Imaging Conference Record, Vol. M16-1, pp. 3511–3518, 2006共unpublished兲.

14C. Lemmens, D. Faul, and J. Nuyts, “Suppression of metal artifacts in CT using a reconstruction procedure that combines MAP and projection completion,” IEEE Trans. Med. Imaging 28共2兲, 250–260共2009兲.

15O. Watzke and W. A. Kalender, “A pragmatic approach to metal artifact reduction in CT: Merging of metal artifact reduced images,” Eur. J. Radiol. 14共5兲, 849–856共2004兲.

16X. Duan, L. Zhang, J. Xiao, J. Cheng, Z. Chen, and Y. Xing, “Metal artifact reduction in CT images by sinogram TV inpainting,” Nuclear Science Symposium Conference Record, 2008共NSS ‘08兲, pp. 4175–4177 共unpublished兲.

17J. Müller and T. M. Buzug, “Spurious structures created by interpolationbased CT metal artifact reduction,” Proc. SPIE 7258共1兲, 1Y1–1Y8共2009兲.

18M. Oehler and T. M. Buzug, “Statistical image reconstruction for inconsistent CT projection data,” Methods Inf. Med. 3, 261–269共2007兲.

19B. Kratz and T. M. Buzug, “Metal artifact reduction in computed tomography using nonequispaced Fourier transform,” IEEE Medical Imaging Conference Record, pp. 2720–2723, 2009共unpublished兲.

20L. Yu, H. Li, J. Mueller, J. Koﬂer, X. Liu, A. Primak, J. Fletcher, L. Guimaraes, T. Macedo, and C. McCollough, “Metal artifact reduction from reformatted projections for hip prostheses in multislice helical computed tomography: Techniques and initial clinical results,” Invest. Radiol. 44共11兲, 691–696共2009兲.

21W. J. H. Veldkamp, R. M. S. Joemai, A. J. van der Molen, and J. Geleijns, “Development and validation of segmentation and interpolation techniques in sinograms for metal artifact suppression in CT,” Med. Phys. 37共2兲, 620–628共2010兲.

22E. Meyer, F. Bergner, R. Raupach, T. Flohr, and M. Kachelrieß, “Normalized metal artifact reduction共NMAR兲in computed tomography,” Nuclear Science Symposium Conference Record共NSS/MIC兲2009 IEEE, pp. 3251–3255, 2009.

23P. M. Joseph, “An improved algorithm for reprojecting rays through pixel images,” IEEE Trans. Med. Imaging 1共3兲, 192–196共1982兲.

24D. Prell, Y. Kyrikou, T. Struffert, A. Dörﬂer, and W. A. Kalender, “Metal artifact reduction for clipping and coiling in interventional C-arm CT,” AJNR Am. J. Neuroradiol. 31共4兲, 634–639共2010兲.