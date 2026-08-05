from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor


OUTPUT = "四篇生成模型组会汇报.pptx"
BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(255, 255, 255)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def box(slide, x, y, w, h, line_width=0.8):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = BLACK
    shape.line.width = Pt(line_width)
    return shape


def line(slide, x1, y1, x2, y2, width=0.8):
    shape = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    shape.line.color.rgb = BLACK
    shape.line.width = Pt(width)
    return shape


def text(slide, x, y, w, h, value, size=16, bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.04):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    paragraph.space_after = Pt(0)
    run = paragraph.add_run()
    run.text = value
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = BLACK
    return shape


def bullets(slide, x, y, w, h, items, size=15, spacing=5):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.04)
    frame.margin_right = Inches(0.04)
    frame.margin_top = Inches(0.02)
    frame.margin_bottom = Inches(0.02)
    for i, item in enumerate(items):
        paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        paragraph.text = "• " + item
        paragraph.font.name = "Microsoft YaHei"
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = BLACK
        paragraph.space_after = Pt(spacing)
    return shape


def footer(slide, number):
    line(slide, 0.62, 7.02, 12.72, 7.02, 0.6)
    text(slide, 0.64, 7.08, 7.5, 0.18, "四篇生成模型论文阅读笔记", 8)
    text(slide, 12.0, 7.08, 0.65, 0.18, f"{number:02d}", 8, align=PP_ALIGN.RIGHT)


def title(slide, section, heading, subheading=None):
    text(slide, 0.64, 0.30, 12.0, 0.22, section, 9, bold=True)
    text(slide, 0.62, 0.62, 12.0, 0.46, heading, 25, bold=True)
    if subheading:
        text(slide, 0.64, 1.15, 11.9, 0.28, subheading, 12)
    line(slide, 0.62, 1.62, 12.72, 1.62, 0.8)


def label_box(slide, x, y, w, h, heading, body, heading_size=14, body_size=13):
    box(slide, x, y, w, h)
    text(slide, x + 0.16, y + 0.14, w - 0.32, 0.28, heading, heading_size, bold=True)
    text(slide, x + 0.16, y + 0.53, w - 0.32, h - 0.65, body, body_size)


def add_numbered_row(slide, y, number, name, body):
    text(slide, 0.90, y, 0.42, 0.32, str(number), 16, bold=True, align=PP_ALIGN.CENTER)
    text(slide, 1.46, y, 2.55, 0.32, name, 16, bold=True)
    text(slide, 4.14, y, 7.95, 0.32, body, 14)
    line(slide, 0.90, y + 0.50, 12.10, y + 0.50, 0.55)


# 1. Cover
slide = prs.slides.add_slide(blank)
text(slide, 0.80, 1.15, 11.8, 0.30, "组会汇报 / PAPER READING", 11, bold=True)
text(slide, 0.80, 1.75, 11.8, 0.70, "四篇生成模型论文阅读汇报", 31, bold=True)
text(slide, 0.82, 2.68, 11.5, 0.38, "从扩散、分数、流匹配到漂移模型", 18)
line(slide, 0.82, 3.55, 12.1, 3.55, 1.0)
text(slide, 0.82, 4.05, 11.3, 0.35, "汇报重点：我是否读懂了四种模型的原理、作用和相互关系", 17, bold=True)
text(slide, 0.82, 4.75, 11.3, 0.32, "形式：白底黑字；只讲机制和判断，不堆公式", 14)
text(slide, 0.82, 6.45, 4.5, 0.22, "多任务成像方向 / 2026.08", 10)

