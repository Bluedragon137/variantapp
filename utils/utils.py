from basepairmodels.cli.shap import shap_scores
import numpy as np
from numpy.core.fromnumeric import _shape_dispatcher
import pandas as pd
import subprocess
import tensorflow as tf
import time

from utils.load_model import load
from utils.query_variant import query_rsID, query_values
from utils.gen_prediction import predict_main
from utils.gen_shap import shap_scores_main
from utils.query_motif import get_motifs

def generate_output_values(cell_type, chrom, position, effect_allele, noneffect_allele):
    subprocess.call(['sh' ,'scripts/reset.sh'])
    model = load(cell_type)
    peaks_df = query_values(chrom, position, effect_allele, noneffect_allele)
    predict_main(model, peaks_df)
    shap_scores_main(model, peaks_df)
    get_motifs(peaks_df['chrom'][0], peaks_df['st'])

def generate_output_rsID(cell_type, rsID):
    subprocess.call(['sh' ,'scripts/reset.sh'])
    model = load(cell_type)
    peaks_df = query_rsID(rsID)
    predict_main(model, peaks_df)
    shap_scores_main(model, peaks_df)
    get_motifs(peaks_df.iloc[0]['chrom'], peaks_df.iloc[0]['st'])

if __name__ == '__main__':
    #generate_output_values('abc', 'chr1', 35641660, 'A', 'G')
    generate_output_rsID('C24', 'rs181391313')
