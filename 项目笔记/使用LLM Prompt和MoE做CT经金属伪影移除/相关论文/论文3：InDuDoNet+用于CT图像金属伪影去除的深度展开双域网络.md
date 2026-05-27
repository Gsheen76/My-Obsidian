**InDuDoNet+: A Deep Unfolding Dual Domain Network for Metal Artifact Reduction in CT Images**

# Abstract 摘要

在计算机断层扫描（CT）成像过程中，患者体内的金属植入物经常引起有害伪影，这会严重降低重建CT图像的视觉质量，并对后续的临床诊断产生不利影响。对于金属伪影减少（MAR）任务，目前基于深度学习的方法已经取得了可喜的性能。然而，它们中的大多数都存在两个主要的共同局限性：1）CT物理成像几何约束没有被全面地纳入到深度网络结构中；2）整个框架对于特定的MAR任务来说，可解释性较弱；因此，每个网络模块的作用难以评估。为了缓解这些问题，在本文中，我们构建了一个新颖的深度展开双域网络，称为InDuDoNet+，其中精细地嵌入了CT成像过程。具体而言，我们推导出一个联合空间和Radon域重建模型，并提出了一种仅使用简单算子的优化算法来求解它。通过将所提出的算法中涉及的迭代步骤展开为相应的网络模块，我们可以轻松构建具有清晰可解释性的InDuDoNet+。此外，我们分析了不同组织之间的CT值，并将先验观察结果合并到InDuDoNet+的先验网络中，这显著提高了其泛化性能。在合成数据和临床数据上进行的综合实验证实了所提出的方法的优越性，以及超越当前最先进（SOTA）MAR方法的卓越泛化性能。代码可在[https://github.com/hongwang01/InDuDoNet_plus](https://github.com/hongwang01/InDuDoNet_plus)上获取。

### Keywords 关键词
CT imaging geometry, Metal artifact reduction, Physical interpretability, Generalization ability
CT成像几何，金属伪影减少，物理可解释性，泛化能力