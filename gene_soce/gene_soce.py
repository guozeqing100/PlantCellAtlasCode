from collections import Counter

import pandas as pd

# ClusterMarker_stats 数据
ClusterMarker_stats_file_name = './gene_soce/ClusterMarker_stats.xlsx'
ClusterMarker_stats_data = pd.read_excel(ClusterMarker_stats_file_name)

# RootTip_data 数据
RootTip_file_name = './gene_soce/RootTip.xlsx'
RootTip_data = pd.read_excel(RootTip_file_name)

def gene_soce(x):

    gene_id = x['Gene_ID']
    cell_type = x['Cell_type']
    soce = 1

    gene_id_data = ClusterMarker_stats_data[ClusterMarker_stats_data['Gene_ID'] == gene_id]
    gene_id_count = dict(Counter(gene_id_data['Cell_type'].to_list()))
    # 判断字典长度
    if len(gene_id_count) == 1: 
        soce = gene_id_count.get(cell_type)
    else:
        cell_type_count = gene_id_count.get(cell_type)
        cell_type_other_list = list(gene_id_count.keys())
        cell_type_other_list.remove(cell_type)
        # AT4G32880
        # RootTip_data 中 Cell Type 的 Parent 个数
        cell_type_parent_list = RootTip_data[RootTip_data['Cell Type'] == cell_type]['Parent'].to_list()
        parent_cell_type_list = RootTip_data[RootTip_data['Parent'] == cell_type]['Cell Type'].to_list()
        cell_type_parent_list.extend(parent_cell_type_list)
        cell_type_other_count = 0
        for cell_type_other in cell_type_other_list:
            if cell_type_other in cell_type_parent_list:
                cell_type_count = cell_type_count + gene_id_count.get(cell_type_other)
            else:
                cell_type_other_count = cell_type_other_count + gene_id_count.get(cell_type_other)

        last_count = cell_type_count - cell_type_other_count
        if last_count < 0:
            last_count = 0
        soce = last_count
    return soce

ClusterMarker_stats_data['Score'] = ClusterMarker_stats_data.apply(gene_soce, axis=1)
# ClusterMarker_stats_data.to_csv('ClusterMarker_stats.csv', index=False)

print(ClusterMarker_stats_data)

def lit_id(x):
    gene_id = x['Gene_ID']
    cell_type = x['Cell_type']
    score = x['Score']

    if score > 1:
        gene_id_data = ClusterMarker_stats_data[(ClusterMarker_stats_data['Gene_ID'] == gene_id) & (ClusterMarker_stats_data['Cell_type'] == cell_type)]
        lit_id_list = list(set(gene_id_data['Lit_ID'].to_list()))
        lit_id_str = ','.join(lit_id_list)
        # print(lit_id_str)

        return lit_id_str
    
    else:
        return x['Lit_ID']
    

ClusterMarker_stats_data['Lit_ID'] = ClusterMarker_stats_data.apply(lit_id, axis=1)
print(ClusterMarker_stats_data)

ClusterMarker_stats_data = ClusterMarker_stats_data.drop_duplicates(subset=['Cell_type', 'Gene_ID', 'Lit_ID', 'Score'], keep='first')
print(ClusterMarker_stats_data)

ClusterMarker_stats_data.to_csv('ClusterMarker_stats.csv', index=False)
