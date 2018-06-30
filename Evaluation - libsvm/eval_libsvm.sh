#!/usr/bin/env bash
topics=(actor author politic director all)
#topics=(director)
mkdir result
mkdir model
for i in ${topics[@]}; do
	mkdir result/${i}
    mkdir model/${i}
	svm-train -s 0 -t 2 data/${i}/${i}.txt_train_70.0.txt model/${i}/${i}.txt_train_70.0.model
	svm-predict data/${i}/${i}.txt_test_30.0.txt model/${i}/${i}.txt_train_70.0.model result/${i}/${i}.txt_test_30.0.output>result/${i}/${i}.txt_test_30.0.accuracy
	
	svm-train -s 0 -t 2 data/${i}/${i}.txt_train_50.0.txt model/${i}/${i}.txt_train_50.0.model
	svm-predict data/${i}/${i}.txt_test_50.0.txt model/${i}/${i}.txt_train_50.0.model result/${i}/${i}.txt_test_50.0.output>result/${i}/${i}.txt_test_50.0.accuracy
	
	svm-train -s 0 -t 2 data/${i}/${i}.txt_train_30.0.txt model/${i}/${i}.txt_train_30.0.model
	svm-predict data/${i}/${i}.txt_test_70.0.txt model/${i}/${i}.txt_train_30.0.model result/${i}/${i}.txt_test_70.0.output>result/${i}/${i}.txt_test_70.0.accuracy
done
