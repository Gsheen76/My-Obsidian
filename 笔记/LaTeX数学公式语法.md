---
tags:
  - 工具
  - LaTeX
  - 数学
title: LaTeX数学公式语法
type: note
summary: 整理 LaTeX 数学公式的常用语法和可复制示例。
updated: 2026-08-05
migrated: 2026-08-05
---

> [!summary] Summary
> 整理 LaTeX 数学公式的常用语法和可复制示例。

# 一、 行内式与独立式
### 1. 行内式
```text
$ $
```
- **例子：**
```text
$x+y=1$
```
   $x+y=1$

### 2. 独立式
```text
$$ $$
```
- **例子：**
```text
$$x+y=1$$
```
$$x+y=1$$

# 二、上下标

### 1. 上标
```text
e^x
``` 
### 2. 下标
```text
y_1
``` 
$$
x^2+y_1=x^{x_1+y}
$$
$$
x^2+y_1=2
$$

### 3. 括号
- 大括号
```text
\{  \}
```
$$
f(x,y)=x^2+y_2,x \epsilon[1,10],y \epsilon \{1,2,3\}
$$
- 左右大括号(成对使用)
```text
\left(  \right)
\left.(  \right.)   //加.便小括号
```
$$
\left.( {1 \over 2} \right)
$$




# 基础符号
$$ + - = \times \div \pm \mp $$

# 上下标
$x^2$ $x_n$ $x^{2n}$ $x_{ij}$

# 分数
$\frac{1}{2}$ ${1}/{2}$

# 根号
$\sqrt{2}$ $\sqrt[n]{2}$

# 希腊字母

| 符号小写          | LaTeX         |
| ------------- | ------------- |
| $\alpha$      | `\alpha`      |
| $\beta$       | `\beta`       |
| $\gamma$      | `\gamma`      |
| $\delta$      | `\delta`      |
| $\epsilon$    | `\epsilon`    |
| $\varepsilon$ | `\varepsilon` |
| $\theta$      | `\theta`      |
| $\vartheta$   | `\vartheta`   |
| $\lambda$     | `\lambda`     |
| $\mu$         | `\mu`         |
| $\nu$         | `\nu`         |
| $\xi$         | `\xi`         |
| $\pi$         | `\pi`         |
| $\rho$        | `\rho`        |
| $\sigma$      | `\sigma`      |
| $\tau$        | `\tau`        |
| $\phi$        | `\phi`        |
| $\varphi$     | `\varphi`     |
| $\psi$        | `\psi`        |
| $\omega$      | `\omega`      |

| 符号大写      | LaTeX     |
| --------- | --------- |
| $\Gamma$  | `\Gamma`  |
| $\Delta$  | `\Delta`  |
| $\Theta$  | `\Theta`  |
| $\Lambda$ | `\Lambda` |
| $\Xi$     | `\Xi`     |
| $\Pi$     | `\Pi`     |
| $\Sigma$  | `\Sigma`  |
| $\Phi$    | `\Phi`    |
| $\Psi$    | `\Psi`    |
| $\Omega$  | `\Omega`  |

# 求和、积分、极限
$\sum_{i=1}^n$ $\int_a^b$ $\lim_{x \to 0}$

# 括号
$\{ \}$ $[ ]$ $( )$ $\langle \rangle$

# 矩阵
$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$

# 多行公式
$\begin{aligned} x &= 1 \\ y &= 2 \end{aligned}$

## 关键概念

- 工具、LaTeX、数学

## 关联笔记

- [[笔记/知识库/知识库索引]]
