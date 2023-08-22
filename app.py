from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def fetch_data_from_url(url, result_list):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=5)
        if response.status_code == 200:
            data = response.json()
            result_list.extend(data)
    except asyncio.TimeoutError:
        print("Timeout fetching data from URL:", url)
    except Exception as e:
        print("Error fetching data from URL:", url, e)

@app.route('/numbers', methods=['GET'])
def get_numbers():
    url_list = request.args.getlist('url')
    result = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [fetch_data_from_url(url, result) for url in url_list]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    unique_sorted_numbers = sorted(set(result))
    
    return jsonify(numbers=unique_sorted_numbers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)