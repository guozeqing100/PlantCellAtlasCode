import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("./total_mean.csv")
# f, ax = plt.subplots(figsize=(16, 10))

corr = data.corr()
print(corr)
# sns.heatmap(corr, cmap='RdBu', linewidths=0.05, ax=ax)
plt.tight_layout()
g = sns.clustermap(corr,
                   row_cluster=True,  # 行 聚类
                   col_cluster=True,  # 列 聚类
                   cmap='coolwarm',  # 颜色配置
                   figsize=(12, 10),
                   linewidths=0.05,
                   )
g.fig.subplots_adjust(right=0.7)
g.ax_cbar.set_position((0.9, .3, .02, .4))
g.savefig('pearson.png', dpi=100, bbox_inches='tight')
# 设置Axes的标题
# ax.set_title('Correlation between features')
# plt.show()
plt.close()
# f.savefig('pearson.png', dpi=100, bbox_inches='tight')
