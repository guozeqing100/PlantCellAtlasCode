import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set(style="whitegrid")
# 以下两句防止中文显示为窗格
# plt.rcParams["font.sans-serif"]=["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False
# 导入数据，从excel中
df = pd.read_csv("./AT1G01010.csv")

# 绘制小提琴图
# 设置窗口的大小
f, ax = plt.subplots(figsize=(11, 6), tight_layout=True)
# 设置轴显示的范围
ax.set(ylim=(df["value"].min(), df['value'].max()))
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
# ax.grid(False)
# 去除上下左右的边框（默认该函数会取出右上的边框）
sns.despine(right=True, top=True)
vio = sns.violinplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
vio.set_title('AT1G01010', fontsize= 30)
plt.savefig('violinplot.png')
plt.close()

# 绘制箱型图
# 设置窗口的大小
f, ax = plt.subplots(figsize=(11, 6), tight_layout=True)
# 设置轴显示的范围
ax.set(ylim=(df["value"].min(), df['value'].max()))
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
# 去除上下左右的边框（默认该函数会取出右上的边框）
sns.despine(right=True, top=True)
box = sns.boxplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
box.set_title('AT1G01010', fontsize= 30)
plt.savefig('boxplot.png')
plt.close()
