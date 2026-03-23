$$
\renewcommand{\arraystretch}{1.1}
\begin{array}{c c c c c c c c c c c}
\hline
\textbf{Config} & \textbf{L} & \textbf{Q} & \textbf{mAP} & \textbf{AP50} & \textbf{AP75} & \textbf{AP}_{\text{small}} & \textbf{AP}_{\text{large}} & \textbf{↓ runtime} & \textbf{Memory} \\
\hline
\text{Baseline}    & 6 & 100 & \mathbf{39.89\%} & \mathbf{59.60\%} & \mathbf{42.20\%} & 19.05\%  & \mathbf{58.63\%} & -        & 21.2\,\text{GB} \\
\text{Balanced}    & 4 & 100 & 39.40\% & 59.35\% & 41.16\% & \mathbf{19.41\%} & 58.56\% & \downarrow 13.3\% & 18.3\,\text{GB} \\
\text{Lite} & 4 & 50  & 37.24\% & 56.29\% & 39.33\% & 16.60\% & 55.17\% & \downarrow 26.7\% & 16.4\,\text{GB} \\
\hline
\end{array}
$$