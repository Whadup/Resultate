## Deep Learning Eigenvalues

I have prepared a visualization that shows how the eigenvalues of a convolution layer in squeezenet1_1 changes over the course of imagenet training. At epoch 30 of the training, the learning rate was reduced by a multiplicative factor of 0.1. This substantially changes the behavior of the eigenvalues; in the first 30 epochs, the norm of the operator is increasing, after the learning rate reduction the norm starts to decrease. 
Overall, the eigenvalues show heavy-tail behavior.



### Layer 38

The first histogram shows a 3x3 linear convolution layer that maps from 8,112 features to 32,448 features.
<div id='d3div38'></div>
<script>d3.json("data/data38.json", function(x){initHistogram(x,"#d3div38");});</script>

### Layer 59

The second histrogram shows a a 3x3 linear convolution layer that maps from 10,816 features to 43,264 features.
<div id='d3div59'></div>
<script>d3.json("data/data59.json", function(x){initHistogram(x,"#d3div59");});</script>

### All 3x3 Convolution Layers

- [Layer 8](layer8)
- [Layer 15](layer15)
- [Layer 30](layer30)
- [Layer 38](layer38)
- [Layer 45](layer45)
- [Layer 52](layer52)
- [Layer 59](layer59)


### What about the other layers?

Squeezenets are build from so-called Fire-modules. Each module applies two 3x3 convolutions and one 1x1 convolution. The eigenvalues of a 1x1 convolution are just the eigenvalues of its filter matrix with a multiplicity according to the dimensionality. Computing these histograms is simple as we can just apply standard methods.