""" A script to randomly sample the required number of sentences from the given file and split them into training and test data"""
import random
import time
import sys

if len(sys.argv) !=6:
    print("Usage: 'path to the source file ' \
    'path to the output file train' \
    'path to the output file test' \
    'number of sentences to be sampled for training'\
    'number of sentences to be sampled for testing")
    sys.exit(1)

source_file = sys.argv[1]
print(source_file)
output_file_train = sys.argv[2]
output_file_test = sys.argv[3]
number_of_sentences_train = int(sys.argv[4])
number_of_sentences_test = int(sys.argv[5])

source_data = open(source_file).read()
lines = source_data.split('\n')
sentences = []
for line in lines :
    sentences.append(line.split('\t'))
random.seed(time.time())
# print(len(sentences))
random.shuffle(sentences)

final_sentences_train = sentences[:number_of_sentences_train]
# print(len(final_sentences_train))
left_over_sentences = sentences[(number_of_sentences_train + 1 ): ]
# print(len(left_over_sentences))
output_data_train = []
for index in range(len(final_sentences_train)):
    if final_sentences_train[index] == ['']:
        print(index)
        continue
    output_line = final_sentences_train[index][0] \
    + "\t" + final_sentences_train[index][1]
    output_data_train.append(output_line)

# print("TRAIN")
# print(output_data_train)
# print("TEST")   
final_sentences_test = random.sample(left_over_sentences, number_of_sentences_test)
output_data_test = []
for index in range(len(final_sentences_test)):
    output_line = final_sentences_test[index][0] + \
    "\t" + final_sentences_test[index][1]
    output_data_test.append(output_line)
# print(output_data_test)
write_file_train = open(output_file_train,"a")
write_file_test = open(output_file_test,"a")

for line in output_data_train:
    write_file_train.write(line)
    write_file_train.write("\n")

for line in output_data_test:
    write_file_test.write(line)
    write_file_test.write("\n")

