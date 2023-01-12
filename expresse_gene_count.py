import pandas as pd
import os

base_dir = '../LT13-GSE158761'


# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(
    cell_cluster_path, sep=r"\t", usecols=['"seurat_clusters"'])

# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")

cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t")
cluster_name_data = cluster_annotation_data.to_dict(
    'dict').get('Cell_type', {})


cell_cluster_rename_columns_data = {
    # '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(
    columns=cell_cluster_rename_columns_data)
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
expresse_gene_count_list = []
for cluster in cluster_list:
    cluster_name = cluster.replace('/', '_')
    cluster_path = f"./mean_data/{cluster_name}.csv"

    cluster_data = pd.read_csv(cluster_path)
    cluster_data = cluster_data[cluster_data["mean"] != 0]
    cluster_dict = {
       cluster: cluster_data.shape[0]
    }
    expresse_gene_count_list.append(cluster_dict)
print(expresse_gene_count_list)
