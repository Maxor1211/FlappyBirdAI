import functools
from aiohttp import web
from newspaper import Article
from train import create_classifiers
from pathlib import Path

text_dataset_classifier = create_classifiers()


def retrain_dtree(criterion="entropy", max_depth=12, min_samples_leaf=40):
	pass


def retrain_cnb():
	pass


def retrain_mnb():
	pass


def retrain_knn():
	pass


def retrain_svm():
	pass


def get_article(url):
	article = Article(url)
	article.download()
	article.parse()
	return [article.title, article.text]


def real_or_fake(url=None, title=None, text=None, classifiers=[0]):
	if title == None and text == None and url != None:
		(title, text) = get_article(url)
	elif title == None and text == None and url == None:
		raise ValueError("No URL or title or text provided. Can't proceed.")
	result = int( text_dataset_classifier.predict(title, text)[0].item(0))
	if result == 0:
		result = "FAKE"
	else:
		result = "REAL"
	return [title, result]


# # test cases
# url = "https://www.theonion.com/celebrities-explain-how-they-are-helping-ukraine-1848695261" #this returns fake
# title = "EU's Tusk says ready to ramp up sanctions against North Korea"
# text = "BRUSSELS (Reuters) - The European Union is prepared to ramp up sanctions against North Korea after it conducted its sixth and most powerful nuclear test on Sunday, European Council President Donald Tusk said.  The EU stands ready to sharpen its policy of sanctions and invites North Korea to restart dialogue on its programers without condition,  Tusk said in a statement.  We call on the UN Security Council to adopt further UN sanctions and show stronger resolve to achieve a peaceful decentralization of the Korean peninsula. The stakes are getting too high."
# the above is from the real dataset, so it returns true, mostly
#  real_or_fake(title=title, text=text)

routes = web.RouteTableDef()
app = web.Application()


@routes.post("/{classifiers}/{article_url}")
async def default_route(request):
	data = await request.json()
	print(data)
	classifiers = []
	for classifier in data:
		if classifier.get("id", -1) != -1 and classifier.get("active", False) == True:
			classifiers.append(classifier.get("id", -1))
	(title,result) = await app.loop.run_in_executor(
		None,
		functools.partial(
			real_or_fake, url=request.match_info["article_url"], classifiers=classifiers
		),
	)
	print(result)
	return web.json_response(
		{"result": result, "title": title}, status=200
	)

@routes.get("/")
async def health(request):
	return web.Response(text="OK")


app.add_routes(routes)
web.run_app(app, port=3636)
