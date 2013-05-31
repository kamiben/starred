import datetime
		
class Item(object):
	def __init__(self, item):
		self.title = item['title'].encode("utf-8")
		self.url = self.get_starred_url(item)
		self.content = self.get_content(item)
		self.datestamp = item['published']
		self.date = datetime.datetime.fromtimestamp(self.datestamp).strftime('%m-%Y')
		
	def genstring_web(self):
		formed_url = "{1}  <small><a href=\"{0}\">Direct link</a></small></br>\n".format(self.url, self.title)
		# Need to implement Lazy load before being able to add the content to the main page.
		#http://twitter.github.io/bootstrap/javascript.html#collapse
		#http://antjanus.com/blog/web-design-tips/user-interface-usability/customize-twitter-bootstrap-into-themes/
		#https://github.com/twitter/bootstrap/issues/5796
		#formed_url += "<div id=\"demo\" class=\"collapse\"> {0} </div>".format(self.content)
		return formed_url
		
	def genstring_csv(self):
		date = datetime.datetime.fromtimestamp(self.datestamp).strftime('%Y-%m-%d %H:%M:%S')
		return [self.title, self.url, date]
	
	def get_starred_url(self, item):
		# error handling in case canonical is not defined for the specific element
		try:
			return item['canonical'][0]['href'].encode("utf-8")
			
		except KeyError:
			return item['alternate'][0]['href'].encode("utf-8")
			
	def get_content(self, item):
		# error handling in case the content is not defined and is in summary instead	
		try:
			return item['content']['content'].encode("utf-8")
			
		except KeyError:
			return item['summary']['content'].encode("utf-8")
		
		
class ItemList(object):
	def __init__(self):
		self.list = []
		
	def add(self, item):
		self.list.append(item)
	
	def date_equal(self, item, date):
		# check if date is equal to item.date, returns true or false. For usage in grab_date
		return item.date == date
	
	def grab_date(self, date):
		# Filter the Item list with the provided date (date_equal = true)
		# Returns an array of items
		return [ x for x in self.list if self.date_equal(x, date) ]