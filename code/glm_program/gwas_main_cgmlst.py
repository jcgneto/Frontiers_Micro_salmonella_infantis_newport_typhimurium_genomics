#/usr/bin/env python
import statsmodels.api as sm
from statsmodels.formula.api import glm
from scipy import stats
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import csv, sys, re, os, subprocess

# Usage
# python gene_gwas.py sistr.csv gene_presence.Rtab monophasic group_1 monophasic_gwas_filtered.csv kmer/Gene

# Functions
def glm_formula(df, dependent_var, i):
    return dependent_var + ' ~ ' + df.columns[i]
def division_zero(n, d):
    return n / d if d else 0

# Read from command line
args = len(sys.argv)
sistr_mlst_file = sys.argv[1]
rtab_kmer_file = sys.argv[2]
response = sys.argv[3]
group_id = sys.argv[4]
# Add headers to final output manually
output_file = sys.argv[5]
output_file_no_filter = sys.argv[6]
kmer_gene = sys.argv[7]

# Check input files manually
# MLST may need to be filtered:
# status, output = subprocess.getstatusoutput("awk -F, 'NF==10' mlst_output.csv >> mlst_output_filtered.csv")
df1 = pd.read_csv(sistr_mlst_file, header=0)
df1 = df1.rename(columns = {'phenotype' : response})
d11 = df1[['id', response]]

# Check input files manually
# some Rtabs have ID.fasta
df2 = pd.read_csv(rtab_kmer_file, sep='\t').transpose().reset_index()
df2.columns=df2.iloc[0]
df2.drop([0])
df2 = df2.rename(columns = {kmer_gene : 'id'})
d22 = df2.drop([0])

resp = d11[['id', response]]
resp_gwas_tmp = pd.merge(resp, d22, on = 'id')
# Remove columns with only 0s or 1s; otherwise GLM fails
t3 = resp_gwas_tmp.loc[:,resp_gwas_tmp.apply(pd.Series.nunique) != 1]
# Remove columns with only 1 0, or only 1 1
t3 = t3.set_index("id")
thres = t3.shape[0] - 1
t1 = t3[t3.columns[t3.sum()!=thres]]
t4 = t1[t1.columns[t1.sum()!=1]]
# Remove rows with NaN
t5 = t4.replace('?', np.nan)
t6 = t5.replace('-', np.nan)
resp_gwas = t6.dropna(axis = 0, how = 'any')
response_fin = resp_gwas

data12_merged = pd.merge(d11, d22, on = 'id')

# Make response the first column
col = response_fin.pop(response)
response_fin.insert(0, col.name, col)
print(response_fin.head())

number_genes = len(response_fin.columns) - 1
n_comparisons =  number_genes
# Set global parameters
sig_cut_off = 0.05 / n_comparisons

final = []
for i in range(1, len(response_fin.columns)):
    gene_kmer_id = response_fin.columns[i]
    f = response + ' ~ ' + "Q(response_fin.columns[i])"
    md = glm(formula = f, data = response_fin, family = sm.families.Binomial(link = sm.families.links.logit)).fit()
    crosstab = pd.crosstab(data12_merged[response], data12_merged[gene_kmer_id])

    # Get 2 X 2 contigency table
    crosstab = pd.crosstab(data12_merged[response], data12_merged[gene_kmer_id])

    # Calculate statistics for binomial model
    beta = md.params[1]  # output
    odds_ratio = np.exp(beta)  # output
    lower_ci_odds_ratio = np.exp(md.conf_int()[0][1])  # output
    upper_ci_odds_ratio = np.exp(md.conf_int()[1][1])  # output
    aic = md.aic  # output
    model_deviance = md.deviance  # output
    p_value_model = md.pvalues[1]  # output
    transf_p_value_model = -1*np.log10(p_value_model)  # output
    pass_sign_binomial_model = "yes" if (p_value_model < sig_cut_off) else "no"  # output

    # Calculate statistics for chi_squared test
    chi_squared_pvalue = stats.chi2_contingency(crosstab)[1]  # output
    transf_chi_squared_pvalue = -1*np.log10(chi_squared_pvalue)  # output
    pass_sign_chi_sq_pvalue = "yes" if (chi_squared_pvalue < sig_cut_off) else "no"  # output

    # Confusion matrix
    cm1 = confusion_matrix(data12_merged[response].tolist(),data12_merged[gene_kmer_id].tolist())
    total1=sum(sum(cm1))
    # accuracy1=(cm1[0,0]+cm1[1,1])/total1
    accuracy1=division_zero((cm1[0,0]+cm1[1,1]), total1)
    accur = accuracy1
    # sensitivity1 = cm1[1,1]/(cm1[1,1]+cm1[1,0])
    sensitivity1 = division_zero(cm1[1,1], (cm1[1,1]+cm1[1,0]))
    sensit = sensitivity1
    # specificity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    specificity1 = division_zero(cm1[0,0], (cm1[0,0]+cm1[0,1]))
    specif = specificity1
    # ppv1 = cm1[1,1]/(cm1[1,1]+cm1[0,1])
    ppv1 =division_zero(cm1[1,1], (cm1[1,1]+cm1[0,1]))
    pos_pred_value = ppv1
    # npv1 = cm1[0,0]/(cm1[0,0]+cm1[1,0])
    npv1 = division_zero(cm1[0,0], (cm1[0,0]+cm1[1,0]))
    neg_pred_value = npv1

    # New stats
    prop_feature_biphasic = division_zero(cm1[0, 1], (cm1[0, 1] + cm1[0, 0]))*100  # output
    prop_feature_monophasic = division_zero(cm1[1, 1], (cm1[1, 1] + cm1[1, 0]))*100  # output

    rows = [group_id,response,gene_kmer_id,beta,odds_ratio,lower_ci_odds_ratio,upper_ci_odds_ratio,aic,model_deviance,p_value_model,transf_p_value_model,pass_sign_binomial_model,chi_squared_pvalue,transf_chi_squared_pvalue,pass_sign_chi_sq_pvalue,accur,sensit,specif,pos_pred_value,neg_pred_value,prop_feature_biphasic,prop_feature_monophasic]
    final.append(rows)

# Filter conditions
header = ["group_id","response","gene_kmer_id","beta","odds_ratio","lower_ci_odds_ratio","upper_ci_odds_ratio","aic","model_deviance","p_value_model","transf_p_value_model","pass_sign_binomial_model","chi_squared_pvalue","transf_chi_squared_pvalue","pass_sign_chi_sq_pvalue","accur","sensit","specif","pos_pred_value","neg_pred_value","prop_feature_biphasic","prop_feature_monophasic"]
dff = pd.DataFrame(final, columns=header)

hits = dff[(dff['lower_ci_odds_ratio'] > 1) & (dff['upper_ci_odds_ratio'] > 1) & (dff['pass_sign_binomial_model'] == 'yes') & (dff['pass_sign_chi_sq_pvalue'] == 'yes') & (dff['accur'] > 0.90) & (dff['pos_pred_value'] > 0.90) & (dff['neg_pred_value'] > 0.90)]

with open(output_file, 'a') as f:
    hits.to_csv(f, index=False, header=False)

with open(output_file_no_filter, 'a') as f:
    dff.to_csv(f, index=False, header=False)
