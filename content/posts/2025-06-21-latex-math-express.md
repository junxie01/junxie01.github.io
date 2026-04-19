---
title: $\LaTeX$的数学公式表达
tags:
  - LaTeX
categories:
  - web
abbrlink: d78cae06
date: 2025-06-21 15:03:50
---
&emsp;&emsp;$\LaTeX$和markdown的数学算符几乎是一样的，那怎么编辑呢？
<!--less-->

> **说明**：公式需包裹在 `$...$`（行内公式）或 `$$...$$`（块级公式）中，以下表格中的 **渲染效果** 需在支持 LaTeX 的 Markdown 环境中显示（如 Typora、Obsidian 等）。

---

## 一、基础运算符号
| 符号名称       | $\LaTeX$ 命令      | 渲染效果         |
|----------------|----------------|------------------|
| 加号           | `a + b`        | $a + b$          |
| 减号           | `a - b`        | $a - b$          |
| 乘号（叉乘）   | `a \times b`   | $a \times b$     |
| 乘号（点乘）   | `a \cdot b`    | $a \cdot b$      |
| 除号           | `a \div b`     | $a \div b$       |
| 加减号         | `a \pm b`      | $a \pm b$        |
| 减加号         | `a \mp b`      | $a \mp b$        |

---

## 二、关系运算符
| 符号名称       | $\LaTeX$ 命令      | 渲染效果         |
|----------------|----------------|------------------|
| 等于           | `a = b`        | $a = b$          |
| 不等于         | `a \neq b`     | $a \neq b$       |
| 约等于         | `a \approx b`  | $a \approx b$    |
| 大于等于       | `a \geq b`     | $a \geq b$       |
| 小于等于       | `a \leq b`     | $a \leq b$       |
| 远大于         | `a \gg b`      | $a \gg b$        |
| 远小于         | `a \ll b`      | $a \ll b$        |
| 正比于         | `a \propto b`  | $a \propto b$    |

---

## 三、集合运算符
| 符号名称       | $\LaTeX$ 命令          | 渲染效果             |
|----------------|--------------------|----------------------|
| 并集           | `A \cup B`         | $A \cup B$          |
| 交集           | `A \cap B`         | $A \cap B$          |
| 属于           | `x \in A`          | $x \in A$           |
| 不属于         | `x \notin B`       | $x \notin B$        |
| 子集           | `A \subset B`      | $A \subset B$       |
| 真子集         | `A \subseteq B`    | $A \subseteq B$     |
| 空集           | `\emptyset`        | $\emptyset$         |
| 实数集         | `\mathbb{R}`       | $\mathbb{R}$        |
| 自然数集       | `\mathbb{N}`       | $\mathbb{N}$        |

---

## 四、微积分符号
| 符号名称         | $\LaTeX$ 命令                 | 渲染效果                  |
|------------------|---------------------------|---------------------------|
| 积分             | `\int_{a}^{b} f(x) dx`    | $\int_{a}^{b} f(x) dx$    |
| 偏导数           | `\frac{\partial f}{\partial x}` | $\frac{\partial f}{\partial x}$ |
| 极限             | `\lim_{x \to 0} \frac{\sin x}{x}` | $\lim_{x \to 0} \frac{\sin x}{x}$ |
| 求和             | `\sum_{i=1}^{n} i^2`      | $\sum_{i=1}^{n} i^2$      |
| 导数（撇号形式） | `f'(x)`                   | $f'(x)$                   |
| 梯度             | `\nabla f`                | $\nabla f$                |
| 二阶导数         | `\frac{d^2 y}{dx^2}`      | $\frac{d^2 y}{dx^2}$      |

---

## 五、希腊字母
| 小写字母 | $\LaTeX$ 命令 | 渲染效果 | 大写字母 | LaTeX 命令 | 渲染效果 |
|----------|------------|----------|----------|------------|----------|
| α (alpha) | `\alpha`   | $\alpha$ | Γ (Gamma) | `\Gamma`   | $\Gamma$ |
| β (beta)  | `\beta`    | $\beta$  | Δ (Delta) | `\Delta`   | $\Delta$ |
| θ (theta) | `\theta`   | $\theta$ | Θ (Theta) | `\Theta`   | $\Theta$ |
| π (pi)    | `\pi`      | $\pi$    | Π (Pi)    | `\Pi`      | $\Pi$    |
| σ (sigma) | `\sigma`   | $\sigma$ | Σ (Sigma) | `\Sigma`   | $\Sigma$ |

---

## 六、箭头符号
| 符号名称   | $\LaTeX$ 命令         | 渲染效果            |
|------------|-------------------|---------------------|
| 右箭头     | `\rightarrow`    | $\rightarrow$       |
| 左箭头     | `\leftarrow`     | $\leftarrow$        |
| 双向箭头   | `\leftrightarrow`| $\leftrightarrow$   |
| 蕴含符号   | `\Rightarrow`    | $\Rightarrow$       |
| 等价符号   | `\Leftrightarrow`| $\Leftrightarrow$   |
| 映射箭头   | `\mapsto`        | $\mapsto$           |

---

## 七、括号与定界符
| 符号名称       | $\LaTeX$ 命令                     | 渲染效果                     |
|----------------|--------------------------------|------------------------------|
| 圆括号（自适应）| `\left( \frac{a}{b} \right)`   | $\left( \frac{a}{b} \right)$  |
| 方括号         | `\left[ x \right]`             | $\left[ x \right]$            |
| 花括号         | `\left\{ x \right\}`           | $\{ x \}$          |
| 绝对值         | `\lvert x \rvert`              | $\lvert x \rvert$             |
| 范数           | `\lVert \mathbf{v} \rVert`     | $\lVert \mathbf{v} \rVert$    |

---

## 八、矩阵环境
```latex
$$ 
\begin{pmatrix}  % 圆括号矩阵
a & b \\
c & d 
\end{pmatrix}
\quad
\begin{bmatrix}  % 方括号矩阵
a & b \\
c & d 
\end{bmatrix}
\quad
\begin{vmatrix}  % 行列式
a & b \\
c & d 
\end{vmatrix}
$$
```
渲染效果：
$$ 
\begin{pmatrix}  % 圆括号矩阵
a & b \\
c & d 
\end{pmatrix}
\quad
\begin{bmatrix}  % 方括号矩阵
a & b \\
c & d 
\end{bmatrix}
\quad
\begin{vmatrix}  % 行列式
a & b \\
c & d 
\end{vmatrix}
$$

看样子花括号和矩阵都不太行啊。
