import string

class Render (object):

	def __init__(self):
		# Load the template once
		with open('template.html') as template_model:
			template = string.Template(template_model.read())
		self.template = template
		
	def render_index(self, content):
		# In: A list, will join it with line returns and apply the template.
		output = {'content':'\n'.join(content)}
		result = self.template.substitute(output)
		return result
		
	def render_article(self, content):
		# In: A string, just apply the template.
		output = {'content':content}
		result = self.template.substitute(output)
		return result