# 2. Main line
slide = prs.slides.add_slide(blank)
title(slide, "01 / 总览", "先给出一条主线", "四篇论文都在解决同一个问题：如何把简单先验分布变成真实数据分布？")
add_numbered_row(slide, 2.08, 1, "DDPM", "把过程离散成很多个小步骤：先加噪，再逐步去噪。")
add_numbered_row(slide, 2.92, 2, "Score-SDE", "把离散步骤提升为连续时间，用分数描述每个时刻的移动方向。")
add_numbered_row(slide, 3.76, 3, "Flow Matching", "预先设计从噪声到数据的路径，直接学习沿路径的速度。")
add_numbered_row(slide, 4.60, 4, "Drifting Models", "把生成时的迭代搬到训练过程，推理时只保留一次前向。")
box(slide, 0.82, 5.65, 11.7, 0.80)
text(slide, 1.05, 5.85, 11.2, 0.38,
     "演进重点不是模型名字变了，而是三件事在变化：路径如何表示、网络学什么、迭代放在哪里。",
     16, bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
footer(slide, 2)

# 3. DDPM
slide = prs.slides.add_slide(blank)
title(slide, "02 / 论文一", "DDPM：把生成拆成很多个小去噪步骤", "论文价值：给出了高质量扩散模型的清晰工程模板，也是后三篇的出发点。")
label_box(slide, 0.78, 1.95, 3.65, 2.05, "要解决的问题", "直接从噪声生成图像很难。论文把它改写成许多次局部去噪，每一步只处理一个小变化。")
label_box(slide, 0.78, 4.22, 3.65, 2.05, "训练方式", "前向加噪过程固定，不需要学习。训练时随机挑一个噪声程度，让网络判断当前样本里加入了什么噪声。")
box(slide, 4.78, 1.95, 7.75, 2.35)
text(slide, 5.05, 2.15, 7.2, 0.25, "生成过程", 15, bold=True)
label_box(slide, 5.08, 2.70, 1.55, 0.90, "第一步", "真实数据", 12, 12)
text(slide, 6.70, 2.94, 0.55, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 7.32, 2.70, 1.55, 0.90, "第二步", "固定加噪", 12, 12)
text(slide, 8.94, 2.94, 0.55, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 9.56, 2.70, 1.55, 0.90, "第三步", "学习反向", 12, 12)
text(slide, 11.18, 2.94, 0.55, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 11.78, 2.70, 0.60, 0.90, "", "图像", 12, 11)
box(slide, 4.78, 4.58, 7.75, 1.69)
text(slide, 5.05, 4.80, 7.2, 0.25, "我读懂的关键", 15, bold=True)
bullets(slide, 5.05, 5.16, 7.15, 0.90, [
    "网络预测噪声，而不是直接预测原图；这种参数化更稳定。",
    "反向方差固定反而更容易训练，简化目标更关注样本质量。",
    "代价是采样必须走完整条反向链，速度较慢。",
], 13, 3)
footer(slide, 3)

# 4. Score-SDE
slide = prs.slides.add_slide(blank)
title(slide, "03 / 论文二", "Score-SDE：把扩散提升到连续时间", "论文价值：统一了多种基于分数的方法，并把采样器从模型中解耦出来。")
label_box(slide, 0.78, 1.95, 3.60, 2.05, "为什么要连续化", "DDPM 的时间步是离散的，采样方式也被写死。连续时间允许用同一个模型搭配不同的数值求解器。")
label_box(slide, 0.78, 4.22, 3.60, 2.05, "网络学什么", "网络学习每个噪声时刻的分数。直观上，它告诉样本应该往数据密度更高的方向移动。")
box(slide, 4.75, 1.95, 7.80, 2.20)
text(slide, 5.03, 2.15, 7.2, 0.25, "统一框架", 15, bold=True)
label_box(slide, 5.06, 2.72, 1.86, 0.86, "输入", "噪声样本", 12, 12)
text(slide, 6.98, 2.94, 0.45, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 7.52, 2.72, 1.86, 0.86, "模型", "分数网络", 12, 12)
text(slide, 9.44, 2.94, 0.45, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 9.98, 2.72, 1.86, 0.86, "选择", "随机或确定性采样", 12, 11)
box(slide, 4.75, 4.42, 7.80, 1.85)
text(slide, 5.03, 4.64, 7.2, 0.25, "我读懂的关键", 15, bold=True)
bullets(slide, 5.03, 5.00, 7.20, 1.02, [
    "DDPM 可以看作连续框架中的一种离散实现。",
    "Predictor-Corrector 适合追求样本质量；概率流 ODE 适合确定性采样和似然计算。",
    "条件分数可以直接接入修复、补全、着色等成像任务。",
], 13, 3)
footer(slide, 4)

# 5. Flow Matching
slide = prs.slides.add_slide(blank)
title(slide, "04 / 论文三", "Flow Matching：直接学习从噪声到数据的速度", "论文价值：不再绕着分数学习，而是直接回归向量场；合理设计路径可以显著减少采样步数。")
label_box(slide, 0.78, 1.95, 3.65, 2.05, "核心改变", "先规定一条从先验到数据的概率路径，再让网络学习每个位置、每个时刻应该朝哪里走。")
label_box(slide, 0.78, 4.22, 3.65, 2.05, "训练为什么可行", "边际路径通常难以直接计算。条件流匹配逐样本构造目标，训练时只需要回归已知的局部速度。")
box(slide, 4.78, 1.95, 7.75, 2.35)
text(slide, 5.05, 2.15, 7.2, 0.25, "路径设计的直观差异", 15, bold=True)
text(slide, 5.10, 2.73, 2.10, 0.25, "普通扩散路径", 13, bold=True)
line(slide, 5.14, 3.42, 7.72, 3.00, 1.0)
line(slide, 7.72, 3.00, 9.15, 3.56, 1.0)
line(slide, 9.15, 3.56, 11.42, 2.66, 1.0)
text(slide, 10.02, 2.30, 1.30, 0.25, "弯曲、可能回退", 12)
text(slide, 5.10, 3.76, 2.10, 0.25, "OT 路径", 13, bold=True)
line(slide, 5.14, 4.06, 11.42, 2.66, 1.8)
text(slide, 9.60, 3.88, 1.90, 0.25, "更直、更容易拟合", 12, bold=True)
box(slide, 4.78, 4.58, 7.75, 1.69)
text(slide, 5.05, 4.80, 7.2, 0.25, "我读懂的关键", 15, bold=True)
bullets(slide, 5.05, 5.16, 7.15, 0.90, [
    "网络输出的是速度方向，采样时只需解一个常微分方程。",
    "OT 路径把轨迹变直，减少网络要拟合的复杂性。",
    "它的优势主要来自路径和训练目标的设计，不只是换一个采样器。",
], 13, 3)
footer(slide, 5)

# 6. Drifting
slide = prs.slides.add_slide(blank)
title(slide, "05 / 论文四", "Drifting Models：把推理迭代搬到训练时", "论文价值：从训练目标上改变生成方式，目标是一次前向完成生成。")
label_box(slide, 0.78, 1.95, 3.65, 2.05, "核心转向", "前三篇在推理时反复更新样本。漂移模型在训练时更新网络参数，使每个先验样本对应的生成结果逐渐靠近数据分布。")
label_box(slide, 0.78, 4.22, 3.65, 2.05, "什么时候停止", "数据样本产生吸引，生成样本产生排斥。两种分布匹配后，漂移场抵消，训练达到平衡。")
box(slide, 4.78, 1.95, 7.75, 2.35)
text(slide, 5.05, 2.15, 7.2, 0.25, "训练和推理的区别", 15, bold=True)
label_box(slide, 5.08, 2.75, 1.95, 0.86, "训练开始", "先验样本", 12, 12)
text(slide, 7.08, 2.98, 0.55, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 7.72, 2.75, 2.05, 0.86, "参数更新", "分布持续漂移", 12, 12)
text(slide, 9.82, 2.98, 0.55, 0.22, "→", 18, bold=True, align=PP_ALIGN.CENTER)
label_box(slide, 10.46, 2.75, 1.70, 0.86, "训练结束", "一次前向", 12, 12)
box(slide, 4.78, 4.58, 7.75, 1.69)
text(slide, 5.05, 4.80, 7.2, 0.25, "我读懂的关键", 15, bold=True)
bullets(slide, 5.05, 5.16, 7.15, 0.90, [
    "反对称漂移是平衡条件的关键；破坏它，分布匹配就失效。",
    "冻结漂移后的目标，才能形成稳定的自监督训练。",
    "特征空间漂移和训练时条件引导，是高维图像质量的工程重点。",
], 13, 3)
footer(slide, 6)

# 7. Comparison
slide = prs.slides.add_slide(blank)
title(slide, "06 / 横向比较", "四个模型的差异，集中在“迭代放在哪里”", "同一条主线下，四篇论文分别优化了表达方式、训练方式和推理成本。")
columns = [0.72, 2.22, 4.52, 7.02, 9.27, 11.15]
widths = [1.35, 2.15, 2.35, 2.10, 1.72, 1.35]
headers = ["模型", "路径表示", "网络学习对象", "推理方式", "主要优势", "主要代价"]
for x, w, h in zip(columns, widths, headers):
    box(slide, x, 2.00, w, 0.52)
    text(slide, x + 0.04, 2.12, w - 0.08, 0.22, h, 11, bold=True, align=PP_ALIGN.CENTER)
rows = [
    ["DDPM", "离散扩散链", "噪声", "多步去噪", "稳定、清晰", "采样慢"],
    ["Score-SDE", "连续 SDE", "分数", "SDE / ODE", "条件控制强", "求解复杂"],
    ["Flow Matching", "概率路径", "速度", "ODE 少步", "路径可设计", "依赖路径"],
    ["Drifting", "训练时演化", "漂移方向", "一次前向", "推理最快", "训练和估计难"],
]
for row_index, row in enumerate(rows):
    y = 2.52 + row_index * 0.80
    for x, w, value in zip(columns, widths, row):
        box(slide, x, y, w, 0.70)
        text(slide, x + 0.06, y + 0.18, w - 0.12, 0.30, value, 11 if len(value) > 8 else 12,
             bold=(x == columns[0]), align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
box(slide, 0.72, 6.00, 11.78, 0.55)
text(slide, 0.95, 6.15, 11.30, 0.22,
     "演进关系：离散去噪 → 连续分数 → 直接速度回归 → 训练时分布演化",
     15, bold=True, align=PP_ALIGN.CENTER)
footer(slide, 7)

# 8. Imaging implications
slide = prs.slides.add_slide(blank)
title(slide, "07 / 多任务成像", "对多任务成像的启示：先看控制需求，再选生成模型", "四种模型不是简单替代关系，而是对应不同的质量、条件控制和推理预算。")
columns = [0.78, 3.18, 6.28, 9.05]
widths = [2.20, 2.85, 2.55, 3.25]
headers = ["成像需求", "优先考虑", "原因", "我会怎么用"]
for x, w, h in zip(columns, widths, headers):
    box(slide, x, 2.00, w, 0.52)
    text(slide, x + 0.04, 2.12, w - 0.08, 0.22, h, 11, bold=True, align=PP_ALIGN.CENTER)
rows = [
    ["多种逆问题 / 条件切换", "Score-SDE", "条件分数机制成熟", "先做统一条件基线"],
    ["希望少步采样", "Flow Matching", "路径可设计、速度直接回归", "把 OT 路径作为加速方向"],
    ["实时或资源受限", "Drifting", "一次前向，推理成本最低", "验证单步质量和稳定性"],
    ["复现和对比基线", "DDPM", "实现清楚、变量最少", "先建立可控基线"],
]
for row_index, row in enumerate(rows):
    y = 2.52 + row_index * 0.78
    for x, w, value in zip(columns, widths, row):
        box(slide, x, y, w, 0.68)
        text(slide, x + 0.06, y + 0.16, w - 0.12, 0.34, value, 11 if len(value) > 10 else 12,
             bold=(x == columns[0]), align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
box(slide, 0.78, 5.95, 11.52, 0.62)
text(slide, 1.02, 6.14, 11.02, 0.24,
     "建议路线：DDPM 建基线，Score-SDE 做条件控制，Flow Matching 做少步加速，Drifting 做单步探索。",
     14, bold=True, align=PP_ALIGN.CENTER)
footer(slide, 8)

# 9. Relationships understood
slide = prs.slides.add_slide(blank)
title(slide, "08 / 我的理解", "四个最容易混淆的关系", "这四点是我判断自己是否真正读懂论文的依据。")
label_box(slide, 0.82, 2.00, 5.68, 1.35, "关系一：DDPM 与 Score-SDE", "DDPM 的噪声预测，本质上提供了同一扰动分布下的分数信息。Score-SDE 把这种关系推广到连续时间。", 14, 13)
label_box(slide, 6.78, 2.00, 5.68, 1.35, "关系二：Score-SDE 与 Flow Matching", "概率流 ODE 描述确定性输运；Flow Matching 进一步把重点放到“选择路径并回归速度”。", 14, 13)
label_box(slide, 0.82, 3.72, 5.68, 1.35, "关系三：Flow Matching 的真正改进", "关键不是简单换采样器，而是把训练目标变成可直接回归的速度，并用更直的路径降低拟合难度。", 14, 13)
label_box(slide, 6.78, 3.72, 5.68, 1.35, "关系四：Drifting 与蒸馏的区别", "Drifting 不依赖多步教师模型做蒸馏，而是从训练目标上让生成分布逐步达到平衡。", 14, 13)
box(slide, 0.82, 5.65, 11.64, 0.72)
text(slide, 1.05, 5.87, 11.18, 0.28, "我对四篇论文的统一理解：先定义“从哪里到哪里”，再决定“用什么局部信息推动分布”。", 15, bold=True, align=PP_ALIGN.CENTER)
footer(slide, 9)

# 10. Conclusion
slide = prs.slides.add_slide(blank)
title(slide, "09 / 结论", "汇报结论", "四篇论文形成了一条清晰的生成建模演进路线。")
box(slide, 0.84, 2.00, 11.62, 0.95)
text(slide, 1.08, 2.27, 11.14, 0.36, "DDPM 学会逐步去噪，Score-SDE 学会连续地判断方向。", 17, bold=True, align=PP_ALIGN.CENTER)
box(slide, 0.84, 3.25, 11.62, 0.95)
text(slide, 1.08, 3.52, 11.14, 0.36, "Flow Matching 学会直接回归速度，Drifting 把迭代从推理搬到训练。", 17, bold=True, align=PP_ALIGN.CENTER)
box(slide, 0.84, 4.50, 11.62, 0.95)
text(slide, 1.08, 4.77, 11.14, 0.36, "对多任务成像，模型选择取决于条件控制、图像质量和推理预算。", 17, bold=True, align=PP_ALIGN.CENTER)
text(slide, 0.84, 6.30, 11.62, 0.30, "谢谢，欢迎提问。", 15, align=PP_ALIGN.CENTER)
footer(slide, 10)

prs.save(OUTPUT)
print(OUTPUT)
