import sys
sys.path.append("..")

import numpy as np
np.seterr(divide="ignore")

import logging
import os
import pickle
import torch


from architectures.recursive_net import GRNNTransformSimple
from architectures.relation_net import RelNNTransformConnected
from architectures.message_net import MPNNTransform
from architectures.predict import PredictFromParticleEmbedding
from architectures.preprocessing import wrap, unwrap, wrap_X, unwrap_X

from scipy import interp
from loading import load_model


def evaluate_models(X, y, w, model_filenames, batch_size=64):

    for filename in model_filenames:
        if 'DS_Store' not in filename:
            model = load_model(filename)
            work = True
            if work:
                model.eval()

                offset = 0
                y_pred = []
                n_batches, remainder = np.divmod(len(X), batch_size)
                for i in range(n_batches):
                    X_batch = X[offset:offset+batch_size]
                    X_var = wrap_X(X_batch)
                    y_pred.append(unwrap(model(X_var)))
                    unwrap_X(X_var)
                    offset+=batch_size
                if remainder > 0:
                    X_batch = X[-remainder:]
                    X_var = wrap_X(X_batch)
                    y_pred.append(unwrap(model(X_var)))
                    unwrap_X(X_var)
                y_pred = np.squeeze(np.concatenate(y_pred, 0), 1)
                
    return y, y_pred

def get_prediction(data, model_path, batch_size):
    X, y, w = data
    model_filenames = [os.path.join(model_path, fn) for fn in os.listdir(model_path)]
    y, y_pred = evaluate_models(X, y, w, model_filenames, batch_size)

    return y, y_pred

def main():
    pass

if __name__ == '__main__':
    main()