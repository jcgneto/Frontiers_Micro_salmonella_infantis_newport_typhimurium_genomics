import pandas as pd
import dask
import dask.dataframe as dd
from glob import glob
import os, re, sys, random
import numpy as np
import itertools

file = "metadata_sra_collection_date_isolation_source_all.txt"
df = pd.read_csv(file, sep=",")
df["isolation_source_lower"] = df["isolation_source"].str.lower()

df['source'] = pd.np.where(df.isolation_source_lower.str.contains("missing"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("produce"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("meal"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("water"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("pork"), "Swine",
                    pd.np.where(df.isolation_source_lower.str.contains("porcine"), "Swine",
                    pd.np.where(df.isolation_source_lower.str.contains("swine"), "Swine",
                    pd.np.where(df.isolation_source_lower.str.contains("scrofa"), "Swine",
                    pd.np.where(df.isolation_source_lower.str.contains("cattle"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("hog"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("cow"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("calf"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("taurus"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("beef"), "Bovine",
                    pd.np.where(df.isolation_source_lower.str.contains("chicken"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("turkey"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("egg"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("poultry"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("gallus"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("broiler"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("avian"), "Poultry",
                    pd.np.where(df.isolation_source_lower.str.contains("horse"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("equine"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("canis"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("dog"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("feed"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("abscess"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("environmental"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("pet"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("mouse"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("food"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("swab"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("ovine"), "Environmental/Others",
                    pd.np.where(df.isolation_source_lower.str.contains("urine"), "Human",
                    pd.np.where(df.isolation_source_lower.str.contains("stool"), "Human",
                    pd.np.where(df.isolation_source_lower.str.contains("blood"), "Human", "Environmental/Others"
                               ))))))))))))))))))))))))))))))))))))

df.groupby("source").count()

df.to_csv("metadata_cleaned_final_new.csv", index=False, header=True)
