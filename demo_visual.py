# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import ch
# 避免 windows 下中文乱码
ch.utf8writer_register()
# 避免图像注释中文乱码
ch.set_ch()

from gensim.models import word2vec
from gensim import models
import logging

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

def main():
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	# model = models.Word2Vec.load_word2vec_format('wiki.zh.model.bin',binary=True)
	model = word2vec.Word2Vec.load('wiki.zh.model')

	print("提供 3 种测试模式")
	print("输入一个词，则去寻找前二十个该词的相似词")
	print("输入两个词，则去计算两个词的余弦相似度")
	print("输入三个词，进行类比推理")

	while True:
		query = raw_input("请输入: ")
		query = query #.decode('utf-8')
		q_list = query.split()
		try:
			if len(q_list) == 1:
				print("相似词前 20 排序")
				res = model.most_similar(q_list[0], topn = 20)
				for item in res:
					print(item[0]+","+str(item[1]))

			elif len(q_list) == 2:
				print("计算 Cosine 相似度")
				res = model.similarity(q_list[0], q_list[1])
				print(res)
				
			else:
				print("%s之于%s，如%s之于" % (q_list[0], q_list[2], q_list[1]))
				res = model.most_similar([q_list[0], q_list[1]], [q_list[2]], topn = 20)
				for item in res:
					print(item[0]+","+str(item[1]))
					
			# 可视化
			visualize(model, q_list)
			visualize_3d(model, q_list)
			print("----------------------------")
		except Exception as e:
			print(repr(e))


def visualize(model, word):
	"""
	根据输入的词搜索邻近词然后可视化展示 2D
	参数：
		model: Word2Vec 模型
		word: 词汇列表
	"""

	# 找出最相似的多个词
	words = [wp[0] for wp in model.most_similar(word, topn=50)]

	# 提取出词对应的词向量
	wordsInVector = [model[word] for word in words]

	# 进行 PCA 降维
	pca = PCA(n_components=2)
	pca.fit(wordsInVector)
	X = pca.transform(wordsInVector)

	# 绘制图形
	xs = X[:, 0]
	ys = X[:, 1]

	plt.figure(figsize=(10, 6))
	plt.scatter(xs, ys, marker='o')

	# 遍历所有的词添加点注释
	for i, w in enumerate(words):
		plt.annotate(
			w,
			xy=(xs[i], ys[i]), xytext=(6, 6),
			textcoords='offset points', ha='left', va='top',
			**dict(fontsize=10)
		)
	plt.show()
	
def visualize_3d(model, word):
	"""
	根据输入的词搜索邻近词然后可视化展示 3D
	参数：
		model: Word2Vec 模型
		word: 词汇列表
	"""

	# 找出最相似的多个词
	words = [wp[0] for wp in model.most_similar(word, topn=20)]

	# 提取出词对应的词向量
	wordsInVector = [model[word] for word in words]

	# 进行 PCA 降维
	pca = PCA(n_components=3)
	pca.fit(wordsInVector)
	X = pca.transform(wordsInVector)

	# 绘制图形
	xs = X[:, 0]
	ys = X[:, 1]
	zs = X[:, 2]

	fig = plt.figure(figsize=(10, 6))
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(xs, ys, zs, marker='o')

	# 遍历所有的词添加点注释
	for i, w in enumerate(words):
		x2, y2, _ = proj3d.proj_transform(xs[i], ys[i], zs[i], ax.get_proj())
		ax.annotate(
			w,
			xy=(x2, y2), xytext=(6, 6),
			textcoords='offset points', ha='left', va='top',
			**dict(fontsize=10)
		)
	plt.show()
			
		
		
if __name__ == "__main__":
	main()
