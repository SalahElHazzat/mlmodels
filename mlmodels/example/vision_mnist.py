# -*- coding: utf-8 -*-
"""mnist mlmodels .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17i0VyndXWDA2LlWqcb6Ad3d3Xl-do4T3
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Download and configuration"""

!git clone https://github.com/ahmed3bbas/mlmodels.git

!pip install numpy==1.17.5 pillow==6.2.1

cd mlmodels/

!git checkout vision

!pip install  git+https://github.com/arita37/mlmodels.git

!wget https://raw.githubusercontent.com/arita37/mlmodels/dev/install/requirements_fake.txt
!pip install -r install/requirements_fake.txt

!ls

!mkdir zwork && cd zwork

!ml_optim

"""# pretrained resnet18 on MNIST (torch)"""

# import library
import mlmodels
from mlmodels.models import module_load
from mlmodels.util import path_norm_dict, path_norm, params_json_load
from mlmodels.metrics import metrics_eval
from jsoncomment import JsonComment ; json = JsonComment()


#### Model URI and Config JSON
model_uri   = "model_tch.torchhub.py"
config_path = path_norm( 'dataset/json/benchmark_cnn/resnet18_benchmark_mnist.json'  )
config_mode = "test"  ### test/prod



#### Model Parameters
model_pars, data_pars, compute_pars, out_pars = params_json_load(config_path, config_mode= config_mode)
print( model_pars, data_pars, compute_pars, out_pars)

print('[INFO] model '+  model_pars['model']  + ' is training')

#### Setup Model 
module         = module_load( model_uri)
model          = module.Model(model_pars, data_pars, compute_pars) 

#### Fit
model, session = module.fit(model, data_pars, compute_pars, out_pars)           #### fit model
metrics_val    = module.fit_metrics(model, data_pars, compute_pars, out_pars)   #### Check fit metrics
print(metrics_val)


#### Inference
ypred          = module.predict(model, session, data_pars, compute_pars, out_pars)   
print(ypred)



#### Save/Load
module.save(model, save_pars ={ 'path': out_pars['path'] +"/model/"})

model2 = module.load(load_pars ={ 'path': out_pars['path'] +"/model/"})

"""# pretrained resnet34 on MNIST (torch)"""

# import library
import mlmodels
from mlmodels.models import module_load
from mlmodels.util import path_norm_dict, path_norm, params_json_load
from jsoncomment import JsonComment ; json = JsonComment()


#### Model URI and Config JSON
model_uri   = "model_tch.torchhub.py"
config_path = path_norm( 'dataset/json/benchmark_cnn/resnet34_benchmark_mnist.json'  )
config_mode = "test"  ### test/prod



#### Model Parameters
model_pars, data_pars, compute_pars, out_pars = params_json_load(config_path, config_mode= config_mode)
print( model_pars, data_pars, compute_pars, out_pars)

#### Setup Model 
module         = module_load( model_uri)
model          = module.Model(model_pars, data_pars, compute_pars) 

#### Fit
model, session = module.fit(model, data_pars, compute_pars, out_pars)           #### fit model
metrics_val    = module.fit_metrics(model, data_pars, compute_pars, out_pars)   #### Check fit metrics
print(metrics_val)


#### Inference
ypred          = module.predict(model, session, data_pars, compute_pars, out_pars)   
print(ypred)



#### Save/Load
module.save(model, save_pars ={ 'path': out_pars['path'] +"/model/"})

model2 = module.load(load_pars ={ 'path': out_pars['path'] +"/model/"})

"""# pretrained resnet50 on MNIST (torch)"""

# import library
import mlmodels
from mlmodels.models import module_load
from mlmodels.util import path_norm_dict, path_norm, params_json_load
from jsoncomment import JsonComment ; json = JsonComment()


#### Model URI and Config JSON
model_uri   = "model_tch.torchhub.py"
config_path = path_norm( 'dataset/json/benchmark_cnn/resnet50_benchmark_mnist.json'  )
config_mode = "test"  ### test/prod



#### Model Parameters
model_pars, data_pars, compute_pars, out_pars = params_json_load(config_path, config_mode= config_mode)
print( model_pars, data_pars, compute_pars, out_pars)

