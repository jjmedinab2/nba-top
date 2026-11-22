import urllib.request
import xml.etree.ElementTree as ET
import re
from html import escape

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCWJ2lWNubArHWmf3FIHbfcQ"

req = urllib.request.Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
xml_data = urllib.request.urlopen(req).read()
root = ET.fromstring(xml_data)

ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'media': 'http://search.yahoo.com/mrss/'
}

items = []
for entry in root.findall('atom:entry', ns):
    title = entry.find('atom:title', ns).text or ""
    video_id = entry.find('yt:videoId', ns).text
    link = entry.find('atom:link', ns).attrib['href']
    published = entry.find('atom:published', ns).text
    
    media_group = entry.find('media:group', ns)
    desc_el = media_group.find('media:description', ns) if media_group is not None else None
    desc = desc_el.text if desc_el is not None and desc_el.text else ""

    if re.search(r'\btop\b', title, re.IGNORECASE) or re.search(r'\btop\b', desc, re.IGNORECASE):
        img_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        contenido_html = f'<img src="{img_url}" /><br><br>{escape(desc).replace(chr(10), "<br>")}'
        
        items.append(f"""
        <entry>
            <id>yt:video:{video_id}</id>
            <title>{escape(title)}</title>
            <link href="{link}"/>
            <published>{published}</published>
            <updated>{published}</updated>
            <content type="html">{escape(contenido_html)}</content>
        </entry>""")

feed_final = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="{'http://' + 'www.w3.org' + '/2005/Atom'}">
    <title>NBA Top Videos</title>
    <id>nba-top-feed-custom</id>
    {''.join(items)}
</feed>"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(feed_final)
