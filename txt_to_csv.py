import os

import pandas as pd

base_dir = '../LT2_GSE123013'


# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")
# print(cluster_annotation_path)
cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t")
print(cluster_annotation_data.to_dict('dict'))
cluster_name_data = cluster_annotation_data.to_dict(
    'dict').get('Cell_type', {})

# 保存为 Cluster_annotation.csv

cluster_annotation_rename_columns_data = {
    'Cluster': 'Clusters',
    'Cell_type': 'Cluster_Name'
}
print(cluster_annotation_data)
cluster_annotation_data = cluster_annotation_data.rename(columns=cluster_annotation_rename_columns_data)
print(cluster_annotation_data)
cluster_annotation_data.to_csv('./Cluster_annotation.csv', index=False)

# 生成 cluster_markers.csv
cluster_markers_path = os.path.join(base_dir, "clustermarker.txt")

cluster_markers_data = pd.read_csv(cluster_markers_path, sep=r"\t")
rename_columns_data = {
    '"cluster"': 'Cluster ID',
    '"p_val"': 'P val',
    '"avg_log2FC"': 'Log2FC',
    '"pct.1"': 'pct1',
    '"pct.2"': 'pct2',
    '"p_val_adj"': 'p_val_adj',
    '"gene"': 'Gene',
}
cluster_markers_data = cluster_markers_data.rename(columns=rename_columns_data)

# 先把 Cluster ID 这一列转换成 数字


def cluster_id_to_int(x):
    return int(x.replace('"', ''))


cluster_markers_data['Cluster ID'] = cluster_markers_data['Cluster ID'].apply(
    cluster_id_to_int)
# 再生成一列 Cell Type


def cluster_id_to_cluster_name(x):
    return cluster_name_data.get(x, '')


cluster_markers_data['Cell Type'] = cluster_markers_data['Cluster ID'].apply(
    cluster_id_to_cluster_name)
# Gene 这一列去除冒号


def gene_replace(x):
    return x.replace('"', '')


cluster_markers_data['Gene'] = cluster_markers_data['Gene'].apply(
    gene_replace)

cluster_markers_data.to_csv('cluster_markers.csv', index=False)

# 生成 Umap_data
# 读取 Umap_location 数据
umap_location_path = os.path.join(base_dir, "umap_location.txt")
umap_location_data = pd.read_csv(umap_location_path, sep=r"\t")

umap_location_rename_columns_data = {
    '"UMAP_1"': 'UMAP_1',
    '"UMAP_2"': 'UMAP_2',
}
umap_location_data = umap_location_data.rename(
    columns=umap_location_rename_columns_data)

# 将索引转换成 Cell_ID 列
umap_location_data['Cell_ID'] = umap_location_data.index
# print(umap_location_data)

# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t")

cell_cluster_rename_columns_data = {
    '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(
    columns=cell_cluster_rename_columns_data)
# 将 Clusters 转换成 整数
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(
    cluster_id_to_int)

# 去除 Project_ID 的冒号
cell_cluster_data['Project_ID'] = cell_cluster_data['Project_ID'].apply(
    gene_replace)

# 将索引转换成 Cell_ID 列
cell_cluster_data['Cell_ID'] = cell_cluster_data.index
# print(cell_cluster_data)
# 根据 Cell_ID 合并 Umap_location 和 Cell_cluster

umap_data = pd.merge(umap_location_data, cell_cluster_data,
                     how='left', on='Cell_ID')

# umap_data 的 Clusters 转换为 cluster_id：cluster_name

def clusters_to_clusters_name(x):
    clusters_name = cluster_name_data.get(x)
    # clusters_name_data = f'{x}:{clusters_name}'
    return clusters_name

umap_data['Cell_type'] = umap_data['Clusters'].apply(clusters_to_clusters_name)

# 去除 Cell_ID 的冒号

umap_data['Cell_ID'] = umap_data['Cell_ID'].apply(
    gene_replace)

umap_data.to_csv('./umap_data.csv', index=False)
