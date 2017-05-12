import sys
import pandas as ps
import random
import numpy as np

from sklearn import cluster as clusters, metrics as Metric
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS

def gender_dev(filename):
    dataFrame = ps.read_csv(filename)
    cols = ['Country', 'Education - Female','Education - Male','Income - Female','Income - Male']
    cols_1 = ['Country', 'Income - Female','Income - Male']
    cols_2 = ['Country', 'Education - Female','Education - Male']
    dataFrame = dataFrame.iloc[:,(1,9,10,11,12)]
    dataFrame2 = ps.DataFrame(dataFrame[dataFrame.iloc[:,(1)] != '..'])

    dataFrame2.columns = cols
   
    dataFrame2.to_csv("bardata_income.csv", sep = ',', columns = cols_1)
    dataFrame2.to_csv("bardata_edu.csv", sep = ',', columns = cols_2)

def Sampling(file1, file2):
	file_name = "Sample.csv"
	dataFrame = ps.read_csv(file1)
	dataFrame1 = ps.read_csv(file2)
	dataFrame2 = ps.DataFrame()

	#Columns used from the dataset : 
	dataFrame = dataFrame.iloc[:,(0,1,5,6,8)].fillna(0)
	dataFrame['Gross National Income'] = dataFrame1.iloc[:,(11)].fillna(0)
	dataFrame.columns = ['GII', 'Country','Par_Rep', 'Sec_Edu', 'Lab_Part', 'Income']
	dataFrame2 = dataFrame[dataFrame.Country != '..']
	dataFrame2 = dataFrame2[dataFrame2.GII != 0]
	dataFrame2 = dataFrame2[dataFrame2.Par_Rep != '..']
	dataFrame2 = dataFrame2[dataFrame2.Sec_Edu != '..']
	dataFrame2 = dataFrame2[dataFrame2.Lab_Part != '..']
	dataFrame2 = dataFrame2[dataFrame2.Income != '..']
	print(dataFrame2.shape)
	return
	return dataFrame2

def generateTestData(samples,file_name,ty):
	samples['type'] = ps.Series(int(ty),index=samples.index)
	samples.columns = ['C1','C2','type']
	samples.to_csv(file_name, sep = ',')

def applyPCA(dataFrame):
	pca = PCA(n_components = 2)
	return ps.DataFrame(pca.fit_transform(dataFrame))

def applyMDS(dataframe, type, file_name):
    dis_mat = Metric.pairwise_distances(dataframe, metric = type)
    mds = MDS(n_components=2, dissimilarity='precomputed')
    df = ps.DataFrame(mds.fit_transform(dis_mat))
    if "random" in file_name:
    	print(file_name)
    	generateTestData(df, file_name, 1)
    else:
    	print(file_name)
    	generateTestData(df, file_name, 2)


def getDimensionality(dataFrame, file_name):
	#Generate the csv file for plotting the Eigen Values Vs. Component
	#For plotting the Scree Plots
	X_std = StandardScaler().fit_transform(dataFrame)
	mean_vec = np.mean(X_std, axis=0)
	cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
   
	cov_mat = np.cov(X_std.T)
	eig_vals, eig_vecs = np.linalg.eig(cov_mat)
	eig_vals = list(eig_vals)
	vals = dataFrame.columns
	finalData = ps.DataFrame({'cmpnt': vals, 'eigen':eig_vals})
	finalData = finalData.sort_values(['eigen'], ascending = False)
	finalData.to_csv(file_name, sep = ',',  index = False)

def getLoadings(dataFrame, file_name):
	#Get the highest PCA Loadings
	pca = PCA()
	pca.n_components = 9
	df = ps.DataFrame(pca.fit_transform(dataFrame))
	print(pca.explained_variance_ratio_)
	df2 = ps.DataFrame(pca.components_, columns = dataFrame.columns, index = ['PC-1','PC-2', 'PC-3', 'PC-4', 
		'PC-5','PC-6', 'PC-7', 'PC-8', 'PC-9']).abs()
	df2 = np.square(df2)
	df2 = df2.sum(axis = 0)
	df2 = np.sqrt(df2)
	df2 = df2.sort_values(ascending = False)
	columns = ['attr', 'loadings']
	df3 = ps.DataFrame(columns= columns)
	df3 = df2.reset_index(level=0)
	df3.columns = columns
	
	df3.to_csv(file_name, sep=',',  index = False)
	return 

def main():

	df = gender_dev('gender_development.csv')
	sys.exit()

	file1 = "gender_inequality.csv"
	file2 = "gender_development.csv"
	samples = ps.read_csv('Sample.csv')
	print(samples)
	print(samples.shape)

	#Apply PCA
	temp = samples.iloc[:,(0,2,3,4,5)]
	print(temp.shape)
	samples_PCA = applyPCA(temp)
	print(samples_PCA)
	samples_PCA.to_csv('temp.csv', sep = ',',  index = False)	
	print(samples_PCA.shape)

	final = ps.DataFrame(columns = ['Country', 'PCA1', 'PCA2'])
	final['Country'] = samples.iloc[:,(1)]
	print(samples.iloc[:,(1)].shape)
	
	colors = []
	for i in range(len(samples)):
		colors.append(0)
	for i in range(len(samples)):
		if i < 50:
			colors[i] = 1
		elif i < 100:
			colors[i] = 2
		else:
			colors[i] = 3

	final = ps.concat([ps.DataFrame(samples.iloc[:,(1)]), samples_PCA], axis = 1)
	final = ps.concat([final, ps.DataFrame(colors)], axis = 1)
	final.columns = ['Country', 'PCA1', 'PCA2', 'color']
	print(final)
	final.to_csv('PCA_Samples.csv', sep = ',',  index = False)
	#Generate dataset after fitting PCA - 2D 
	generateTestData(samples_PCA,"PCA_Samples.csv",1)

if __name__ == "__main__":
	main()