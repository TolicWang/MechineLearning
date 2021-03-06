# -*- coding: utf-8 -*-
# Author: wangchengo@126.com
import numpy as np
import random
import math




def InitCentroids(X, K):
    n = np.size(X, 0)
    rands_index = np.array(random.sample(range(1, n), K))
    centriod = X[rands_index, :]
    return centriod

def findClosestCentroids(X, w, centroids):
    K = np.size(centroids, 0)
    idx = np.zeros((np.size(X, 0)), dtype=int)
    n = X.shape[0]  # n 表示样本个数
    for i in range(n):
        subs = centroids - X[i,:]
        dimension2 = np.power(subs, 2)
        w_dimension2=np.multiply(w,dimension2)
        w_distance2=np.sum(w_dimension2,axis=1)
        if math.isnan(w_distance2.sum()) or math.isinf(w_distance2.sum()):
            w_distance2=np.zeros(K)
            # print 'the situation that w_distance2 is nan or inf'
        idx[i] = np.where(w_distance2 == w_distance2.min())[0][0]
    return idx

def computeCentroids(X, idx, K):
    n, m = X.shape
    centriod = np.zeros((K, m), dtype=float)
    for k in range(K):
        index = np.where(idx == k)[0]# 一个簇一个簇的分开来计算
        temp = X[index, :]  # ? by m # 每次先取出一个簇中的所有样本
        s=np.sum(temp,axis=0)
        centriod[k,:] = s/np.size(index)
    return centriod

def computeWeight(X,centroid,idx,K,belta):
    n, m = X.shape
    weight = np.zeros((1, m), dtype=float)
    D = np.zeros((1,m),dtype=float)
    for k in range(K):
        index = np.where(idx == k)[0]
        temp = X[index, :]  # ? by m
        distance2= np.power((temp - centroid[k,:]),2)  # ? by m
        D = D + np.sum(distance2,axis=0)

    e=1/float(belta-1)
    for j in range(m):
        temp = D[0][j] / D[0]
        weight[0][j] = 1/np.sum((np.power(temp,e)),axis=0)
    return weight

def costFunction(X,K,centroids,idx,w):
    cost = 0
    n, m = X.shape
    D = np.zeros((1, m), dtype=float)
    for k in range(K):
        index = np.where(idx == k)[0]
        temp = X[index, :]
        distance2 = np.power((temp - centroids[k,:]),2)  # ? by m
        D = D + np.sum(distance2, axis=0)

    cost = np.sum(w * D)
    return cost

def isConvergence(costF,max_iter):
    if math.isnan(np.sum(costF)):
        return False
    index = np.size(costF)
    # print(index)
    # print(costF)
    for i in range(index-1):
        if costF[i] < costF[i+1]:
            return False
    if index >= max_iter:
        return True
    elif costF[index-1]==costF[index-2]==costF[index-3]:
        return True
    return 'continue'

def wkmeans(X,K,belta,max_iter):
    n, m = X.shape
    costF =[]
    r = np.random.rand(1, m)
    w = np.divide(r, r.sum())
    centroids = InitCentroids(X, K)
    for i in range(max_iter):
        idx = findClosestCentroids(X, w, centroids)
        centroids = computeCentroids(X, idx, K)
        w = computeWeight(X, centroids, idx, K, belta)
        c = costFunction(X,K,centroids,idx,w)
        costF.append(round(c, 4))
        if i < 2:
            continue
        flag = isConvergence(costF, max_iter)
        if flag == 'continue':
            continue
        elif flag:
            best_labels = idx
            best_centers = centroids
            isConverge = True
            return isConverge, best_labels, best_centers, costF
        else:
            isConverge = False
            return isConverge, None, None, costF




class WKMeans:
    n_clusters=0
    max_iter=0
    belta=0
    best_labels, best_centers = None, None
    isConverge=False
    cost=None
    def __init__(self,n_clusters=3,max_iter=20,belta=7.0    ):
        self.n_clusters=n_clusters
        self.max_iter=max_iter
        self.belta=belta
    def fit(self,X):
        self.isConverge,self.best_labels,self.best_centers,self.cost=wkmeans(
            X=X,K=self.n_clusters,max_iter=self.max_iter,belta=self.belta
        )
        return self

    def fit_predict(self,X,y=None):
        if self.fit(X).isConverge:
            return self.best_labels
        else:
            return 'Not convergence with current parameter ' \
                   'or centroids,Please try again'
    def get_params(self):
        return self.isConverge,self.n_clusters,self.belta
    def get_cost(self):
        return self.cost