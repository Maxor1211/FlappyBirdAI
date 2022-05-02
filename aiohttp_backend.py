import functools, asyncio
from json import JSONDecodeError
from aiohttp import web
from newspaper import Article
from train import create_classifiers
from pathlib import Path

text_dataset_classifier = create_classifiers()


def get_article(url):
	article = Article(url)
	article.download()
	article.parse()
	return [article.title, article.text]


def real_or_fake(url=None, title=None, text=None, classifiers=[0], train_req=None):
	if title == None and text == None and url != None:
		(title, text) = get_article(url)
	elif title == None and text == None and url == None:
		raise ValueError("No URL or title or text provided. Can't proceed.")
	for item in train_req:
		id = item.get("id",-1)
		opts = item.get("options", {})
		if id in classifiers:
			if id == 0:
				clfer = (0, opts.get("criterion","entropy"), opts.get("max_depth",5), opts.get("min_samples_leaf",1000), opts.get("min_samples_split",1000) )
			elif id == 1:
				clfer = (1, opts.get("type","multinomial"), opts.get("alpha",0.5) )
			elif id == 2:
				clfer = (2, opts.get("k_neighbours",4), opts.get("weight","uniform"), opts.get("power", 2) )
			elif id == 3:
				clfer = (3, opts.get("param_c", 1), opts.get("kernel","linear"), opts.get("degree",2) )
			text_dataset_classifier.train(classifier=clfer)
	return_results = {}
	results = text_dataset_classifier.predict(title, text, classifiers)
	for i in range(len(results)):
		return_results[classifiers[i]] = int(results[i].item(0))
	for i in [0, 1, 2, 3]:
		if return_results.get(i, None) == None:
			return_results[i] = -1
	return [title, return_results]


routes = web.RouteTableDef()
app = web.Application()


@routes.post("/predict")
async def default_route(request):
	try:
		data = await request.json()
	except JSONDecodeError:
		return web.json_response({"message": "Malformed request"}, status=400)
	print(data)
	request_url = data.get("request_url", "")
	classifiers = []
	for classifier in data.get("classifiers", []):
		if classifier.get("id", -1) != -1 and classifier.get("active", False) == True:
			classifiers.append(classifier.get("id", -1))
	print(classifiers)
	try:
		(title, results) = await asyncio.wait_for(asyncio.shield(asyncio.get_running_loop().run_in_executor(
			None,
			functools.partial(real_or_fake, url=request_url, classifiers=classifiers, train_req=data.get("classifiers", [])),
		)),timeout=80)
	except asyncio.TimeoutError:
		return web.json_response(
			{"status": "scheduled"},
			status=200,
		)
	print(request_url, results)
	return web.json_response(
		{
			"status": "processed",
			"result": results,
			"title": title,
			"request_url": request_url,
			"request": data.get("classifiers", []),
			"stats": [],
		},
		status=200,
	)
		


@routes.get("/")
async def health(request):
	return web.Response(text="OK")


app.add_routes(routes)
web.run_app(app, port=3636)
