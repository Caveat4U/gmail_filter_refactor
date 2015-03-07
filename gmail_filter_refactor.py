# from defusedxml.ElementTree import parse

# tree = parse('mailFilters.xml')
# root = tree.getroot()
# print root.findall('entry')
# print tree.findall('entry')

# for entry in root.getchildren():
# 	print entry.tag


# # 		<category term='filter'></category>
# # 		<title>Mail Filter</title>
# # 		<id>tag:mail.google.com,2008:filter:1266219424336</id>
# # 		<updated>2015-03-07T19:30:11Z</updated>
# # 		<content></content>
# # 		<apps:property name='hasTheWord' value='@facebookmail.com OR @honestybox.com'/>
# # 		<apps:property name='label' value='Facebook'/>
# # 		<apps:property name='shouldArchive' value='true'/>
# for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
# 	print entry.getchildren()
# 	print entry.get('category')



# # build a tree structure
# root = ET.Element("html")

# head = ET.SubElement(root, "head")

# title = ET.SubElement(head, "title")
# title.text = "Page Title"

# body = ET.SubElement(root, "body")
# body.set("bgcolor", "#ffffff")

# body.text = "Hello, World!"

# # wrap it in an ElementTree instance, and save as XML
# tree = ET.ElementTree(root)
# #print tree
# #tree.write("page.xhtml")

import lxml.etree

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

filters = {
	'from',
	'to',
	'subject',
	'hasTheWord',
	'doesNotHaveTheWord',
	'hasAttachment'
}

def main():
    doc = lxml.etree.parse('mailFilters.xml')
    for entry in doc.xpath('//atom:entry', namespaces=ns):
        [title] = entry.xpath('./atom:title', namespaces=ns)
        if title.text == "Mail Filter":
        	[category] = entry.xpath('./atom:category', namespaces=ns)
        	[id] = entry.xpath('./atom:id', namespaces=ns)
        	[updated] = entry.xpath('./atom:updated', namespaces=ns)
        	[content] = entry.xpath('./atom:content', namespaces=ns)
        	for property in list(entry.xpath('./apps:property', namespaces=ns)):
        		name = property.get("name")
        		value = property.get("value")
        		if name in actions:
        			category = 'actions'
        		elif name in filters:
        			category = 'filters'
        		else:
        			#print "Warning - Unknown property type '%s'." % name
        			category = 'unknown'

# If actions are the same and filters are the same...

if __name__ == '__main__':
    main()