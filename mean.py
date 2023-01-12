import pandas as pd
import os

base_dir = '../LT13-GSE158761'


# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", usecols=['"seurat_clusters"'])

# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")

cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t")
cluster_name_data = cluster_annotation_data.to_dict(
    'dict').get('Cell_type', {})

cell_cluster_rename_columns_data = {
    # '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
print(cell_cluster_data)

# cell_cluster_data 的 Clusters 转换为 cluster_id：cluster_name
def clusters_to_clusters_name(x):
    x = x.replace('"', '')
    clusters_name = cluster_name_data.get(int(x))
    # clusters_name_data = f'{x}:{clusters_name}'
    return clusters_name

cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(clusters_to_clusters_name)
print(cell_cluster_data)


cluster_list = list(set(cell_cluster_data["Clusters"].values.tolist()))
print(cluster_list)
# 读取表达值
expression_path = os.path.join(base_dir, "scRNA_Matrix.txt")
expression = pd.read_csv(expression_path, sep=r"\t")

expression_data = expression.T

# 根据 Cell_ID 合并 Umap_location 和 Cell_cluster
total_data = pd.merge(expression_data, cell_cluster_data,
                      left_index=True, right_index=True)

print(total_data)

for cluster in cluster_list:


    cluster_data = total_data[total_data["Clusters"] == cluster]
    cluster_data = cluster_data.set_index('Clusters')
    cluster_data = cluster_data.T
    cluster_data['mean'] = cluster_data.mean(axis=1)


    cluster_name = cluster.replace('/', '_')
    save_name = f"./mean_data/{cluster_name}.csv"
    cluster_data['mean'].to_csv(save_name, index=False)
