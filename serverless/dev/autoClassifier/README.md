# audio-classifier-keras-cnn
Audio Classifier in Keras using Convolutional Neural Network

*ok this is a public repo, but it's not ready for public distribution.  Just letting a few students & colleagues know about it for now.
Wrote the main code Monday night, got the results Tuesday morning, added the augmentation Wednesday night (for future use)...now posting this repo on Thursday.*

**Credits:** This is an amalgamation of the [Keras MNIST CNN example](https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py) and [@keunwoochoi](https://github.com/keunwoochoi)'s [CNN Music Tagger](https://github.com/keunwoochoi/music-auto_tagging-keras) -- I would truly say my code is just a "dumbed-down rip-off" of Choi's work (just not his exact code because it was too clever for me).  In particular, like in Choi's work, it uses mel-spectrograms as inputs, and a multi-layer CNN with Batch Normalization and ELU activations. (Although ReLU seems to work just as well as ELU on the data I've tried so far.) Unlike Choi's work, the network uses the same kernel size for all layers (that's part of the "dumbed down" nature of the code, but it still works), the melgram-shape of the network input is not hardcoded and adapts to whatever the shape (of the first file) is, and I threw in an optional thing for data augmentation which may come in handy later.

*(Regarding Batch Normalization: Changing the `batch_size` variable between training and evaluation may not be a good idea.)*


## Dependencies
* Python
* numpy
* keras
* theano or tensorflow (as backends)
* librosa

## Quick Start
* In `Samples/`, create  subdirectories for each class and put your audio files in them.
* run `python preprocess_data.py`
* run `python train_network.py`
* optional: run `python eval_network.py`


## Data Preparation
### Data organization:
Sound files should go into a directory called `Samples/` that is local off wherever the scripts are being run.  Within `Samples`, you should have subdirectories which divide up the various classes.

Example: for the [IDMT-SMT-Audio-Effects database](https://www.idmt.fraunhofer.de/en/business_units/m2d/smt/audio_effects.html), using their monophonic guitar audio clips...

    $ ls -F Samples/
    Chorus/  Distortion/  EQ/  FeedbackDelay/  Flanger/   NoFX/  Overdrive/  Phaser/  Reverb/  SlapbackDelay/
    Tremolo/  Vibrato/
    $
(Within each subdirectory of `Samples`, there are loads of .wav or .mp3 files that correspond to each of those classes.)
For now, it's assumed that all data files have the same length & sample rate.  
Also, `librosa` is going to turn stereo files into mono by, e.g. averaging the left & right channels. 

*"Is there any sample data that comes with this repo?"  Not right now, sorry.  So the Samples directory 'ships' as empty.*


### Data preprocessing and/or augmentation:
You don't *have* to preprocess or augment the data.  If you preprocess, the data-loading will go *much* faster (e.g., 100 times faster) the next time you try to train the network. So, preprocess.

The "augmentation" will [vary the speed, pitch, dynamics, etc.](https://bmcfee.github.io/papers/ismir2015_augmentation.pdf) of the sound files ("data") to try to "bootstrap" some extra data with which to train.  It can either be performed *within* the preprocessing step, or you can do it *before* preprocessing as a standalone step (i.e., if you really want to be able to listen to what these augmented datasets sound like). To save disk space, I recommend doing it during preprocessing rather than as a standalone.

If you want to augment first as a standalone, then you'll run it as

`$ python augment_data.py <N>  Samples/*/*`

where N is how many augmented copies of each file you want it to create.  It will place all of these in the Samples/ directory with some kind of "_augX" appended to the filename (where X just counts the number of the augmented data files).

Preprocessing will generate mel-spectrograms of all data files, and create a "new version" of `Samples/` called `Preproc/`, with the same subdirectory names, but all the .wav and .mp3 files will have ".npy" on the end now.

To do the preprocessing you just run

`$ python preprocess_data.py`

...which currently doesn't DO any data augmentation, but I'm about to add that in *very* soon.


## Training & Evaluating the Network
`$ python train_network.py`
That's all you need.  (I should add command-line arguments to adjust the layer size and number of layers...later.)

It will perform an 80-20 split of training vs. testing data, and give you some validation scores along the way.  

It's set to run for 2000 epochs, feel free to shorten that or just ^C out at some point.  It automatically does checkpointing by saving(/loading) the network weights via a new file `weights.hdf5`, so you can interrupt & resume the training if you need to.

After training, more diagnostics -- ROC curves, AUC -- can be obtained by running

`$ python eval_network.py`

## Results
On the [IDMT Audio Effects Database](https://www.idmt.fraunhofer.de/en/business_units/m2d/smt/audio_effects.html) using the 20,000 monophonic guitar samples across 12 effects classes, this code achieved 99.7% accuracy and an AUC of 0.9999. Specifically, 11 mistakes were made out of about 4000 testing examples; 6 of those were for the 'Phaser' effect, 3 were for EQ, a couple elsewhere, and most of the classes had zero mistakes. (No augmentation was used.)

<a href="url"><img src="http://i.imgur.com/nWHqAWy.png" width="400"></a>

This accuracy is comparable to the [original 2010 study by Stein et al.](http://www.ece.rochester.edu/courses/ECE472/resources/Papers/Stein_2010.pdf), who used a Support Vector Machine.

This was achieved by running for 10 hours on [our workstation with an NVIDIA GTX1080 GPU](https://pcpartpicker.com/b/4xLD4D). 

**Future Work**: So, the Stein et al. data was a great test case, and now we have confidence to apply this method to other datasets.  I just got a new audio dataset I want to try, but it's small and will probably require some augmentation.  And, this github repo and the code itself are still not "cleaned up" for public reading/usage. 

<hr>
-- [@drscotthawley](https://drscotthawley.github.io), March 2, 2017

PS- Thanks to [@WmHHooper](https://github.com/WmHHooper) for explaining what ROC & AUC mean.  I'm such a noob.
