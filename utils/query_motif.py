import os
import subprocess
import numpy as np
import pandas as pd

def path_to_image_html(best_model):
    """ Finds the file path to the motif image that corresponds to the queried TF
    """
    return '<img src="static/images/motifs/'+ best_model + '" style="max-height:100px;"/>'

def get_motif(input_chrom, input_loc):
    """ Queries the positionally-relevant motifs from Jeff Vierstra's database
        given a chromosome and location. Exports a pandas dataframe in html format
        with TFs sorted by 'match_score' (how well the TF binds at the site)

        @Joel - you can save the data from the pandas dataframe 'motifs' probably
        where I commented out "print(motifs)" but any of the stages work (whatever
        is more efficient for you).
    """

    # create header for the table
    motifs_main = pd.DataFrame(columns = ['chromosome', 'start', 'end', 'motif_cluster', 'match_score', 'strand', 'best_model', 'num_models'])

    # call the shell that queries motifs from the database
    subprocess.call(['sh', 'utils/query_motif.sh', '-c', input_chrom, '-l', input_loc])

    # load motifs from the text file generated by the shell script
    motifs=pd.read_csv('static/text/motifs.txt', sep='\t', header=None, names=['chromosome', 'start', 'end', 'motif_cluster', 'match_score', 'strand', 'best_model', 'num_models']) #../
    motifs = motifs.sort_values(by=['match_score'], ascending=False)
    
    # print(motifs)
    
    # find the image filepath
    motifs['image'] = motifs['best_model'] + '.png'
    # limit motifs to only the most relevant TFs
    motifs = motifs[motifs['match_score'] > 8]
    motifs_main = motifs_main.append(motifs)

    # construct the html string to display to the user
    html_string = '''
    <html>
    <head><title>HTML Motifs Dataframe with CSS</title></head>
    <link rel="stylesheet" type="text/css" href="/static/css/df_style.css"/>
    <body>
        {table}
    </body>
    </html>
    '''
    s = html_string.format(table=motifs_main.to_html(classes='mystyle', escape=False, formatters=dict(image=path_to_image_html), index=False))
    return s