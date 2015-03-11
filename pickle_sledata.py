import cPickle as pickle
import gzip
import numpy as np
import data_tweaking as dt

'''
pickleArray[0] = train_set
	pickleArray[0][0] = x 
	pickleArray[0][1] = y
pickleArray[1] = valid_set
	pickleArray[1][0] = x
	pickleArray[1][1] = y 
pickleArray[2] = test_set
	pickleArray[2][0] = x
	pickleArray[2][1] = y
(new part for us)
pickleArray[3] = pretrain_set

Pretraining just sends in train_set[0] (aka, the x's of the training set)
We need to redefine these variables since what we want to pre-train on 
	doesn't actually have labels
'''

#unlabeled_data_file = open("sle_data/alldata_gold_cuis_only.txt","r")
#unlabeled_data_lines = unlabeled_data_file.readlines()
#unlabeled_data_file.close()
#labeled_data_file = open("sle_data/sorted_golddata.txt","r")
#labeled_data_lines = labeled_data_file.readlines()
#labeled_data_file.close()

attrfile = "sle_data/goldattributes.txt"
goldDataString = "sle_data/sorted_golddata.txt"
goldInstancesString = "sle_data/goldinstance.txt"
golddata_matrix = dt.readSparse(attributesString=attrfile,dataString=goldDataString,instancesString=goldInstancesString)
gold_labels = dt.get_labels_according_to_data_order(dataString=goldDataString,instancesString=goldInstancesString)

rows_in_gold = len(golddata_matrix) ## == len(gold_labels)
train_matrix = golddata_matrix[0:(rows_in_gold/3)]
train_labels = gold_labels[0:(rows_in_gold/3)]
valid_matrix = golddata_matrix[(rows_in_gold/3):(2*rows_in_gold/3)]
valid_labels = gold_labels[(rows_in_gold/3):(2*rows_in_gold/3)]
test_matrix = golddata_matrix[(2*rows_in_gold/3):rows_in_gold]
test_labels = gold_labels[(2*rows_in_gold/3):rows_in_gold]
pretrain_matrix = dt.readSparse(attributesString=attrfile,dataString="sle_data/alldata_gold_cuis_only.txt",instancesString="sle_data/allinstance.txt")

pickleArray = [[train_matrix,train_labels],
		[valid_matrix,valid_labels]
		[test_matrix,test_labels]
		[pretrain_matrix]]

print pickleArray[0][0]
print pickleArray[0][1]
print pickleArray[1][0]
print pickleArray[1][1]
print pickleArray[2][0]
print pickleArray[2][1]
print pickleArray[3]

# Pickle and zip to binary data
f = open("sle.pkl","w")
pickle.dump(pickleArray,f)
f.close()
f = open("sle.pkl","rb")
f_out = gzip.open("sle.pkl.gz","wb")
f_out.writelines(f)
f.close()
f_out.close()
