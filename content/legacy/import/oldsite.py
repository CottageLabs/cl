import requests, os, json, codecs

pad = "http://pads.cottagelabs.com/p/"
suffix = "/export/txt"

def metadata(js):
	author = js.get("author")
	created_date = js.get("created_date")
	last_updated = js.get("last_updated")
	tags = js.get("tags", [])
	title = js.get("title")

	md = ""
	if title is not None:
		md += "Original Title: " + title + "\n"
	if author is not None:
		md += "Original Author: " + author + "\n"
	if len(tags) > 0:
		md += "Tags: " + ", ".join(tags) + "\n"
	if created_date is not None:
		md += "Created: " + created_date + "\n"
	if last_updated is not None:
		md += "Last Modified: " + last_updated + "\n"
	
	return md


def do_page(js):
	id = js.get("id")
	print id
	
	resp = requests.get(pad + id + suffix)
	
	visible = js.get("visible", False)
	url = js.get("url")
	url = url[1:]
	bits = url.split("/")
	bits[-1] = bits[-1] + ".md"
	if visible:
		bits.insert(0, "public")
	else:
		bits.insert(0, "private")
	path = os.path.join("pages", *bits)
		
	try:
		os.makedirs(os.path.join("pages", *bits[:-1]))
	except OSError:
		pass
	
	out = codecs.open(path, "wb", "utf-8")
	out.write(resp.text)
	out.write("\n\n")

	md = metadata(js)
	out.write(md)
	out.close()

def do_all():
	f = codecs.open("index.json", "rb", "utf-8")
	cont = f.read()
	objects = cont.split("}\n{")

	objects = [x.strip() + "}" if not x.strip().endswith("}") else x for x in objects]
	objects = ["{" + x if not x.startswith("{") else x for x in objects]
	js = [json.loads(x) for x in objects]

	for j in js:
		do_page(j)

do_all()
