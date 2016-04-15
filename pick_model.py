import sys
# Slightly different for NNs as we use Theano mechanisms
is_nn = False
is_w2v = False
if len(sys.argv) > 2:
    if sys.argv[2] == "w2v":
        print "is_w2v == True"
        is_w2v = True
    else:
        print "is_nn == True"
        is_nn = True

iteration = sys.argv[1]

preamble = 'results_run_sle_sda_cui/'
# This array will be used to see which model performed best
# We then look at that model's external test set accuracy
models = []

for i in range(1,4):
    for j in range(1):#20):
        new_preamble = preamble + str(j)+"_"+str(i)
        f = open(new_preamble+"_labels.txt","r")
        labels = f.readlines()
        f.close()
        f = open(new_preamble+"_p_values.txt","r")
        p_values = f.readlines()
        f.close()
        correct = 0
        incorrect = 0
        fold_accuracies = []

        if is_nn: # this is because of how theano saves p value stuff
            #nn_actual_p_values = []
            for k in range(len(labels)):
                label = labels[k].strip()
                p_value = p_values[k].strip()
                p_value = p_value[:3] # This is because we have values like 0.000000e+00
                if p_value == "0.0": # We were right as per Theano
                    #nn_actual_p_values.append(label+"\n")
                    correct += 1
                else: # We were wrong
                    incorrect += 1
                    #if label == "0.0":
                    #    nn_actual_p_values.append("1.0\n")
                    #else:
                    #    nn_actual_p_values.append("0.0\n")

        else:
            for j in range(len(labels)): # labels and p_values are the same size
                label = float(labels[j].strip())
                if is_w2v: # We could have stripped out the other p values, but this was faster
                    guess = float(p_values[j].split(",")[0].strip())
                else:
                    guess = float(p_values[j].strip())
                # If/else makes it easier since we can vary the amount of datapoints per fold
                if label == round(guess):
                    correct += 1
                else:
                    incorrect += 1
        fold_accuracies.append(float(correct)/(float(correct)+float(incorrect)))
    models.append(float(sum(fold_accuracies))/float(len(fold_accuracies)))
    f = open(preamble+"model_accuracies.txt","w")
    f.write("\t".join(map(str,models)))
    f.close()
best_model = str(models.index(max(models)))
print "Using model "+best_model

f = open(preamble+iteration+"_best_model.txt","w")
f.write(best_model)
f.close()
