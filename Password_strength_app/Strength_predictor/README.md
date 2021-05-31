# PASSWORD STRENGTH PREDICTOR USING DEEP LEARNING AND NLP
Traditonal methods of checking the strength of a password involve using regular expressions and pattern recognition.

I've developed a neural network to take care of the task.

Natural language processing techniques usually involve converting sentences to tokens and further converting them to word vectors. The output is then fed into a neural network such as a
RNN or an LSTM.

I've used a similar technique where each word is considered as a sentence and each of the characters in the word are tokens. These are then further coverted to vectors. 
and fed as input to a LSTM network which predicts either 0(weak) or 1(strong).
The standard tokenizer from keras has been used to handle the tokenization.

An accuracy of around 99% has been achieved and using a LSTM makes sure that repition of characters are penalised.

The model then predicts a password as strong provided it has a length of 15 and equal no. of alphabets, numbers andspcial characters. 
