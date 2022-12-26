import os

import openai
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup

# import xml.etree.ElementTree as ET
#
# from lxml import etree

# root = etree.Element("root")
# print(root.tag)

# tree = etree.parse("data/blog_template.xml")

# ET.register_namespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/')
# ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
# ET.register_namespace('wfw', 'http://wellformedweb.org/CommentAPI/')
# ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
# ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')

# tree = ET.parse('data/blog_template.xml')
# root = tree.getroot()

# channel_tag = root.find("./channel")
# item_tag = channel_tag.find('./item')
# item_tag_string = ET.tostring(item_tag, encoding='utf8', method='xml')
# channel_tag.remove(item_tag)

app = Flask(__name__)
openai.api_key = "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"

df_source = pd.read_csv('data/blog_table_updated.csv')
df_source = df_source.reset_index()
df = df_source.truncate(0,29)

for idx, row in df.iterrows():

    openai_prompt = row['Open API Query']

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=openai_prompt,
    temperature=0.6,
    max_tokens=3700,
    )

#     blog_post_title = row['Title']
    blog_post_content = response.choices[0].text.replace("\n", "")
#     blog_post_category = 'Misc'

    html = blog_post_content
    parsed_html = BeautifulSoup(html)
#     print(parsed_html.body.find('h1').text)
#     print(parsed_html.body.find('p').text)

    print('open ai response received for prompt: ' + openai_prompt)
    print('Response: ' + blog_post_content)
    df.at[idx, 'API Output'] = blog_post_content

    df.at[idx, 'Title'] = parsed_html.body.find('h1').text
    df.at[idx, 'Meta Title'] = parsed_html.body.find('h1').text

    df.at[idx, 'Description'] = parsed_html.body.find('p').text
    df.at[idx, 'Meta Description'] = parsed_html.body.find('p').text

#     new_blog_item_tag = ET.fromstring(item_tag_string)
#     content_tag = new_blog_item_tag.find("./{http://purl.org/rss/1.0/modules/content/}encoded")
#     title_tag = new_blog_item_tag.find("./title")
#     category_tag = new_blog_item_tag.find("./category")

#     title_tag.text = blog_post_title
#     content_tag.text = blog_post_content
#     category_tag.text = blog_post_category
#     category_tag.set('nicename', blog_post_category.lower())

#     channel_tag.append(new_blog_item_tag)

# tree.write('data/test.xml')
df.to_csv('data/out.csv')
raise RuntimeError('Silly way to finish')


# @app.route("/", methods=("GET", "POST"))
# def index():

#     if request.method == "POST":
#         response = openai.Completion.create(
#             model="text-davinci-002",
#             prompt=request_string,
#             temperature=0.6,
#             max_tokens=1000,
#         )

#         competion_result = response.choices[0].text.replace("\n", "")

#         print(competion_result)
    
#         return redirect(url_for("index", result=competion_result))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)
