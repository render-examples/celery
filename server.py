import aiohttp
import asyncio
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles
from simpletransformers.classification import ClassificationModel
import zipfile

export_file_url = 'https://www.dropbox.com/s/bgljpmn90u7v91n/model_files.zip?raw=1'
export_file_name = 'model_files.zip'

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])


async def download_file(url, dest):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_model():
    await download_file(export_file_url, export_file_name)
    args = {'use_multiprocessing': False, 'no_cache': True, 'use_cached_eval_features': False,
            'reprocess_input_data': True, 'silent': True}
    zipfile.ZipFile('model_files.zip').extractall()
    model = ClassificationModel('roberta', 'model_files/', use_cuda=False, args=args)
    return model


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_model())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

label_mapping = {"0": 0, "1": 1}


@app.route('/predict', methods=['POST'])
async def predict(request):
    data = await request.json()['data']

    instances = model.predict(data)[1].tolist()

    results = []
    for i, instance_scores in enumerate(instances):

        predictions = []
        for j, score in enumerate(instance_scores):
            predictions.append({'class': label_mapping[str(j)], 'score': score})
        predictions = sorted(predictions, key=lambda k: k['score'], reverse=True)

        results.append({'text': data[i], 'predictions': predictions})

    return UJSONResponse({'results': results})


# @app.route('/bulk-predict', methods=['POST'])
# async def analyze(request):
#     img_data = await request.form()
#     img_bytes = await (img_data['file'].read())
#     img = open_image(BytesIO(img_bytes))
#     prediction = learn.predict(img)[0]
#     return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
