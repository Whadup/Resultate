<link href="https://fonts.googleapis.com/css?family=Roboto:300" rel="stylesheet">
## Deep Learning Eigenvalues
I have prepared a visualization that shows how the eigenvalues of a convolution layer in squeezenet1_1 changes over the course of imagenet training. At epoch 30 of the training, the learning rate was reduced by a multiplicative factor of 0.1. This substantially changes the behavior of the eigenvalues; in the first 30 epochs, the norm of the operator is increasing, after the learning rate reduction the norm starts to decrease.
<link rel="stylesheet" href="https://whadup.github.io/static-homepage/style.css">
<script src="https://d3js.org/d3.v3.min.js"></script>
<script src="https://whadup.github.io/static-homepage/script.js"></script>
<div id='d3div'></div>
