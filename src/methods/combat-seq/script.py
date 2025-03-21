import sys

import anndata as ad
import numpy as np
from inmoose.pycombat import pycombat_seq
from scipy.sparse import csr_matrix

# VIASH START
# Note: this section is auto-generated by viash at runtime. To edit it, make changes
# in config.vsh.yaml and then run `viash config inject config.vsh.yaml`.
par = {"input": "resources_test/.../input.h5ad", "output": "output.h5ad"}
meta = {"name": "combat-seq"}
# VIASH END

sys.path.append(meta["resources_dir"])
from read_anndata_partial import read_anndata

print("Read input", flush=True)
adata = read_anndata(
    par["input"], X="layers/normalized", obs="obs", var="var", uns="uns"
)

print("Run Combat-Seq", flush=True)
counts = adata.T.to_df().astype(np.double).values
corrected_counts = pycombat_seq(adata.X, adata.obs["batch"])

print("Store output", flush=True)
output = ad.AnnData(
    obs=adata.obs[[]],
    var=adata.var[[]],
    uns={
        "dataset_id": adata.uns["dataset_id"],
        "normalization_id": adata.uns["normalization_id"],
        "method_id": meta["name"],
    },
    layers={
        "corrected_counts": csr_matrix(corrected_counts.T),
    },
)

print("Store outputs", flush=True)
output.write_h5ad(par["output"], compression="gzip")
