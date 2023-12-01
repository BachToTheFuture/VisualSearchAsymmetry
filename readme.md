# Visual Search Asymmetry: Deep Nets and Humans Share Similar Inherent Biases
This repository contains an implementation of our paper published in NeurIPS 2021 [[1](#cite_vsa)][[NeurIPS][neurips]]. The video presentation can be viewable [HERE (MIT CBMM)](https://www.youtube.com/watch?v=pA_sTT3ii9Y&t=724s) and [HERE (NeurIPS)](https://slideslive.com/38966964/visual-search-asymmetry-deep-nets-and-humans-share-similar-inherent-biases). The poster is available [HERE](https://d2b38104-6cb6-430b-95b9-765197711bda.usrfiles.com/ugd/d2b381_772a90ce15ce4c6ca91a3310b42a6563.pdf).

It contains all the code required to reproduce the results shown in our paper. To make things simple we have provided several bash scripts that can be directly used to run the specified models to produce results shown in the paper. If you want to evaluate different parts of the model individually, use the notebook file `runExp.ipynb` inside the `vs_exp/eccNET`directory.

## Paper Abstract
Visual search is a ubiquitous and often challenging daily task, exemplified by looking for the car keys at home or a friend in a crowd. An intriguing property of some classical search tasks is an asymmetry such that finding a target A among distractors B can be easier than finding B among A. To elucidate the mechanisms responsible for asymmetry in visual search, we propose a computational model that takes a target and a search image as inputs and produces a sequence of eye movements until the target is found. The model integrates eccentricity-dependent visual recognition with target-dependent top-down cues. We compared the model against human behavior in six paradigmatic search tasks that show asymmetry in humans. Without prior exposure to the stimuli or task-specific training, the model provides a plausible mechanism for search asymmetry. We hypothesized that the polarity of search asymmetry arises from experience with the natural environment. We tested this hypothesis by training the model on augmented versions of ImageNet where the biases of natural images were either removed or reversed. The polarity of search asymmetry disappeared or was altered depending on the training protocol. This study highlights how classical perceptual properties can emerge in neural network models, without the need for task-specific training, but rather as a consequence of the statistical properties of the developmental diet fed to the model.


## Reproducing Results From NeurIPS Paper

### Environment Preparation

First of all you will need to prepare your environment to run these codes. Make sure you have Ananconda installed on your machine, if you do not have you can follow the instruction from [here](https://docs.anaconda.com/anaconda/install/) to install it. Anaconda will be used to create a virtual environment with all the packages and dependencies which are used in our code. Note that these scripts were tested on **Ubuntu System**, make sure to make necessary changes if you are trying to run it on any other system

We have provided a `prepDirectory.sh` bash script for you to quickly prepare your environment. Run the following commands:

```
bash prepDirectory.sh
```

The above script will download all the experiment datasets, pre-trained weights, and GBVS models from a dropbox link. The script will automatically place them at the relevant directory location. Next, the script will create an anaconda environment with all the required packages with the name `vsa_nips_klab`.

Once, the directory is prepared activate the conda environment by running `conda activate vsa_nips_klab`.

### Running Visual Search Experiments

**To run the experiment using the *eccNET* model. Run the following command:**

```
bash runExp_eccNET.sh
```

This will perform all the visual asymmetry search experiments using our proposed eccNET model. It takes 28 mins to run all the experiments on a single NVIDIA GeForce RTX 2080 Ti Rev. A (11GB) GPU. The predicted files will be saved in: `./vs_exp/eccNET/out/eccNET`

**To run the experiment using the ablation model. Run the following command:**

```
bash runExp_ablation.sh
```

This will perform all the visual asymmetry search experiments using all the ablated models in Fig5B in the texts (except the GBVS model which requires you to run in Matlab). It takes 2 hours and 15 mins to run all the experiments on a single NVIDIA GeForce RTX 2080 Ti Rev. A (11GB) GPU. The predicted files will be saved in: `./vs_exp/eccNET/out/MODEL_NAME` for DL based models. For chance, the files will be saved in: `./vs_exp/chance` and pixelMatch will be saved in: `./vs_exp/pixelMatch`. Note model name eccNET_0_0_1 is the model eccNET_18-->17.

**To run the experiments using GBVS:**
Go to the following directory: `vs_exp/gbvs/` and open `visual_search.m` in MATLAB and run. The predictions will be save inside: `vs_exp/gbvs/out_data`. This can take a significant amount of time, the GBVS package does not support GPU. It approximately took ~12 hours for us to run all the experiments on Intel® Core™ i7-8565U CPU with 8 GB of RAM.

### Producing the results and figures from the predictions generated by the models

Note that the repository already contains all the predicted files so that you do not necessarily need to run all the models to generate predictions. Again you can either use the relevant `ipynb` notebook files inside the `vs_exp` directory or simply run the bashscript provided by us to generate all the results and figures.

```
bash generateResults.sh
```

The above code will generate all the figures and plots inside the `vs_exp/results`

### Producing results for additional experiments shown in supplementary

Various other experiemnts were also conducted during the rebuttal period. Results from those expeirments are included in our supplementary figures. To generate those results we have provided extra bash files. For those experiments, there's a need to download additional datasets and model files. Kindly follow the below steps to replicate those results:

Run the below command to download additional files and prepare your conda environment `vsa_nips_klab` to support some additional packages used to calculate Scanpath Similarity scores. This may take significant amount of time as the package for calculating Scanpath Similarity scores also installs matlab runtime library.

```
bash prepDirectoryAdditionalExp.sh
```

**Experiments to evaluate the effect of "training regime"**

To replicate the results from experiments done to study the role of training regime (**Figure S10-13**).

To perform the search task use the below command. This will take approximately 2-3 hours. The model predictions will be saved in `./vs_exp/eccNET/out_aug/MODEL_NAME`. Note that the predictions are already saved inside the `./vs_exp/eccNET/out_aug/` for reference.

```
bash runExp_augment.sh
```

Finally to produce the RT plots shown in **Figure S10-13** run the below command.

```
bash generateAugmentResults.sh
```

**Experiments to compare human fixations in visual search**

To replicate the results from experiments done to study human fixations in visual search and compare scanpath score, saccade distributions of eccNET vs Humans (**Figure S16-18**).

To perform the search task use the below command. This will take approximately 3 hours. The model predictions will be saved in `./vs_saccade_exp/eccNET/out/EXP_NAME/`. Note that the predictions are already saved inside the `./vs_saccade_exp/eccNET/out/` for reference.

```
bash runExp_saccade.sh
```

Finally to produce different subplots shown in **Figure S16-13** run the below command.

```
bash generateSaccadeResults.sh
```


## Training/Finetuning eccNET

Training/Finetuning of eccNET architecture on classification tasks can be done using the following python script: `vgg16_training/train_eccnet_imagenet.py`. The checkpoints for our finetuning experiment for eccNET is available [here](https://huggingface.co/shashikg/visual_search_klab/tree/main/checkpoints/eccNET).


## Training on Augmented Imagenet

Training on augmented imagenet to study the role of training regime can be done using the following python script: `vgg16_training/train_vgg16_imagenet.py`. The checkpoints for our training experiment is available [here](https://huggingface.co/shashikg/visual_search_klab/tree/main/checkpoints/AsymmetryAugmentedVGG16). To generate the augmented imagenet data use the notebooks available here: [extras/imagenet_asymmetry_augmentation](extras/imagenet_asymmetry_augmentation)


## Generating Additional Stimuli

We used the scripts available here: [extras/experiment_stimuli_generators](extras/experiment_stimuli_generators) to generate the asymmetry experiment stimuli. These can be used to used generate additional stimuli with different configuration for further studies. Please refer to our supplementary material for the configuration used in our paper.


## Citation

<a name="cite_vsa"></a> Shashi Kant Gupta, Mengmi Zhang, Chia-Chien Wu, Jeremy M. Wolfe, & Gabriel Kreiman (2021). Visual Search Asymmetry: Deep Nets and Humans Share Similar Inherent Biases. In Thirty-Fifth Conference on Neural Information Processing Systems. [[NeurIPS][neurips]] [[arXiv][arxiv]]

[//]: #
[arxiv]: <https://arxiv.org/abs/2106.02953>
[neurips]: <https://proceedings.neurips.cc/paper_files/paper/2021/hash/37f0e884fbad9667e38940169d0a3c95-Abstract.html>