#### Setup Model 
module         = module_load( model_uri)
model          = module.Model(model_pars, data_pars, compute_pars) 

#### Fit
model, session = module.fit(model, data_pars, compute_pars, out_pars)           #### fit model
metrics_val    = module.fit_metrics(model, data_pars, compute_pars, out_pars)   #### Check fit metrics
print(metrics_val)


#### Inference
ypred          = module.predict(model, session, data_pars, compute_pars, out_pars)   
print(ypred)



#### Save/Load
module.save(model, save_pars ={ 'path': out_pars['path'] +"/model/"})

model2 = module.load(load_pars ={ 'path': out_pars['path'] +"/model/"})

"""# pretrined models"""

# import library
import mlmodels
from mlmodels.models import module_load
from mlmodels.util import path_norm_dict, path_norm, params_json_load
from mlmodels.metrics import metrics_eval
from jsoncomment import JsonComment ; json = JsonComment()


#### Model URI and Config JSON
model_uri   = "model_tch.torchhub.py"
config_path = path_norm( 'dataset/json/benchmark_cnn/resnet18_benchmark_mnist.json'  )
config_mode = "test"  ### test/prod



#### Model Parameters
model_pars, data_pars, compute_pars, out_pars = params_json_load(config_path, config_mode= config_mode)
print( model_pars, data_pars, compute_pars, out_pars)
model_pars =   {
                "model_uri": "model_tch.torchhub.py",
                "repo_uri": "pytorch/vision",
                "model": "resnet18",
                "num_classes": 10,
                "pretrained": 0,  "_comment": "0: False, 1: True",
                "num_layers": 5,
                "size": 6,
                "size_layer": 128,
                "output_size": 6,
                "timestep": 4,
                "epoch": 2
            }
models = ['alexnet', 'densenet121', 'densenet169', 'densenet201',
'densenet161', 'inception_v3', 'resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152',
'resnext50_32x4d', 'resnext101_32x8d', 'wide_resnet50_2', 'wide_resnet101_2', 'squeezenet1_0',
'squeezenet1_1', 'vgg11', 'vgg13', 'vgg16', 'vgg19', 'vgg11_bn', 'vgg13_bn', 'vgg16_bn', 'vgg19_bn',
'googlenet', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0', 'mobilenet_v2']

valid_models =  ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152',
'resnext50_32x4d', 'resnext101_32x8d', 'wide_resnet50_2', 'wide_resnet101_2', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0']
#yes
#'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0','wide_resnet101_2'
#no
#'mobilenet_v2','googlenet','vgg*','squeezenet1_1','alexnet','densenet','inception_v3'

#errors 
#'GoogLeNetOutputs' object has no attribute 'log_softmax'
#'VGG' object has no attribute 'fc'
#'SqueezeNet' object has no attribute 'fc'
#'AlexNet' object has no attribute 'fc'
#'DenseNet' object has no attribute 'fc'
# Calculated padded input size per channel: (1 x 1). Kernel size: (3 x 3). Kernel size can't be greater than actual input size

for model_name in valid_models:
    print('[INFO] model '+  model_name + ' is training')
    
    model_pars['model'] = model_name
    out_pars = {
                    "checkpointdir": "ztest/model_tch/torchhub/"+ model_pars['model'] +"/checkpoints/",
                    "path": "ztest/model_tch/torchhub/"+ model_pars['model'] +"/"
                }

    #### Setup Model 
    module         = module_load( model_uri)
    model          = module.Model(model_pars, data_pars, compute_pars) 

    #### Fit
    model, session = module.fit(model, data_pars, compute_pars, out_pars)           #### fit model
    metrics_val    = module.fit_metrics(model, data_pars, compute_pars, out_pars)   #### Check fit metrics
    print(metrics_val)


    #### Inference
    ypred          = module.predict(model, session, data_pars, compute_pars, out_pars)   
    print(ypred)



    #### Save/Load
    module.save(model, save_pars ={ 'path': out_pars['path'] +"/model/"})

    model2 = module.load(load_pars ={ 'path': out_pars['path'] +"/model/"})