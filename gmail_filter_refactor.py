class Property(object):
	def __init__(self, name, value, category):
		self.name = name
		self.value = value
		self.category = category

	def __eq__(self, other):
		equals = None
		# They must both be of class Property
		equals = isinstance(other, self.__class__)
		equals = equals and (self.name == other.name)
		equals = equals and (self.category == other.category)
		# If it's a condition, the values must equal each other, but otherwise, it doesn't matter
		if self.category is "condition":
			equals = equals and (self.value == other.value)

		return equals

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "\nName: %s, Value: %s, Category: %s" % (self.name, self.value, self.category)

	def __repr__(self):
		return "\nName: %s, Value: %s, Category: %s" % (self.name, self.value, self.category)

class Filter(object):
	def __init__(self, filter_name):
		self.filter_name = filter_name
		self.properties = []

	def addProperty(self, new_prop):
		self.properties.append(new_prop)


	def __eq__(self, other):
		equals = None
		self.properties.sort()
		other.properties.sort()
		equals = len(self.properties) == len(other.properties)
		for index, prop in enumerate(self.properties):
			equals = equals and (prop == other.properties[index])
			if equals is False:
				break

		return equals

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "Filter Name: %s\nProperties:\n%s\n\n" % (self.filter_name, self.properties)

	def __repr__(self):
		return "Filter Name: %s\nProperties:\n%s\n\n" % (self.filter_name, self.properties)


import lxml.etree
from itertools import combinations
feed_url = 'http://earthquake.usgs.gov/earthquakes/catalogs/1hour-M1.xml'
ns = {
	'atom': 'http://www.w3.org/2005/Atom',
	'apps': 'http://schemas.google.com/apps/2006'
}
actions = [
	'shouldArchive',
	'shouldMarkAsRead',
	'shouldStar',
	'label',
	'forwardTo',
	'shouldTrash',
	'neverSpam'
]

conditions = {
	'from',
	'to',
	'subject',
	'hasTheWord',
	'doesNotHaveTheWord',
	'hasAttachment'
}

def main():
	filters = []
	new_filters = []
	doc = lxml.etree.parse('mailFilters.xml')
	for entry in doc.xpath('//atom:entry', namespaces=ns):
		[title] = entry.xpath('./atom:title', namespaces=ns)
		if title.text == "Mail Filter":
			[category] = entry.xpath('./atom:category', namespaces=ns)
			[id] = entry.xpath('./atom:id', namespaces=ns)
			[updated] = entry.xpath('./atom:updated', namespaces=ns)
			[content] = entry.xpath('./atom:content', namespaces=ns)
			this_filter = Filter(filter_name=title.text)
			for property in list(entry.xpath('./apps:property', namespaces=ns)):
				name = property.get("name")
				value = property.get("value")
				if name in actions:
					category = 'action'
				elif name in conditions:
					category = 'condition'	
				else:
					# TODO - should I skip the unknown ones?
					category = 'unknown'
					continue
				this_filter.addProperty(Property(name=name, value=value, category=category))
			filters.append(this_filter)
	filter_len = len(filters)
	for index, filter in enumerate(filters):
		if len(new_filters) is 0:
			new_filters.append([filter])
		found = False
		for i, this_filter_list in enumerate(new_filters):
			if this_filter_list[0] == filter:
				found = True
				new_filters[i].append(filter)
				# TODO - remove me
				break

		if not found:
			new_filters.append([filter])

	for new_filter_group in new_filters:
		print len(new_filter_group)

# If actions are the same and filters are the same...

if __name__ == '__main__':
	main()