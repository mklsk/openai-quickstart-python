import os

import openai
import time
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)
openai.api_key = "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"

@app.route('/create', methods=['GET'])
def create_articles():

    args = request.args
    slice_start = args.get('start')
    slice_end = args.get('end')

    df_source = pd.read_csv('data/source/blog_source_27122022.csv')
    df_source = df_source.reset_index()
    df = df_source.truncate(slice_start,slice_end)

    for idx, row in df.iterrows():

        print('[LOG] processing row with index ' + str(idx))
        start_time = time.time()

        openai_prompt = row['API Request']

        attempts = 0
        while attempts < 3:
            try:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=openai_prompt,
                temperature=0.6,
                max_tokens=3700,
                )
                break
            except Exception as e:
                attempts += 1
                print('[ERROR] Error while performing Open AI request:')
                print(e)

        openai_finish_time = time.time()
        print('[LOG] fetched OpenAI response in: ' + str(openai_finish_time - start_time))

        blog_post_content = response.choices[0].text.replace("\n", "")
        parsed_html = BeautifulSoup(blog_post_content)

        parse_html_finish_time = time.time()
        print('[LOG] parsed html in: ' + str(parse_html_finish_time - openai_finish_time))

        df.at[idx, 'Output'] = blog_post_content
        df.at[idx, 'Post title'] = parsed_html.body.find('h1').text
        df.at[idx, 'Post SEO title'] = parsed_html.body.find('h1').text

        df.at[idx, 'Description'] = parsed_html.body.find('p').text
        df.at[idx, 'Meta Description'] = parsed_html.body.find('p').text

        set_csv_field_finish_time = time.time()
        print('[LOG] set csv fields in: ' + str(set_csv_field_finish_time - parse_html_finish_time))

    df.to_csv('data/out/' + str(time.time()) + '.csv')
    return 'File saved'