# 导入 pandas 库，并将其简称为 pd。
import pandas as pd

# 使用 pandas 读取名为 'iris_csv.csv' 的 CSV 文件，并将其存储在变量 irisdata 中。
irisdata = pd.read_csv('C:/Users/15815/Desktop/ollama/iris_csv.csv')
# 打印 irisdata 数据框的前五行，以查看数据的初步情况。
print(irisdata.head())

# 从 irisdata 中选取前四列（即特征列），存储在变量 X 中。
X = irisdata.iloc[:,0:4]
# 从 irisdata 中选取数据类型为 object 的列（通常是目标变量列），存储在变量 y 中。
y = irisdata.select_dtypes(include=[object])
# 打印 y 数据框的前五行，以查看目标变量的初步情况。
print(y.head())

# 从 scikit-learn 库中导入预处理模块。
from sklearn import preprocessing
# 创建一个标签编码器对象 le，用于将目标变量中的类别标签转换为整数。
le = preprocessing.LabelEncoder()

# 对 y 中的每个列应用标签编码器，将类别标签转换为整数。
y = y.apply(le.fit_transform)

# 从 scikit-learn 库中导入 train_test_split 函数，用于将数据集分割为训练集和测试集。
from sklearn.model_selection import train_test_split
# 将 X 和 y 分割为训练集和测试集，测试集占总数据的 20%。
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20)

# 从 scikit-learn 库中导入 StandardScaler 模块，用于标准化特征数据。
from sklearn.preprocessing import StandardScaler
# 创建一个 StandardScaler 对象 scaler。
scaler = StandardScaler()
# 使用训练集数据拟合 scaler，确定数据的均值和标准差。
scaler.fit(X_train)

# 使用 scaler 转换训练集和测试集的特征数据，使其标准化。
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# 从 scikit-learn 库中导入 MLPClassifier 类，用于创建多层感知器分类器。
from sklearn.neural_network import MLPClassifier
# 创建一个 MLPClassifier 对象 mlp，设置隐藏层的大小为 (10, 10, 10)，最大迭代次数为 1000。
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10),max_iter=1000)
# 使用训练集数据训练 mlp 分类器。
mlp.fit(X_train,y_train.values.ravel())
# 使用训练好的 mlp 分类器对测试集数据进行预测。
predictions = mlp.predict(X_test)

# 从 scikit-learn 库中导入 classification_report 和 confusion_matrix 函数，用于评估分类器的性能。
from sklearn.metrics import classification_report, confusion_matrix
# 打印混淆矩阵，显示实际类别与预测类别之间的关系。
print(confusion_matrix(y_test,predictions))
# 打印分类报告，显示主要的分类指标，如精确度、召回率、F1分数等。
print(classification_report(y_test,predictions))

# 从 scikit-learn 库中导入 accuracy_score 函数，用于计算分类器的准确率。
from sklearn.metrics import accuracy_score
a=accuracy_score(y_test,predictions)
a=a*100
print("Accuracy:",a,"%")