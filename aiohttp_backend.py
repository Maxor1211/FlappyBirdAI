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


def real_or_fake(url=None, title=None, text=None):
	if title == None and text == None and url != None:
		(title, text) = get_article(url)
	elif title == None and text == None and url == None:
		raise ValueError("No URL or title or text provided. Can't proceed.")
	print(text_dataset_classifier.predict(title, text))


# # test cases
# url = "https://www.theonion.com/celebrities-explain-how-they-are-helping-ukraine-1848695261"
# title = "EU's Tusk says ready to ramp up sanctions against North Korea"
# text = "BRUSSELS (Reuters) - The European Union is prepared to ramp up sanctions against North Korea after it conducted its sixth and most powerful nuclear test on Sunday, European Council President Donald Tusk said.  The EU stands ready to sharpen its policy of sanctions and invites North Korea to restart dialogue on its programers without condition,  Tusk said in a statement.  We call on the UN Security Council to adopt further UN sanctions and show stronger resolve to achieve a peaceful decentralization of the Korean peninsula. The stakes are getting too high."
# real_or_fake(title=title, text=text)

routes = web.RouteTableDef()

@routes.get('/{slug}/{slug2}')
async def default_route(request):
	return web.json_response({'message':'Nothing is currently implemented. Come back later!'}, status=400)

@routes.get('/')
async def health(request):
	return web.Response(text="OK")

app = web.Application()
app.add_routes(routes)
web.run_app(app,port=3636)
