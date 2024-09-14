import pandas as pd
from optbinning import OptimalBinning
import numpy as np
import pwlf # type: ignore
from sklearn.linear_model import Ridge
import copy
import itertools

# global bs
# bs = dict()

def apply_optimal_binning(data, feature, target):
    '''
    使用 OptimalBinning 对数据进行分箱处理
    :data: 数据
    :feature: 特征
    :target: 目标变量
    '''
    
    opt_bin = OptimalBinning(name=feature, dtype="numerical", min_bin_size=0.005, min_bin_n_event=10)
    opt_bin.fit(data[feature], target)
    
    # 获取并显示分箱区间
    binning_splits = opt_bin.splits
    
    # 获取最小值和最大值
    min_val = data[feature].min()
    max_val = data[feature].max()
    
    # 构建完整的区间
    intervals = [min_val] + list(binning_splits) + [max_val]
    interval_pairs = [(intervals[i], intervals[i+1]) for i in range(len(intervals)-1)]
    
    def get_interval(x):
        for _, (a, b) in enumerate(interval_pairs):
            if a <= x <= b:
                return str([round(a, 4), round(b, 4)])
        return str([])
    
    binned_data_interval = data[feature].apply(get_interval)
    
    def get_data(x):
        for _, (a, b) in enumerate(interval_pairs):
            if a <= x <= b:
                return (a+b)/2
        return -1

    binned_data_mean = data[feature].apply(get_data)
    
    return binned_data_mean, binned_data_interval


def remark(dataall, features, features_formul):
    '''
    对数据进行分箱处理，并使用线性回归模型进行拟合
    :data: 数据
    :features: 成品特征
    :features_formul: 配方特征
    '''
    data = dataall[features + ['异常类型']].copy()
    # X 是特征，y 是目标变量
    X1 = data.drop(columns=['异常类型'])
    X2 = data.drop(columns=['异常类型'])
    y = data['异常类型']

    # 对每个特征进行分箱并替换原始数据
    for col in X1.columns:
        X1[col], X2[col] = apply_optimal_binning(data, col, y)
    
    # 选择特征
    features2 = [x + '区间' for x in features]
    X2 = X2[features]
    X2.columns = features2
    
    featuresplus = features + features2
    
    # 拟合单个元素的作用
    # 返回modelpwlfs
    modelpwlfs = dict()
    dataxy = pd.concat([X1, X2, y], axis=1)
    for col in features:
        dataxyg = dataxy[[col, '异常类型']].groupby(col).mean().reset_index() # 单个特征与异常类型的均值
        dataxyg.sort_values(col, inplace=True)
        r = pwlf.PiecewiseLinFit(dataxyg[col], dataxyg['异常类型'])
        r.fit(len(dataxyg))
        modelpwlfs[col] = r
        
    # 拟合单个元素产生的y值
    dataxy_cov = dataxy.groupby(featuresplus).mean().reset_index() # 多个特征与异常类型的均值
    dataxy_cov_pwlf = copy.deepcopy(dataxy_cov)
    # 转化为用区间均值预测的数据
    for col in features:
        dataxy_cov_pwlf[col] = modelpwlfs[col].predict(dataxy_cov_pwlf[col].values)

    r = Ridge(fit_intercept=False)
    r.fit(dataxy_cov_pwlf[features], dataxy_cov_pwlf['异常类型'])
    
    # 寻找最好的成品值
    dataxy_cov['异常率'] = r.predict(dataxy_cov_pwlf[features])
    dataxy_cov.sort_values('异常率', ascending=True, inplace=True)
    best_quality = dataxy_cov[features2][:3].round(4).reset_index(drop=True).T.to_dict()
    
    # 返回最佳配方
    best_formul = dict()
    data_formul = pd.concat([X2, dataall[features_formul]], axis=1)
    for i in range(3):
        data_temp = copy.deepcopy(data_formul)
        quality = best_quality[i]
        for k, v in quality.items():
            data_temp = data_temp[data_temp[k] == v]
            data_temp.sort_values(by=features_formul[:-1], inplace=True, ascending=True)
            best_formul[i] = data_temp[features_formul].iloc[0].T.to_dict()
    
    best_best_formul = []
    for i in range(3):
        best_best_formul.append({
            'quality': best_quality[i],
            'formulation': best_formul[i]
        })
    
    # 返回数据集合
    dataxy_response = dataxy_cov[features + ['异常率']].copy()
    dataxy_response.drop_duplicates(subset=features, inplace=True)

    return dataxy_response, best_best_formul
        
