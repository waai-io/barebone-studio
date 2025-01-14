from fastapi import APIRouter
from fastapi.responses import FileResponse

import shutil
from glob import glob

from studio.api.dir_path import DIRPATH
from studio.api.utils.filepath_creater import join_filepath
from studio.api.experiment.experiment_reader import ExptConfigReader
from studio.routers.model import DeleteItem

router = APIRouter()


@router.get("/experiments")
async def get_experiments():
    exp_config = {}
    config_paths = glob(join_filepath([DIRPATH.OUTPUT_DIR, "*", DIRPATH.EXPERIMENT_YML]))
    for path in config_paths:
        try:
            config = ExptConfigReader.read(path)
            config.nodeDict = []
            config.edgeDict = []
            exp_config[config.unique_id] = config
        except Exception as e:
            pass

    return exp_config


@router.get("/experiments/import/{unique_id}")
async def import_experiment(unique_id: str):
    config = ExptConfigReader.read(join_filepath([
        DIRPATH.OUTPUT_DIR,
        unique_id,
        DIRPATH.EXPERIMENT_YML
    ]))
    return {
        "nodeDict": config.nodeDict,
        "edgeDict": config.edgeDict,
    }


@router.delete("/experiments/{unique_id}")
async def delete_experiment(unique_id: str):
    try:
        shutil.rmtree(join_filepath([DIRPATH.OUTPUT_DIR, unique_id]))
        return True
    except Exception as e:
        return False


@router.post("/experiments/delete")
async def delete_experiment_list(deleteItem: DeleteItem):
    try:
        [
            shutil.rmtree(join_filepath([DIRPATH.OUTPUT_DIR, uid]))
            for uid in deleteItem.uidList
        ]
        return True
    except Exception as e:
        return False


@router.get("/experiments/download/nwb/{unique_id}")
async def download_nwb_experiment(unique_id: str):
    nwb_path_list = glob(join_filepath([
        DIRPATH.OUTPUT_DIR,
        unique_id,
        "*.nwb"
    ]))
    if len(nwb_path_list) > 0:
        return FileResponse(nwb_path_list[0])
    else:
        return False


@router.get("/experiments/download/nwb/{unique_id}/{function_id}")
async def download_nwb_experiment(unique_id: str, function_id: str):
    nwb_path_list = glob(join_filepath([
        DIRPATH.OUTPUT_DIR,
        unique_id,
        function_id,
        "*.nwb"
    ]))
    if len(nwb_path_list) > 0:
        return FileResponse(nwb_path_list[0])
    else:
        return False


@router.get("/experiments/download/config/{unique_id}")
async def download_config_experiment(unique_id: str):
    config_filepath = join_filepath([
        DIRPATH.OUTPUT_DIR,
        unique_id,
        DIRPATH.SNAKEMAKE_CONFIG_YML
    ])
    return FileResponse(config_filepath)
