import pandas as pd
import os

base_dir = '../LT01-PRJNA517021'

# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")
cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t")
cluster_name_data = cluster_annotation_data.to_dict(
    'dict').get('Cell_type', {})
print(cluster_name_data)

# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(
    cell_cluster_path, sep=r"\t", usecols=['"seurat_clusters"'])

def cluster_id_to_int(x):
    return int(x.replace('"', ''))

# expression_data 的 Clusters 转换为 cluster_id：cluster_name
def clusters_to_clusters_name(x):
    clusters_name = cluster_name_data.get(x)
    # clusters_name_data = f'{x}:{clusters_name}'
    return clusters_name
# 去除冒号
def gene_replace(x):
    return x.replace('"', '')


cell_cluster_rename_columns_data = {
    # '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(
    columns=cell_cluster_rename_columns_data)
# 将 Clusters 转换成 整数
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(
    cluster_id_to_int)

# 将索引转换成 Cell_ID 列
cell_cluster_data['Cell_ID'] = cell_cluster_data.index
print(cell_cluster_data)

# 读取表达值
expression_path = os.path.join(base_dir, "scRNA_Matrix.txt")
# expression = pd.read_csv(expression_path, sep=r"\t")
expression = pd.read_csv(expression_path, sep=r"\t", chunksize=1)
print(expression)
save_dir = './expression_data_other/'

for i in range(21503):
    try:
        expression_data = expression.get_chunk(1).T
        expression_data = expression_data.reset_index()
        column_name = expression_data.columns.values.tolist()[1]
        save_name = column_name.replace('"', '')
        save_name = os.path.join(save_dir, save_name)
        if not os.path.exists(save_name):
            rename_columns_data = {
                'index': 'Cell_ID',
                column_name: 'value',
            }
            expression_data = expression_data.rename(
                columns=rename_columns_data)
            # 根据 Cell_ID 合并 expression_data 和 cell_cluster_data
            expression_data = pd.merge(
                expression_data, cell_cluster_data, how='left', on='Cell_ID')
            expression_data['Cell_type'] = expression_data['Clusters'].apply(
                clusters_to_clusters_name)
            expression_data['Cell_ID'] = expression_data['Cell_ID'].apply(
                gene_replace)
            print(expression_data)
            expression_data.to_csv(f'{save_name}.csv', index=False)

    except Exception as e:
        print(e)
        continue
