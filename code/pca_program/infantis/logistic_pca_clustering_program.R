# libraries needed
library(logisticPCA)
library(stats)
library(tidyverse)
library(skimr)
library(ggpubr)
library(vegan)
library(reshape2)
#library(ggnewscale)
library(forcats)
library(naniar)
library(data.table)
library(rARPACK)
library(cluster)   
library(factoextra)
library(dendextend)
library(rstatix)
library(modelr)
library(plyr)
#library(broom)
library(plotly)

# read the data in and prepare for analysis
training_data <- read.csv("training_data_infantis.csv")
colnames(training_data)[1] <- "id"
training_data <- column_to_rownames(training_data, var = "id") 

########################################################################################
# logistic pca (first step of the analysis - we need pca_data as output, and progress to the next step of the analysis using pca_data as an input
set.seed(123)
logpca_cv = cv.lpca(training_data, ks = 2, ms = 1:10, partial_decomp = TRUE, max_iters = 1000)
logpca_model <- logisticPCA(training_data, k = 2, m = which.min(logpca_cv), partial_decomp = TRUE, max_iters = 1000)
pca_scores <- logpca_model$PCs
colnames(pca_scores)[1:2] <- c("PC1", "PC2")
pca_data1 <- as.data.frame(pca_scores)
pca_data2 <- rownames_to_column(pca_data1, var = "id")

# read out variance explained

deviance_model <- logpca_model$prop_deviance_expl
write.csv(deviance_model, "deviance_model.csv")

# read out the PCA data
write.csv(pca_data2, "pca_data2.csv")

######################################################################################

# Kmeans clustering analysis

#Elbow Method for finding the optimal number of clusters
set.seed(123)
# Compute and plot wss for k = 1 to k = 10.
k.max <- 10
cluster_data <- pca_data1
data <- cluster_data
wss <- sapply(1:k.max, 
              function(k){kmeans(data, k, nstart=50,iter.max = 10)$tot.withinss})
wss2 <- as.data.frame(wss)
write.csv(wss2, "wss2.csv")

km.final <- kmeans(cluster_data, 3) # get clusters
cluster <- as.data.frame(km.final$cluster) # transform to data.frame
colnames(cluster)[1] <- "cluster" # change column name
cluster2 <- rownames_to_column(cluster, "id") # move id to column name

# read out the PCA data
write.csv(cluster2, "cluster2.csv")


